import re
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from .models import Account

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_username(username):
    return 3 <= len(username) <= 32

def validate_password(password):
    if len(password) < 8 or len(password) > 32:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)

def rate_limit(db: Session, username: str) -> bool:
    account = db.query(Account).filter(Account.username == username).first()
    if not account:
        return False

    now = datetime.now()
    if account.failed_attempts >= 5 and (now - account.last_attempt) < timedelta(minutes=1):
        return True
    if (now - account.last_attempt) >= timedelta(minutes=1):
        account.failed_attempts = 0
        db.commit()
    return False
