import pytest
from fastapi.testclient import TestClient


class TestMainEndpoints:
    
    def test_read_root(self, client: TestClient):
        """Test the root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == "BytePay API"
        assert data["version"] == "1.0.0"
        assert data["message"] == "Welcome to BytePay API"
    
    def test_openapi_docs(self, client: TestClient):
        """Test that OpenAPI documentation is accessible"""
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "BytePay API"
    
    def test_docs_endpoint(self, client: TestClient):
        """Test that Swagger UI docs are accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_cors_headers(self, client: TestClient):
        """Test CORS headers are properly set"""
        response = client.options("/api/v1/merchants/")
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers