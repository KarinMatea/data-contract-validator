from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserContract(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=18)