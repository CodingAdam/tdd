"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the file that contains the status codes
from src import status
# we need to import the unit under test - counter
from src.counter import app


class CounterTest(TestCase):

    def setUp(self):
        self.client = app.test_client()

    """Counter tests"""

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter_null(self):
        """It should return an error trying to update a null counter"""
        result = self.client.put('/counters/null')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_counter(self):
        """It should return an error for no counter found"""
        # Call to create a counter
        result = self.client.post('/counters/update')

        # Check for successful return code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Create baseline counter
        baseline = self.client.get('/counters/update')
        self.assertEqual(baseline.status_code, status.HTTP_200_OK)

        # Check the counter value of baseline
        baseline = baseline.json['update']
        self.assertEqual(baseline, 0)

        # Update call to created counter
        result = self.client.put('/counters/update')

        # Check for successful return code
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        # Check if value is one more than baseline
        baseline = self.client.get('/counters/update')
        baseline = baseline.json['update']
        self.assertEqual(baseline, 1)

    def test_get_a_counter_null(self):
        """It should return an error for getting a null counter"""
        result = self.client.get('/counters/null1')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_a_counter(self):
        """It should get a counter"""
        # Call to create a counter
        result = self.client.post('/counters/get')

        # Check for successful return code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Create baseline counter
        baseline = self.client.get('/counters/get')
        self.assertEqual(baseline.status_code, status.HTTP_200_OK)

        # Check the counter value of baseline
        baseline = baseline.json['get']
        self.assertEqual(baseline, 0)

    def test_delete_a_counter(self):
        """It should delete a counter"""
        # Call to create a counter
        result = self.client.post('/counters/delete')

        # Check for successful return code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Delete counter
        result = self.client.delete('/counters/delete')
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)

        # Check if counter doesn't exist
        result = self.client.get('/counters/delete')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter_null(self):
        """It should return an error trying to delete a null counter"""
        result = self.client.delete('/counters/null2')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

