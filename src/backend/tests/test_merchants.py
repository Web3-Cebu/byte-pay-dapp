import pytest
import json
from fastapi.testclient import TestClient


class TestMerchantEndpoints:
    
    def test_create_merchant(self, client: TestClient, test_merchant_data):
        """Test creating a new merchant"""
        response = client.post("/api/v1/merchants/", json=test_merchant_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["company_name"] == test_merchant_data["company_name"]
        assert data["wallet_address"] == test_merchant_data["wallet_address"]
        assert data["contact_email"] == test_merchant_data["contact_email"]
        assert "merchant_id" in data
        assert "id" in data
        assert "created_at" in data
        assert data["is_active"] is True

    def test_create_merchant_invalid_wallet(self, client: TestClient, test_merchant_data):
        """Test creating merchant with invalid wallet address"""
        invalid_data = test_merchant_data.copy()
        invalid_data["wallet_address"] = "invalid_wallet_address"
        
        response = client.post("/api/v1/merchants/", json=invalid_data)
        assert response.status_code == 422

    def test_create_merchant_invalid_email(self, client: TestClient, test_merchant_data):
        """Test creating merchant with invalid email"""
        invalid_data = test_merchant_data.copy()
        invalid_data["contact_email"] = "invalid_email"
        
        response = client.post("/api/v1/merchants/", json=invalid_data)
        assert response.status_code == 422

    def test_get_merchants(self, client: TestClient, test_merchant_data):
        """Test retrieving list of merchants"""
        # Create a test merchant first
        create_response = client.post("/api/v1/merchants/", json=test_merchant_data)
        assert create_response.status_code == 200
        
        # Get merchants list
        response = client.get("/api/v1/merchants/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["company_name"] == test_merchant_data["company_name"]

    def test_get_merchants_with_pagination(self, client: TestClient, test_merchant_data):
        """Test retrieving merchants with pagination"""
        # Create multiple merchants
        for i in range(3):
            merchant_data = test_merchant_data.copy()
            merchant_data["company_name"] = f"Test Company {i}"
            merchant_data["contact_email"] = f"test{i}@example.com"
            merchant_data["wallet_address"] = f"0x123456789012345678901234567890123456789{i}"
            client.post("/api/v1/merchants/", json=merchant_data)
        
        # Test pagination
        response = client.get("/api/v1/merchants/?skip=1&limit=2")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) <= 2

    def test_get_merchant_by_id(self, client: TestClient, test_merchant_data):
        """Test retrieving a specific merchant by ID"""
        # Create a merchant
        create_response = client.post("/api/v1/merchants/", json=test_merchant_data)
        created_merchant = create_response.json()
        merchant_id = created_merchant["merchant_id"]
        
        # Get merchant by ID
        response = client.get(f"/api/v1/merchants/{merchant_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["merchant_id"] == merchant_id
        assert data["company_name"] == test_merchant_data["company_name"]

    def test_get_nonexistent_merchant(self, client: TestClient):
        """Test retrieving a non-existent merchant"""
        response = client.get("/api/v1/merchants/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Merchant not found"

    def test_update_merchant(self, client: TestClient, test_merchant_data):
        """Test updating an existing merchant"""
        # Create a merchant
        create_response = client.post("/api/v1/merchants/", json=test_merchant_data)
        created_merchant = create_response.json()
        merchant_id = created_merchant["merchant_id"]
        
        # Update merchant
        update_data = {
            "company_name": "Updated Company Name",
            "company_address": "456 Updated Street",
            "wallet_address": "0x1234567890123456789012345678901234567890",
            "company_logo": "https://example.com/new-logo.png",
            "store_description": "Updated description",
            "contact_email": "updated@example.com",
            "payment_options": ["ETH", "BTC"]
        }
        
        response = client.put(f"/api/v1/merchants/{merchant_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["company_name"] == "Updated Company Name"
        assert data["company_address"] == "456 Updated Street"
        assert data["contact_email"] == "updated@example.com"

    def test_update_nonexistent_merchant(self, client: TestClient, test_merchant_data):
        """Test updating a non-existent merchant"""
        response = client.put("/api/v1/merchants/nonexistent-id", json=test_merchant_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Merchant not found"

    def test_delete_merchant(self, client: TestClient, test_merchant_data):
        """Test deleting an existing merchant"""
        # Create a merchant
        create_response = client.post("/api/v1/merchants/", json=test_merchant_data)
        created_merchant = create_response.json()
        merchant_id = created_merchant["merchant_id"]
        
        # Delete merchant
        response = client.delete(f"/api/v1/merchants/{merchant_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["message"] == "Merchant deleted"
        
        # Verify merchant is deleted
        get_response = client.get(f"/api/v1/merchants/{merchant_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_merchant(self, client: TestClient):
        """Test deleting a non-existent merchant"""
        response = client.delete("/api/v1/merchants/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Merchant not found"

    def test_merchant_data_validation(self, client: TestClient):
        """Test merchant data validation"""
        # Test missing required fields
        incomplete_data = {
            "company_name": "Test Company"
            # Missing required fields
        }
        
        response = client.post("/api/v1/merchants/", json=incomplete_data)
        assert response.status_code == 422
        
        # Test invalid wallet address format
        invalid_wallet_data = {
            "company_name": "Test Company",
            "wallet_address": "not_a_valid_wallet",
            "contact_email": "test@example.com",
            "payment_options": ["ETH"]
        }
        
        response = client.post("/api/v1/merchants/", json=invalid_wallet_data)
        assert response.status_code == 422

    def test_merchant_optional_fields(self, client: TestClient):
        """Test merchant creation with minimal required fields"""
        minimal_data = {
            "company_name": "Minimal Company",
            "wallet_address": "0x1234567890123456789012345678901234567890",
            "contact_email": "minimal@example.com",
            "payment_options": ["ETH"]
        }
        
        response = client.post("/api/v1/merchants/", json=minimal_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["company_name"] == "Minimal Company"
        assert data["company_address"] is None
        assert data["company_logo"] is None
        assert data["store_description"] is None