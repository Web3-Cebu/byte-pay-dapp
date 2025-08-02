from sqlalchemy.orm import Session
from . import models, schemas

# Merchant CRUD operations
def get_merchant(db: Session, merchant_id: str):
    return db.query(models.Merchant).filter(models.Merchant.merchant_id == merchant_id).first()

def get_merchants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Merchant).offset(skip).limit(limit).all()

def create_merchant(db: Session, merchant: schemas.MerchantCreate, merchant_id: str):
    db_merchant = models.Merchant(
        merchant_id=merchant_id,
        **merchant.model_dump()
    )
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant

def update_merchant(db: Session, merchant_id: str, merchant: schemas.MerchantUpdate):
    db_merchant = get_merchant(db, merchant_id=merchant_id)
    if not db_merchant:
        return None
    
    for key, value in merchant.model_dump().items():
        setattr(db_merchant, key, value)
    
    db.commit()
    db.refresh(db_merchant)
    return db_merchant

def delete_merchant(db: Session, merchant_id: str):
    db_merchant = get_merchant(db, merchant_id=merchant_id)
    if not db_merchant:
        return False
    
    db.delete(db_merchant)
    db.commit()
    return True

# Payment CRUD operations
def get_payment(db: Session, payment_id: str):
    return db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()

def get_merchant_payments(db: Session, merchant_id: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Payment)
        .join(models.Merchant)
        .filter(models.Merchant.merchant_id == merchant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_payment(db: Session, payment: schemas.PaymentCreate, payment_id: str):
    # Get merchant
    db_merchant = db.query(models.Merchant).filter(
        models.Merchant.merchant_id == payment.merchant_id
    ).first()
    
    if not db_merchant:
        raise ValueError("Merchant not found")
    
    # Create payment
    db_payment = models.Payment(
        payment_id=payment_id,
        merchant_id=db_merchant.id,
        status="pending",
        **payment.model_dump(exclude={'merchant_id'})
    )
    
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_payment(db: Session, payment_id: str, payment: schemas.PaymentUpdate):
    db_payment = get_payment(db, payment_id=payment_id)
    if not db_payment:
        return None
    
    for key, value in payment.model_dump().items():
        setattr(db_payment, key, value)
    
    db.commit()
    db.refresh(db_payment)
    return db_payment