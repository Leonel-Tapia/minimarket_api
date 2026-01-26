# app/schemas/user.py

from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="1234")
