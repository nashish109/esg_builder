# This file will contain tests for the backend module.
import unittest
from fastapi.testclient import TestClient
from backend.api.main import app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "ESG Builder API", "version": "1.0.0"})

if __name__ == '__main__':
    unittest.main()