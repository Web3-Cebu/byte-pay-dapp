from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Merchant)
def create_merchant(merchant: schemas.MerchantCreate, db: Session = Depends(get_db)):
    # Generate unique merchant ID
    merchant_id = str(uuid.uuid4())
    return crud.create_merchant(db=db, merchant=merchant, merchant_id=merchant_id)

@router.get("/", response_model=List[schemas.Merchant])
def read_merchants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    merchants = crud.get_merchants(db, skip=skip, limit=limit)
    return merchants

@router.get("/{merchant_id}", response_model=schemas.Merchant)
def read_merchant(merchant_id: str, db: Session = Depends(get_db)):
    db_merchant = crud.get_merchant(db, merchant_id=merchant_id)
    if db_merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return db_merchant

@router.put("/{merchant_id}", response_model=schemas.Merchant)
def update_merchant(merchant_id: str, merchant: schemas.MerchantUpdate, db: Session = Depends(get_db)):
    db_merchant = crud.update_merchant(db, merchant_id=merchant_id, merchant=merchant)
    if db_merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return db_merchant

@router.delete("/{merchant_id}")
def delete_merchant(merchant_id: str, db: Session = Depends(get_db)):
    success = crud.delete_merchant(db, merchant_id=merchant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return {"status": "success", "message": "Merchant deleted"}