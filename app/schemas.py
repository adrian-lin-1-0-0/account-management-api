from pydantic import BaseModel

class AccountCreateRequest(BaseModel):
    username: str
    password: str

class AccountVerifyRequest(BaseModel):
    username: str
    password: str
