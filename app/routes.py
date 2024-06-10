from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import SessionLocal, Account
from .utils import validate_username, validate_password, rate_limit, hash_password, verify_password
from .schemas import AccountCreateRequest, AccountVerifyRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/create_account', status_code=status.HTTP_201_CREATED)
def create_account(request: AccountCreateRequest, db: Session = Depends(get_db)):
    if not validate_username(request.username):
        return {"success": False, "reason": "Invalid username length"}
    if not validate_password(request.password):
        return {"success": False, "reason": "Password does not meet criteria"}

    db_account = db.query(Account).filter(Account.username == request.username).first()
    if db_account:
        return {"success": False, "reason": "Username already exists"}

    hashed_password = hash_password(request.password)
    new_account = Account(username=request.username, password=hashed_password)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return {"success": True, "reason": ""}

@router.post('/verify_account')
def verify_account(request: AccountVerifyRequest, db: Session = Depends(get_db)):
    db_account = db.query(Account).filter(Account.username == request.username).first()
    
    if not db_account:
        return {"success": False, "reason": "Invalid credentials"}

    if rate_limit(db, request.username):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many attempts, try again later")

    if not verify_password(request.password, db_account.password):
        db_account.failed_attempts += 1
        db_account.last_attempt = datetime.utcnow()
        db.commit()
        return {"success": False, "reason": "Password is incorrect"}

    db_account.failed_attempts = 0
    db.commit()
    return {"success": True, "reason": ""}
