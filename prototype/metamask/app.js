class CryptoPayment {
    constructor() {
        this.web3 = null;
        this.userAccount = null;
        this.productPrice = 9.99;
        this.selectedVendor = null;
        this.vendors = [
            {
                id: 'vendor1',
                name: 'Post-it Store',
                address: '0x742d35Cc6464C4532d9E46C0c5a4E6C30D60E8EE',
                description: 'Premium office supplies'
            },
            {
                id: 'vendor2', 
                name: 'Tech Gadgets Co',
                address: '0x1234567890123456789012345678901234567890',
                description: 'Latest tech accessories'
            },
            {
                id: 'vendor3',
                name: 'Books & More',
                address: '0x9876543210987654321098765432109876543210',
                description: 'Educational materials'
            }
        ];
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.populateVendorSelect();
        await this.updateCryptoPrices();
        setInterval(() => this.updateCryptoPrices(), 60000);
        
        // Check if MetaMask is already available
        if (window.ethereum) {
            console.log('MetaMask detected on page load');
        } else {
            // Listen for MetaMask injection
            window.addEventListener('ethereum#initialized', this.onEthereumInit.bind(this), {
                once: true,
            });
            
            // Fallback timeout
            setTimeout(() => {
                if (window.ethereum) {
                    this.onEthereumInit();
                }
            }, 3000);
        }
    }
    
    onEthereumInit() {
        console.log('Ethereum initialized');
    }

    setupEventListeners() {
        document.getElementById('connect-wallet').addEventListener('click', () => this.connectWallet());
        document.getElementById('pay-eth').addEventListener('click', () => this.payWithCrypto('ETH'));
        document.getElementById('pay-lisk').addEventListener('click', () => this.payWithCrypto('LISK'));
        document.getElementById('vendor-select').addEventListener('change', (e) => this.selectVendor(e.target.value));
    }

    populateVendorSelect() {
        const select = document.getElementById('vendor-select');
        this.vendors.forEach(vendor => {
            const option = document.createElement('option');
            option.value = vendor.id;
            option.textContent = `${vendor.name} - ${vendor.description}`;
            select.appendChild(option);
        });
        this.selectVendor(this.vendors[0].id);
    }

    selectVendor(vendorId) {
        this.selectedVendor = this.vendors.find(v => v.id === vendorId);
        const vendorInfo = document.getElementById('vendor-info');
        if (this.selectedVendor) {
            vendorInfo.innerHTML = `
                <p><strong>Vendor:</strong> ${this.selectedVendor.name}</p>
                <p><strong>Address:</strong> ${this.selectedVendor.address.substring(0, 6)}...${this.selectedVendor.address.substring(38)}</p>
            `;
        }
    }

    async connectWallet() {
        if (!window.ethereum) {
            alert('MetaMask is not installed or not loaded yet. Please install MetaMask and refresh the page.');
            return;
        }

        try {
            console.log('Requesting MetaMask connection...');
            
            const accounts = await window.ethereum.request({
                method: 'eth_requestAccounts'
            });
            
            if (accounts.length > 0) {
                this.userAccount = accounts[0];
                this.web3 = new Web3(window.ethereum);
                this.updateUI();
                console.log('Connected to:', this.userAccount);
                
                // Listen for account changes
                window.ethereum.on('accountsChanged', (accounts) => {
                    if (accounts.length === 0) {
                        this.userAccount = null;
                        this.hideWalletInfo();
                    } else {
                        this.userAccount = accounts[0];
                        this.updateUI();
                    }
                });
            }
        } catch (error) {
            console.error('Connection error:', error);
            if (error.code === 4001) {
                alert('Connection rejected by user.');
            } else {
                alert(`Failed to connect: ${error.message}`);
            }
        }
    }

    updateUI() {
        if (this.userAccount) {
            document.getElementById('connect-wallet').style.display = 'none';
            document.getElementById('wallet-info').classList.remove('hidden');
            document.getElementById('wallet-address').textContent = 
                `${this.userAccount.substring(0, 6)}...${this.userAccount.substring(38)}`;
        }
    }

    hideWalletInfo() {
        document.getElementById('connect-wallet').style.display = 'block';
        document.getElementById('wallet-info').classList.add('hidden');
    }

    async updateCryptoPrices() {
        try {
            const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=ethereum,lisk&vs_currencies=usd');
            const data = await response.json();
            
            if (data.ethereum) {
                const ethAmount = (this.productPrice / data.ethereum.usd).toFixed(6);
                document.getElementById('eth-price').textContent = `${ethAmount} ETH`;
            }
            
            if (data.lisk) {
                const liskAmount = (this.productPrice / data.lisk.usd).toFixed(2);
                document.getElementById('lisk-price').textContent = `${liskAmount} LSK`;
            }
        } catch (error) {
            console.error('Error fetching crypto prices:', error);
            document.getElementById('eth-price').textContent = '~0.003 ETH';
            document.getElementById('lisk-price').textContent = '~15 LSK';
        }
    }

    async payWithCrypto(cryptoType) {
        if (!this.userAccount) {
            alert('Please connect your wallet first.');
            return;
        }

        if (!this.selectedVendor) {
            alert('Please select a vendor first.');
            return;
        }

        try {
            this.showLoadingOverlay();
            
            let transactionParams;
            
            if (cryptoType === 'ETH') {
                const ethAmount = await this.getETHAmount();
                transactionParams = {
                    from: this.userAccount,
                    to: this.selectedVendor.address,
                    value: this.web3.utils.toWei(ethAmount.toString(), 'ether'),
                    gas: '21000',
                };
            } else if (cryptoType === 'LISK') {
                await this.switchToLiskNetwork();
                const liskAmount = await this.getLISKAmount();
                transactionParams = {
                    from: this.userAccount,
                    to: this.selectedVendor.address,
                    value: this.web3.utils.toWei(liskAmount.toString(), 'ether'),
                    gas: '21000',
                };
            }

            const txHash = await window.ethereum.request({
                method: 'eth_sendTransaction',
                params: [transactionParams],
            });

            this.hideLoadingOverlay();
            this.showSuccessMessage(txHash, cryptoType, this.selectedVendor.name);
            
        } catch (error) {
            this.hideLoadingOverlay();
            console.error('Payment error:', error);
            
            if (error.code === 4001) {
                alert('Payment cancelled by user.');
            } else {
                alert(`Payment failed: ${error.message}`);
            }
        }
    }

    async getETHAmount() {
        try {
            const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd');
            const data = await response.json();
            return (this.productPrice / data.ethereum.usd).toFixed(6);
        } catch (error) {
            return '0.003';
        }
    }

    async getLISKAmount() {
        try {
            const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=lisk&vs_currencies=usd');
            const data = await response.json();
            return (this.productPrice / data.lisk.usd).toFixed(2);
        } catch (error) {
            return '15';
        }
    }

    async switchToLiskNetwork() {
        try {
            await window.ethereum.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: '0x46a' }],
            });
        } catch (switchError) {
            if (switchError.code === 4902) {
                try {
                    await window.ethereum.request({
                        method: 'wallet_addEthereumChain',
                        params: [
                            {
                                chainId: '0x46a',
                                chainName: 'Lisk',
                                nativeCurrency: {
                                    name: 'Lisk',
                                    symbol: 'LSK',
                                    decimals: 18,
                                },
                                rpcUrls: ['https://rpc.api.lisk.com'],
                                blockExplorerUrls: ['https://liskscan.com/'],
                            },
                        ],
                    });
                } catch (addError) {
                    throw new Error('Failed to add Lisk network to MetaMask');
                }
            } else {
                throw switchError;
            }
        }
    }

    showLoadingOverlay() {
        document.getElementById('loading-overlay').classList.remove('hidden');
    }

    hideLoadingOverlay() {
        document.getElementById('loading-overlay').classList.add('hidden');
    }

    showSuccessMessage(txHash, cryptoType, vendorName) {
        const message = `
            <div style="background: white; padding: 30px; border-radius: 15px; text-align: center; max-width: 400px; color: #333;">
                <div style="font-size: 3rem; color: #28a745; margin-bottom: 20px;">✅</div>
                <h2 style="color: #28a745; margin-bottom: 15px;">Payment Successful!</h2>
                <p style="margin-bottom: 20px;">Your payment to <strong>${vendorName}</strong> has been processed successfully.</p>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <p style="font-weight: bold; margin-bottom: 10px;">Transaction Hash:</p>
                    <p style="font-family: monospace; font-size: 12px; word-break: break-all; color: #667eea;">${txHash}</p>
                </div>
                <p style="color: #666; margin-bottom: 20px;">Paid with ${cryptoType} to ${vendorName}</p>
                <button onclick="location.reload()" style="background: #28a745; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-weight: bold;">Continue Shopping</button>
            </div>
        `;
        
        const overlay = document.getElementById('loading-overlay');
        overlay.innerHTML = message;
        overlay.style.display = 'flex';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new CryptoPayment();
});