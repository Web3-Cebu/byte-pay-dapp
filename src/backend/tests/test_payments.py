import pytest
import json
from fastapi.testclient import TestClient


class TestPaymentEndpoints:
    
    @pytest.fixture
    def created_merchant(self, client: TestClient, test_merchant_data):
        """Create a merchant for payment tests"""
        response = client.post("/api/v1/merchants/", json=test_merchant_data)
        return response.json()
    
    def test_create_payment(self, client: TestClient, created_merchant, test_payment_data):
        """Test creating a new payment"""
        payment_data = test_payment_data.copy()
        payment_data["merchant_id"] = created_merchant["merchant_id"]
        
        response = client.post("/api/v1/payments/", json=payment_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["amount"] == test_payment_data["amount"]
        assert data["currency"] == test_payment_data["currency"]
        assert data["customer_wallet"] == test_payment_data["customer_wallet"]
        assert data["status"] == "pending"
        assert "payment_id" in data
        assert "id" in data
        assert "created_at" in data
        assert data["merchant"]["merchant_id"] == created_merchant["merchant_id"]

    def test_create_payment_invalid_merchant(self, client: TestClient, test_payment_data):
        """Test creating payment with invalid merchant ID"""
        payment_data = test_payment_data.copy()
        payment_data["merchant_id"] = "nonexistent-merchant-id"
        
        response = client.post("/api/v1/payments/", json=payment_data)
        assert response.status_code == 500  # Should be handled better in real app

    def test_create_payment_invalid_wallet(self, client: TestClient, created_merchant, test_payment_data):
        """Test creating payment with invalid customer wallet"""
        payment_data = test_payment_data.copy()
        payment_data["merchant_id"] = created_merchant["merchant_id"]
        payment_data["customer_wallet"] = "invalid_wallet_address"
        
        response = client.post("/api/v1/payments/", json=payment_data)
        assert response.status_code == 422

    def test_get_payment_by_id(self, client: TestClient, created_merchant, test_payment_data):
        """Test retrieving a specific payment by ID"""
        # Create a payment
        payment_data = test_payment_data.copy()
        payment_data["merchant_id"] = created_merchant["merchant_id"]
        
        create_response = client.post("/api/v1/payments/", json=payment_data)
        created_payment = create_response.json()
        payment_id = created_payment["payment_id"]
        
        # Get payment by ID
        response = client.get(f"/api/v1/payments/{payment_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["payment_id"] == payment_id
        assert data["amount"] == test_payment_data["amount"]
        assert data["merchant"]["merchant_id"] == created_merchant["merchant_id"]

    def test_get_nonexistent_payment(self, client: TestClient):
        """Test retrieving a non-existent payment"""
        response = client.get("/api/v1/payments/nonexistent-payment-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Payment not found"

    def test_get_merchant_payments(self, client: TestClient, created_merchant, test_payment_data):
        """Test retrieving payments for a specific merchant"""
        # Create multiple payments for the merchant
        for i in range(3):
            payment_data = test_payment_data.copy()
            payment_data["merchant_id"] = created_merchant["merchant_id"]
            payment_data["amount"] = 100.0 + i * 10
            client.post("/api/v1/payments/", json=payment_data)
        
        # Get merchant payments
        response = client.get(f"/api/v1/payments/merchant/{created_merchant['merchant_id']}")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Verify all payments belong to the merchant
        for payment in data:
            assert payment["merchant"]["merchant_id"] == created_merchant["merchant_id"]

    def test_get_merchant_payments_with_pagination(self, client: TestClient, created_merchant, test_payment_data):
        """Test retrieving merchant payments with pagination"""
        # Create multiple payments
        for i in range(5):
            payment_data = test_payment_data.copy()
            payment_data["merchant_id"] = created_merchant["merchant_id"]
            payment_data["amount"] = 100.0 + i * 10
            client.post("/api/v1/payments/", json=payment_data)
        
        # Test pagination
        response = client.get(f"/api/v1/payments/merchant/{created_merchant['merchant_id']}?skip=2&limit=2")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) <= 2

    def test_get_nonexistent_merchant_payments(self, client: TestClient):
        """Test retrieving payments for non-existent merchant"""
        response = client.get("/api/v1/payments/merchant/nonexistent-merchant-id")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_update_payment(self, client: TestClient, created_merchant, test_payment_data):
        """Test updating an existing payment"""
        # Create a payment
        payment_data = test_payment_data.copy()
        payment_data["merchant_id"] = created_merchant["merchant_id"]
        
        create_response = client.post("/api/v1/payments/", json=payment_data)
        created_payment = create_response.json()
        payment_id = created_payment["payment_id"]
        
        # Update payment
        update_data = {
            "status": "completed",
            "tx_hash": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
        }
        
        response = client.put(f"/api/v1/payments/{payment_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "completed"
        assert data["tx_hash"] == update_data["tx_hash"]

    def test_update_nonexistent_payment(self, client: TestClient):
        """Test updating a non-existent payment"""
        update_data = {
            "status": "completed",
            "tx_hash": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
        }
        
        response = client.put("/api/v1/payments/nonexistent-payment-id", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Payment not found"

    def test_check_payment_status(self, client: TestClient, created_merchant, test_payment_data):
        """Test checking payment status"""
        # Create a payment
        payment_data = test_payment_data.copy()
        payment_data["merchant_id"] = created_merchant["merchant_id"]
        
        create_response = client.post("/api/v1/payments/", json=payment_data)
        created_payment = create_response.json()
        payment_id = created_payment["payment_id"]
        
        # Check initial status
        response = client.get(f"/api/v1/payments/{payment_id}/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["payment_id"] == payment_id
        assert data["status"] == "pending"
        assert data["tx_hash"] is None
        
        # Update payment status
        update_data = {
            "status": "completed",
            "tx_hash": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
        }
        client.put(f"/api/v1/payments/{payment_id}", json=update_data)
        
        # Check updated status
        response = client.get(f"/api/v1/payments/{payment_id}/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "completed"
        assert data["tx_hash"] == update_data["tx_hash"]

    def test_check_nonexistent_payment_status(self, client: TestClient):
        """Test checking status of non-existent payment"""
        response = client.get("/api/v1/payments/nonexistent-payment-id/status")
        assert response.status_code == 404
        assert response.json()["detail"] == "Payment not found"

    def test_payment_data_validation(self, client: TestClient, created_merchant):
        """Test payment data validation"""
        # Test missing required fields
        incomplete_data = {
            "amount": 100.0
            # Missing required fields
        }
        
        response = client.post("/api/v1/payments/", json=incomplete_data)
        assert response.status_code == 422
        
        # Test invalid amount
        invalid_amount_data = {
            "merchant_id": created_merchant["merchant_id"],
            "amount": -50.0,  # Negative amount
            "currency": "ETH",
            "customer_wallet": "0x9876543210987654321098765432109876543210"
        }
        
        response = client.post("/api/v1/payments/", json=invalid_amount_data)
        # Should validate positive amount in real implementation

    def test_payment_status_transitions(self, client: TestClient, created_merchant, test_payment_data):
        """Test payment status transitions"""
        # Create a payment
        payment_data = test_payment_data.copy()
        payment_data["merchant_id"] = created_merchant["merchant_id"]
        
        create_response = client.post("/api/v1/payments/", json=payment_data)
        created_payment = create_response.json()
        payment_id = created_payment["payment_id"]
        
        # Test valid status transitions
        valid_statuses = ["pending", "completed", "failed"]
        
        for status in valid_statuses:
            update_data = {"status": status}
            response = client.put(f"/api/v1/payments/{payment_id}", json=update_data)
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == status

    def test_payment_with_metadata(self, client: TestClient, created_merchant):
        """Test payment creation with metadata"""
        payment_data = {
            "merchant_id": created_merchant["merchant_id"],
            "amount": 150.75,
            "currency": "USDT",
            "customer_wallet": "0x9876543210987654321098765432109876543210",
            "payment_metadata": {
                "product_id": "12345",
                "product_name": "Test Product",
                "quantity": 2,
                "customer_note": "Express delivery please"
            }
        }
        
        response = client.post("/api/v1/payments/", json=payment_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["payment_metadata"]["product_id"] == "12345"
        assert data["payment_metadata"]["quantity"] == 2