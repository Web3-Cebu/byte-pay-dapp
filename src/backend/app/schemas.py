from pydantic import BaseModel, EmailStr, HttpUrl, constr
from typing import List, Optional
from datetime import datetime

# Merchant Schemas
class MerchantBase(BaseModel):
    company_name: str
    company_address: Optional[str] = None
    wallet_address: constr(pattern=r'^0x[a-fA-F0-9]{40}$')
    company_logo: Optional[HttpUrl] = None
    store_description: Optional[str] = None
    contact_email: EmailStr
    payment_options: List[str]

class MerchantCreate(MerchantBase):
    pass

class MerchantUpdate(MerchantBase):
    pass

class Merchant(MerchantBase):
    id: int
    merchant_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Payment Schemas
class PaymentBase(BaseModel):
    amount: float
    currency: str
    customer_wallet: constr(pattern=r'^0x[a-fA-F0-9]{40}$')
    payment_metadata: Optional[dict] = None

class PaymentCreate(PaymentBase):
    merchant_id: str

class PaymentUpdate(BaseModel):
    status: str
    tx_hash: Optional[str] = None

class Payment(PaymentBase):
    id: int
    payment_id: str
    status: str
    tx_hash: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    merchant: Merchant

    class Config:
        from_attributes = True