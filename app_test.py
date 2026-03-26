import unittest

from main import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # /getSingleProduct - This allows you to pass a single ID number into the endpoint and return the details of the single product in JSON format.
    def test_get_single_product(self):
        response = self.app.get('/getSingleProduct', params={'id': 1001})
        self.assertEqual(response.status_code, 200)

    # /getAll - This endpoint should return all inventory in JSON format from the database.
    def test_get_all(self):
        response = self.app.get('/getAll')
        self.assertEqual(response.status_code, 200)

    # /addNew - This endpoint should take in all 5 attributes of a new item and insert them into the database as a new record.
    def test_add_new(self):
        response = self.app.get('/addNew')
        self.assertEqual(response.status_code, 200)

    # /deleteOne - This endpoint should delete a product by the provided ID.
    def test_delete_one(self):
        response = self.app.get('/deleteOne')
        self.assertEqual(response.status_code, 200)

    # /startsWith - This should allow the user to pass a letter to the URL, such as s, and return all products that start with s.
    def test_starts_with(self):
        response = self.app.get('/startsWith')
        self.assertEqual(response.status_code, 200)

    # /paginate - This URL should pass in a product ID to start from and a product ID to end from. The products should be returned in a batch of 10.
    def test_paginate(self):
        response = self.app.get('/paginate')
        self.assertEqual(response.status_code, 200)

    # /convert - All of the prices are currently in dollars in the sample data. Implement a URL titled /convert which takes in the ID number of a product and returns the price in euros. An online API should be used to get the current exchange rate.
    def test_convert(self):
        response = self.app.get('/convert')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()