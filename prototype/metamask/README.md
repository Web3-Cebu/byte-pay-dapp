# BytePay - Crypto Merchant Store

A simple merchant web page selling post-it notes with cryptocurrency payment integration via MetaMask.

## Features

- Product display for premium post-it notes
- Real-time cryptocurrency price conversion
- MetaMask wallet integration
- Support for ETH and LISK payments
- Responsive design
- Transaction confirmation

## How to Use

1. Open `index.html` in a web browser
2. Click "Connect Wallet" to connect your MetaMask wallet
3. Choose payment method (ETH or LISK)
4. Complete the transaction through MetaMask
5. Receive confirmation of successful payment

## Payment Networks

- **Ethereum**: Mainnet for ETH payments
- **Lisk**: Lisk network for LSK payments (automatically added to MetaMask if needed)

## Price Conversion

Prices are automatically fetched from CoinGecko API and updated every minute.

## Files

- `index.html` - Main HTML structure
- `styles.css` - CSS styling and responsive design
- `app.js` - JavaScript for MetaMask integration and payment processing

## Security Note

This is a demo application. In production:
- Use proper merchant address validation
- Implement server-side order processing
- Add proper error handling and logging
- Use secure price oracles
- Implement proper inventory management