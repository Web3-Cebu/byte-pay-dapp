# BytePay API Tests

This directory contains comprehensive tests for the BytePay API endpoints.

## Test Structure

```
tests/
├── conftest.py          # Test configuration and fixtures
├── test_main.py         # Tests for main app endpoints
├── test_merchants.py    # Tests for merchant API endpoints
├── test_payments.py     # Tests for payment API endpoints
└── README.md           # This file
```

## Running Tests

### Quick Start
```bash
# Run all tests
source venv/bin/activate
python run_tests.py

# Or use pytest directly
python -m pytest tests/ -v
```

### Test Categories

#### 1. Main App Tests (`test_main.py`)
- Root endpoint functionality
- OpenAPI documentation access
- CORS configuration
- Basic app health checks

#### 2. Merchant Tests (`test_merchants.py`)
- ✅ Create merchant with valid data
- ✅ Validation of wallet addresses and email formats
- ✅ Get merchant by ID and list merchants
- ✅ Update merchant information
- ✅ Delete merchant
- ✅ Pagination support
- ✅ Error handling for non-existent merchants

#### 3. Payment Tests (`test_payments.py`)
- ✅ Create payment with valid merchant
- ✅ Get payment by ID and status checking
- ✅ Get payments by merchant
- ✅ Update payment status and transaction hash
- ✅ Payment metadata handling
- ✅ Validation of customer wallet addresses
- ✅ Error handling for invalid data

## Test Fixtures

### Available Fixtures

- `client`: FastAPI test client
- `test_app`: Configured FastAPI application
- `db_session`: Database session for testing
- `test_merchant_data`: Sample merchant data
- `test_payment_data`: Sample payment data
- `created_merchant`: Pre-created merchant for payment tests

### Test Database

Tests use a separate SQLite database (`test.db`) that is:
- Created before each test session
- Isolated per test function (transactions are rolled back)
- Cleaned up after tests complete

## Test Coverage

The test suite covers:

### ✅ Positive Test Cases
- Valid data creation and retrieval
- Successful updates and deletions
- Proper API responses and status codes
- Relationship handling between merchants and payments

### ✅ Negative Test Cases
- Invalid input validation
- Non-existent resource handling
- Malformed wallet addresses
- Missing required fields

### ✅ Edge Cases
- Pagination with various limits
- Empty result sets
- Optional field handling
- Status transitions

## Sample Test Data

### Merchant Data
```json
{
    "company_name": "Test Company",
    "company_address": "123 Test Street",
    "wallet_address": "0x1234567890123456789012345678901234567890",
    "company_logo": "https://example.com/logo.png",
    "store_description": "A test store",
    "contact_email": "test@example.com",
    "payment_options": ["ETH", "USDT", "LSK"]
}
```

### Payment Data
```json
{
    "amount": 100.50,
    "currency": "ETH",
    "customer_wallet": "0x9876543210987654321098765432109876543210",
    "payment_metadata": {
        "product": "test_item",
        "quantity": 2
    }
}
```

## API Endpoints Tested

### Merchant Endpoints
- `POST /api/v1/merchants/` - Create merchant
- `GET /api/v1/merchants/` - List merchants
- `GET /api/v1/merchants/{merchant_id}` - Get merchant
- `PUT /api/v1/merchants/{merchant_id}` - Update merchant
- `DELETE /api/v1/merchants/{merchant_id}` - Delete merchant

### Payment Endpoints
- `POST /api/v1/payments/` - Create payment
- `GET /api/v1/payments/{payment_id}` - Get payment
- `GET /api/v1/payments/merchant/{merchant_id}` - Get merchant payments
- `PUT /api/v1/payments/{payment_id}` - Update payment
- `GET /api/v1/payments/{payment_id}/status` - Check payment status

## Dependencies

The test suite requires:
- `pytest` - Test framework
- `httpx` - HTTP client for API testing
- `fastapi[all]` - FastAPI framework with all dependencies
- `sqlalchemy` - Database ORM

## Notes

- Tests use transaction rollback for database isolation
- Each test is independent and can be run in any order
- The test database is automatically created and cleaned up
- CORS and authentication middleware are tested
- All validation logic is thoroughly covered