from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    # Generate unique payment ID
    payment_id = str(uuid.uuid4())
    return crud.create_payment(db=db, payment=payment, payment_id=payment_id)

@router.get("/merchant/{merchant_id}", response_model=List[schemas.Payment])
def read_merchant_payments(
    merchant_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    payments = crud.get_merchant_payments(db, merchant_id=merchant_id, skip=skip, limit=limit)
    return payments

@router.get("/{payment_id}", response_model=schemas.Payment)
def read_payment(payment_id: str, db: Session = Depends(get_db)):
    db_payment = crud.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.put("/{payment_id}", response_model=schemas.Payment)
def update_payment(payment_id: str, payment: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = crud.update_payment(db, payment_id=payment_id, payment=payment)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get("/{payment_id}/status")
def check_payment_status(payment_id: str, db: Session = Depends(get_db)):
    db_payment = crud.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {
        "payment_id": payment_id,
        "status": db_payment.status,
        "tx_hash": db_payment.tx_hash
    }