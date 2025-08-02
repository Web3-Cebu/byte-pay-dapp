class MerchantSetup {
    constructor() {
        this.form = document.getElementById('merchant-form');
        this.previewSection = document.getElementById('preview-section');
        this.previewContent = document.getElementById('preview-content');
        this.successModal = document.getElementById('success-modal');
        this.logoPreview = document.getElementById('logo-preview');
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadSavedConfiguration();
    }

    setupEventListeners() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Preview button
        document.getElementById('preview-btn').addEventListener('click', () => this.showPreview());
        
        // Logo URL input for live preview
        document.getElementById('company-logo').addEventListener('input', (e) => this.updateLogoPreview(e.target.value));
        
        // Payment options validation
        const paymentCheckboxes = document.querySelectorAll('input[name="paymentOptions"]');
        paymentCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => this.validatePaymentOptions());
        });
        
        // Wallet address validation
        document.getElementById('wallet-address').addEventListener('input', (e) => this.validateWalletAddress(e.target.value));
        
        // Modal actions
        document.getElementById('view-customer-page').addEventListener('click', () => this.viewCustomerPage());
        document.getElementById('edit-config').addEventListener('click', () => this.closeModal());
        
        // Real-time form validation
        const inputs = this.form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
        });
    }

    handleSubmit(e) {
        e.preventDefault();
        
        if (this.validateForm()) {
            const config = this.getFormData();
            this.saveConfiguration(config);
            this.showSuccessModal();
        }
    }

    validateForm() {
        let isValid = true;
        
        // Validate required fields
        const requiredFields = ['company-name', 'wallet-address'];
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!field.value.trim()) {
                this.showFieldError(field, 'This field is required');
                isValid = false;
            } else {
                this.clearFieldError(field);
            }
        });
        
        // Validate wallet address
        const walletAddress = document.getElementById('wallet-address').value;
        if (walletAddress && !this.isValidWalletAddress(walletAddress)) {
            this.showFieldError(document.getElementById('wallet-address'), 'Invalid wallet address format');
            isValid = false;
        }
        
        // Validate at least one payment option is selected
        const paymentOptions = document.querySelectorAll('input[name="paymentOptions"]:checked');
        if (paymentOptions.length === 0) {
            this.showFieldError(document.querySelector('.checkbox-group'), 'Please select at least one payment option');
            isValid = false;
        } else {
            this.clearFieldError(document.querySelector('.checkbox-group'));
        }
        
        return isValid;
    }

    validateField(field) {
        if (field.hasAttribute('required') && !field.value.trim()) {
            this.showFieldError(field, 'This field is required');
            return false;
        }
        
        if (field.id === 'wallet-address' && field.value && !this.isValidWalletAddress(field.value)) {
            this.showFieldError(field, 'Invalid wallet address format');
            return false;
        }
        
        this.clearFieldError(field);
        return true;
    }

    validateWalletAddress(address) {
        if (!address) return true; // Allow empty for real-time validation
        return this.isValidWalletAddress(address);
    }

    isValidWalletAddress(address) {
        return /^0x[a-fA-F0-9]{40}$/.test(address);
    }

    validatePaymentOptions() {
        const paymentOptions = document.querySelectorAll('input[name="paymentOptions"]:checked');
        if (paymentOptions.length > 0) {
            this.clearFieldError(document.querySelector('.checkbox-group'));
        }
    }

    showFieldError(field, message) {
        this.clearFieldError(field);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.style.color = '#dc3545';
        errorDiv.style.fontSize = '0.875rem';
        errorDiv.style.marginTop = '5px';
        errorDiv.textContent = message;
        
        if (field.classList.contains('checkbox-group')) {
            field.parentNode.appendChild(errorDiv);
        } else {
            field.parentNode.appendChild(errorDiv);
        }
        
        field.style.borderColor = '#dc3545';
    }

    clearFieldError(field) {
        const errorDiv = field.parentNode.querySelector('.field-error');
        if (errorDiv) {
            errorDiv.remove();
        }
        
        if (field.style) {
            field.style.borderColor = '';
        }
    }

    updateLogoPreview(url) {
        if (url && this.isValidURL(url)) {
            const img = document.createElement('img');
            img.src = url;
            img.onerror = () => {
                this.logoPreview.innerHTML = '<span style="color: #dc3545;">Invalid image URL</span>';
                this.logoPreview.classList.add('show');
            };
            img.onload = () => {
                this.logoPreview.innerHTML = '';
                this.logoPreview.appendChild(img);
                this.logoPreview.classList.add('show');
            };
        } else {
            this.logoPreview.classList.remove('show');
        }
    }

    isValidURL(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    getFormData() {
        const formData = new FormData(this.form);
        const config = {};
        
        // Get regular form fields
        for (let [key, value] of formData.entries()) {
            if (key === 'paymentOptions') {
                if (!config[key]) config[key] = [];
                config[key].push(value);
            } else {
                config[key] = value;
            }
        }
        
        // Ensure payment options is an array
        if (!config.paymentOptions) {
            config.paymentOptions = [];
        }
        
        // Add timestamp
        config.lastUpdated = new Date().toISOString();
        
        return config;
    }

    showPreview() {
        const config = this.getFormData();
        this.renderPreview(config);
        this.previewSection.classList.remove('hidden');
        this.previewSection.scrollIntoView({ behavior: 'smooth' });
    }

    renderPreview(config) {
        const previewItems = [
            { label: 'Company Name', value: config.companyName || 'Not specified' },
            { label: 'Company Address', value: config.companyAddress || 'Not specified' },
            { label: 'Wallet Address', value: config.walletAddress || 'Not specified', class: 'wallet' },
            { label: 'Payment Options', value: this.renderPaymentBadges(config.paymentOptions), class: 'badges' },
            { label: 'Store Description', value: config.storeDescription || 'Not specified' },
            { label: 'Contact Email', value: config.contactEmail || 'Not specified' }
        ];

        if (config.companyLogo) {
            previewItems.unshift({ label: 'Company Logo', value: `<img src="${config.companyLogo}" style="max-height: 40px; max-width: 150px; object-fit: contain;">` });
        }

        this.previewContent.innerHTML = previewItems.map(item => `
            <div class="preview-item">
                <div class="preview-label">${item.label}:</div>
                <div class="preview-value ${item.class || ''}">${item.value}</div>
            </div>
        `).join('');
    }

    renderPaymentBadges(paymentOptions) {
        if (!paymentOptions || paymentOptions.length === 0) {
            return 'None selected';
        }
        
        return paymentOptions.map(option => `<span class="payment-badge">${option}</span>`).join('');
    }

    saveConfiguration(config) {
        // Save to localStorage
        localStorage.setItem('bytepay-merchant-config', JSON.stringify(config));
        
        // In a real application, you would also send this to a server
        console.log('Configuration saved:', config);
    }

    loadSavedConfiguration() {
        const savedConfig = localStorage.getItem('bytepay-merchant-config');
        if (savedConfig) {
            try {
                const config = JSON.parse(savedConfig);
                this.populateForm(config);
            } catch (error) {
                console.error('Error loading saved configuration:', error);
            }
        }
    }

    populateForm(config) {
        // Populate text inputs and textareas
        Object.keys(config).forEach(key => {
            if (key === 'paymentOptions') return; // Handle separately
            
            const field = document.getElementById(this.camelToKebab(key));
            if (field && field.type !== 'checkbox') {
                field.value = config[key];
                
                // Trigger logo preview if it's the logo field
                if (key === 'companyLogo') {
                    this.updateLogoPreview(config[key]);
                }
            }
        });
        
        // Populate payment options checkboxes
        if (config.paymentOptions) {
            config.paymentOptions.forEach(option => {
                const checkbox = document.querySelector(`input[name="paymentOptions"][value="${option}"]`);
                if (checkbox) {
                    checkbox.checked = true;
                }
            });
        }
    }

    camelToKebab(str) {
        return str.replace(/([a-z0-9]|(?=[A-Z]))([A-Z])/g, '$1-$2').toLowerCase();
    }

    showSuccessModal() {
        this.successModal.classList.remove('hidden');
    }

    closeModal() {
        this.successModal.classList.add('hidden');
    }

    viewCustomerPage() {
        // Create a preview of how the customer page would look with this configuration
        const config = JSON.parse(localStorage.getItem('bytepay-merchant-config'));
        
        // In a real application, this would redirect to the customer page with the merchant's configuration
        alert(`This would redirect to the customer page with your configuration. 
               
Configuration preview:
- Company: ${config.companyName}
- Payments: ${config.paymentOptions.join(', ')}
- Wallet: ${config.walletAddress}`);
    }

    // Utility method to get current configuration
    getCurrentConfiguration() {
        return JSON.parse(localStorage.getItem('bytepay-merchant-config') || '{}');
    }

    // Method to export configuration (for integration with customer page)
    exportConfiguration() {
        const config = this.getCurrentConfiguration();
        return {
            merchantId: this.generateMerchantId(config),
            companyName: config.companyName,
            walletAddress: config.walletAddress,
            paymentOptions: config.paymentOptions,
            companyLogo: config.companyLogo,
            storeDescription: config.storeDescription
        };
    }

    generateMerchantId(config) {
        // Simple hash function for demo purposes
        const str = config.companyName + config.walletAddress;
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return Math.abs(hash).toString(36);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MerchantSetup();
});

// Add some additional styling for dynamic elements
const style = document.createElement('style');
style.textContent = `
    .field-error {
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    input:valid {
        border-color: #28a745 !important;
    }
    
    .checkbox-item:has(input:checked) {
        background: #f0f4ff;
        border-color: #667eea;
    }
    
    .preview-section {
        animation: slideDown 0.5s ease;
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);