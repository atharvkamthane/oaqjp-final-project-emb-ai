"""Tests for the Accounts REST API, CORS, and security headers."""

import unittest
from app import create_app


class AccountsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "FORCE_HTTPS": False})
        self.client = self.app.test_client()

    def test_service_root_metadata(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"name": "Account REST API Service", "version": "1.0"})

    def test_create_account(self):
        response = self.client.post("/accounts", json={"name": "Test User", "email": "test@example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Test User")
        self.assertIn("id", response.get_json())

    def test_list_accounts(self):
        self.client.post("/accounts", json={"name": "Test User", "email": "test@example.com"})
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_read_account(self):
        created = self.client.post("/accounts", json={"name": "Test User", "email": "test@example.com"}).get_json()
        response = self.client.get("/accounts/" + created["id"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email"], "test@example.com")

    def test_update_account(self):
        created = self.client.post("/accounts", json={"name": "Test User", "email": "test@example.com"}).get_json()
        response = self.client.put("/accounts/" + created["id"], json={"name": "Updated User"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Updated User")

    def test_delete_account(self):
        created = self.client.post("/accounts", json={"name": "Test User", "email": "test@example.com"}).get_json()
        response = self.client.delete("/accounts/" + created["id"])
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.client.get("/accounts/" + created["id"]).status_code, 404)

    def test_create_requires_fields(self):
        response = self.client.post("/accounts", json={"name": "Only Name"})
        self.assertEqual(response.status_code, 400)

    def test_cors_header(self):
        response = self.client.get("/", headers={"Origin": "http://example.com"})
        self.assertIn("Access-Control-Allow-Origin", response.headers, "It should return a CORS header")

    def test_security_headers(self):
        response = self.client.get("/")
        self.assertIn("X-Frame-Options", response.headers, "It should return security headers")
        self.assertIn("Content-Security-Policy", response.headers)


if __name__ == "__main__":
    unittest.main()
