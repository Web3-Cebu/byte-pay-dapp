# BytePay DApp

A simple decentralized payment application (dApp) that enables users to send cryptocurrency payments via Ethereum and Lisk blockchains. This project demonstrates the integration of Web3 wallet connectivity and payment functionality using MetaMask or other Web3 wallets.

## Features

- **Multi-Chain Support**: Connect your Ethereum or Lisk wallet using MetaMask or compatible Web3 wallets
- **Merchant Management**: Complete merchant onboarding and configuration system
- **Payment Processing**: Send cryptocurrency payments directly from the dApp interface
- **FastAPI Backend**: Robust API for merchant and payment management
- **Elegant UI**: Modern, responsive design with authentication flows
- **Multiple Cryptocurrencies**: Support for USDT, ETH, and LISK payments

## Project Structure

```
byte-pay-dapp/
├── src/
│   ├── backend/           # FastAPI backend application
│   │   ├── app/
│   │   │   ├── api/       # API endpoints (merchants, payments)
│   │   │   ├── models.py  # Database models
│   │   │   ├── schemas.py # Pydantic schemas
│   │   │   └── main.py    # FastAPI app with static file serving
│   │   ├── tests/         # Backend tests
│   │   └── requirements.txt
│   └── frontend/          # Production frontend application
├── prototype/
│   ├── merchant/          # Merchant UI prototypes with login system
│   └── metamask/          # MetaMask integration demos
├── deploy/
│   └── start_local_app.py # Local development server script
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+ for backend
- MetaMask extension or compatible Web3 wallet installed in your browser

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Web3-Cebu/byte-pay-dapp.git
   cd byte-pay-dapp
   ```

2. **Start the local development server:**
   ```bash
   python3 deploy/start_local_app.py
   ```

   This script will automatically:
   - Create a Python virtual environment
   - Install backend dependencies
   - Start the FastAPI server with frontend serving
   - Make the app available at http://localhost:8000

### Manual Setup (Alternative)

If you prefer manual setup:

1. **Backend Setup:**
   ```bash
   cd src/backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start the backend:**
   ```bash
   hypercorn app.main:app --bind 0.0.0.0:8000 --reload
   ```

## Usage

### Merchant Setup
1. Navigate to http://localhost:8000
2. Complete the merchant login process using popular email providers (Gmail, Yahoo, Outlook)
3. Configure your store settings:
   - Company information
   - Wallet address for receiving payments
   - Accepted payment options (USDT, ETH, LISK)
   - Store description and contact details

### Payment Processing
1. Connect your wallet by clicking the "Connect" button
2. Enter the recipient's wallet address
3. Specify the amount to send
4. Select the cryptocurrency (USDT, ETH, or LISK)
5. Click "Send" to initiate the payment transaction via your connected wallet
6. Confirm the transaction details in MetaMask or your wallet app

### API Documentation
- **API Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/api/v1/openapi.json

## API Endpoints

### Merchants
- `POST /api/v1/merchants/` - Create a new merchant
- `GET /api/v1/merchants/` - List all merchants
- `GET /api/v1/merchants/{merchant_id}` - Get merchant by ID
- `PUT /api/v1/merchants/{merchant_id}` - Update merchant
- `DELETE /api/v1/merchants/{merchant_id}` - Delete merchant

### Payments
- `POST /api/v1/payments/` - Create a new payment
- `GET /api/v1/payments/{payment_id}` - Get payment by ID
- `GET /api/v1/merchants/{merchant_id}/payments` - Get merchant payments
- `PUT /api/v1/payments/{payment_id}` - Update payment status
- `GET /api/v1/payments/{payment_id}/status` - Check payment status

## Development

### Running Tests
```bash
cd src/backend
./venv/bin/python -m pytest tests/ -v
```

### Project Components

- **Backend**: FastAPI application with SQLAlchemy ORM
- **Frontend**: Static HTML/CSS/JavaScript served by FastAPI
- **Prototypes**: Design playground for UI experimentation
- **Database**: SQLite for development (configurable for production)

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy, Pydantic, Hypercorn
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Blockchain**: Ethers.js/Web3.js for blockchain interactions
- **Wallet**: MetaMask SDK for wallet integration
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Testing**: Pytest, FastAPI TestClient

## Contributing

Contributions and improvements are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For questions, issues, or support:
- Open an issue on GitHub
- Check the API documentation at `/docs` when running locally
- Review the prototype implementations in the `prototype/` directory

---

**Note**: This is a demonstration project. For production use, ensure proper security measures, environment configuration, and testing are in place.