import numpy as np
import pandas as pd
import json
import requests

URL = 'http://127.0.0.1:8000'

data = pd.read_csv("products.csv")

records = data.to_dict(orient='records')

"""for record in records:
    response = requests.post(f"{URL}/addNew", 
        json=record     
    )"""

# /getSingleProduct - This allows you to pass a single ID number into the endpoint and return the details of the single product in JSON format.
response = requests.get(f"{URL}/getSingleProduct", params={'id': records[0]['ProductID']})
print(response.json())

# /getAll - This endpoint should return all inventory in JSON format from the database.
response = requests.get(f"{URL}/getAll")
print(len(response.json()))

# /addNew - This endpoint should take in all 5 attributes of a new item and insert them into the database as a new record.
new_record = records[-1].copy()
new_record['ProductID'] = new_record['ProductID'] + 1
response = requests.post(f"{URL}/addNew", json=new_record)
print(response.json())

# /deleteOne - This endpoint should delete a product by the provided ID.
response = requests.delete(f"{URL}/deleteOne", params={'id': new_record['ProductID']})
print(response.status_code)

# /startsWith - This should allow the user to pass a letter to the URL, such as s, and return all products that start with s.
response = requests.get(f"{URL}/startsWith", params={'letter': 'a'})
print(len(response.json()))

# /paginate - This URL should pass in a product ID to start from and a product ID to end from. The products should be returned in a batch of 10.
response = requests.get(f"{URL}/paginate", params={'start_id': records[0]['ProductID'], 'end_id': records[15]['ProductID']})
print(len(response.json()))

# /convert - All of the prices are currently in dollars in the sample data. Implement a URL titled /convert which takes in the ID number of a product and returns the price in euros. An online API should be used to get the current exchange rate.
response = requests.get(f"{URL}/getSingleProduct", params={'id': records[0]['ProductID']})
print(response.json())

response = requests.get(f"{URL}/convert", params={'id': records[0]['ProductID']})
print(response.json())