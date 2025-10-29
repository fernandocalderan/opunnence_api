from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ContactSubmissionBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = None
    message: Optional[str] = None


class ContactSubmissionCreate(ContactSubmissionBase):
    pass


class ContactSubmissionResponse(ContactSubmissionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
