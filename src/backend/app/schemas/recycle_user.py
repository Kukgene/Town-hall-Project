"""Schema for recycle user"""
from typing import Optional

from datetime import datetime
from pydantic import BaseModel, field_validator


class ItemRecycleUserBase(BaseModel):
    """
    Shared properties for recycle user

    Table Name: recycled_users
    """

    id: Optional[int] = None
    name: str
    phone_number: str
    bags: int
    created_at: Optional[datetime] = None

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value):
        expected_format = "010-xxxx-xxxx"
        if not value.startswith("010-") or not value[4:].replace("-", "").isdigit():
            raise ValueError(f"Phone number must be in the format '{expected_format}'")
        return value
    
    @field_validator('bags')
    @classmethod
    def validate_bag(cls, value):
        if not 1 <= value <= 3:
            raise ValueError("Number of bags must be between 1 and 3 (inclusive)")
        return value


class ItemRecycleUserCreate(ItemRecycleUserBase):
    """Properties needed to create a recycle user"""


class ItemRecycleUser(ItemRecycleUserBase):
    """Properties of recycle user fetched from db"""
    id: int
    created_at: datetime
    