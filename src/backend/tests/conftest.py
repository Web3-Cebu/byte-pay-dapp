import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app import models

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def test_app():
    # Create test database tables
    Base.metadata.create_all(bind=engine)
    yield app
    # Drop test database tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_app):
    return TestClient(test_app)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def test_merchant_data():
    return {
        "company_name": "Test Company",
        "company_address": "123 Test Street",
        "wallet_address": "0x1234567890123456789012345678901234567890",
        "company_logo": "https://example.com/logo.png",
        "store_description": "A test store",
        "contact_email": "test@example.com",
        "payment_options": ["ETH", "USDT", "LSK"]
    }

@pytest.fixture
def test_payment_data():
    return {
        "amount": 100.50,
        "currency": "ETH",
        "customer_wallet": "0x9876543210987654321098765432109876543210",
        "payment_metadata": {"product": "test_item", "quantity": 2}
    }