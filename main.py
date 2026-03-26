from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "Products")
COLLECTION = "Products"


@app.on_event("startup")
async def startup():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.db = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.close()


def item_to_dict(item: dict) -> dict:
    item["ProductID"] = item.pop("_id")
    return item

class ItemCreate(BaseModel):
    ProductID: int
    Name: str
    UnitPrice: float
    StockQuantity: int
    Description: Optional[str]

class ItemResponse(BaseModel):
    ProductID: int
    Name: str
    UnitPrice: float
    StockQuantity: int
    Description: Optional[str] = None

class ConvertResponse(BaseModel):
    ProductID: int
    Name: str
    price_usd: float
    price_eur: float
    exchange_rate: float
    rate_date: str

# /getSingleProduct - This allows you to pass a single ID number into the endpoint and return the details of the single product in JSON format.
@app.get("/getSingleProduct", response_model=ItemResponse)
async def get_single_product(id: int):
    item = await app.db[COLLECTION].find_one({"_id": id})
    return item_to_dict(item)


# /getAll - This endpoint should return all inventory in JSON format from the database.
@app.get("/getAll", response_model=list[ItemResponse])
async def get_all():
    items = app.db[COLLECTION].find()
    return [item_to_dict(item) async for item in items]


# /addNew - This endpoint should take in all 5 attributes of a new item and insert them into the database as a new record.
@app.post("/addNew", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def add_new(item: ItemCreate):
    existing = await app.db[COLLECTION].find_one({"_id": item.ProductID})
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Product with ID {item.ProductID} already exists"
        )
    item = item.model_dump()
    item["_id"] = item.pop("ProductID")
    await app.db[COLLECTION].insert_one(item)
    created = await app.db[COLLECTION].find_one({"_id": item["_id"]})
    return item_to_dict(created)


# /deleteOne - This endpoint should delete a product by the provided ID.
@app.delete("/deleteOne", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one(id: int):
    result = await app.db[COLLECTION].delete_one({"_id": id})


# /startsWith - This should allow the user to pass a letter to the URL, such as s, and return all products that start with s.
@app.get("/startsWith", response_model=list[ItemResponse])
async def starts_with(letter: str):
    items = app.db[COLLECTION].find(
        {"Name": {"$regex": f"^{letter}", "$options": "i"}}
    )
    results = [item_to_dict(item) async for item in items]
    return results


# /paginate - This URL should pass in a product ID to start from and a product ID to end from. The products should be returned in a batch of 10.
@app.get("/paginate", response_model=list[ItemResponse])
async def paginate(start_id: int, end_id: int):
    items = (
        app.db[COLLECTION]
        .find({"_id": {"$gte": start_id, "$lte": end_id}})
        .sort("_id", 1)
        .limit(10)
    )
    results = [item_to_dict(item) async for item in items]
    return results

# /convert - All of the prices are currently in dollars in the sample data. Implement a URL titled /convert which takes in the ID number of a product and returns the price in euros. An online API should be used to get the current exchange rate.
@app.get("/convert", response_model=ConvertResponse)
async def convert(id: int):
    item = await app.db[COLLECTION].find_one({"_id": id})

    async with httpx.AsyncClient() as client:
        try:
            fx_response = await client.get(
                "https://api.frankfurter.dev/v1/latest",
                params={"base": "USD", "symbols": "EUR"},
                timeout=10.0
            )
            fx_response.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(
                status_code=503,
                detail="Could not reach exchange rate API. Try again later."
            )

    fx_data = fx_response.json()
    eur_rate = fx_data["rates"]["EUR"]
    rate_date = fx_data["date"]
    price_usd = item["UnitPrice"]
    price_eur = round(price_usd * eur_rate, 2)

    return ConvertResponse(
        ProductID=item["_id"],
        Name=item["Name"],
        price_usd=price_usd,
        price_eur=price_eur,
        exchange_rate=eur_rate,
        rate_date=rate_date
    )