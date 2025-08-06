from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String, unique=True, index=True)
    company_name = Column(String, index=True)
    company_address = Column(String, nullable=True)
    wallet_address = Column(String)
    company_logo = Column(String, nullable=True)
    store_description = Column(String, nullable=True)
    contact_email = Column(String)
    payment_options = Column(JSON)  # List of accepted cryptocurrencies
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationship with payments
    payments = relationship("Payment", back_populates="merchant")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(String, unique=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    amount = Column(Float)
    currency = Column(String)  # ETH, USDT, LSK
    status = Column(String)  # pending, completed, failed
    tx_hash = Column(String, nullable=True)  # Blockchain transaction hash
    customer_wallet = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    payment_metadata = Column(JSON, nullable=True)  # Additional payment metadata
    
    # Relationship with merchant
    merchant = relationship("Merchant", back_populates="payments")