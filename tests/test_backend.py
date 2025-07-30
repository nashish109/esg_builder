# This file will contain tests for the backend module.
import unittest
from fastapi.testclient import TestClient
from backend.app import app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome to the ESG Builder API"})

if __name__ == '__main__':
    unittest.main()