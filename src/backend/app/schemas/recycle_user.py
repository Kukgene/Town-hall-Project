"""Schema for recycle user"""
from typing import Optional

from datetime import datetime
from pydantic import BaseModel


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

    """
    TODO
    Define validators here
    Reference: https://docs.pydantic.dev/2.5/api/functional_validators/
    """


class ItemRecycleUserCreate(ItemRecycleUserBase):
    """Properties needed to create a recycle user"""


class ItemRecycleUser(ItemRecycleUserBase):
    """Properties of recycle user fetched from db"""

    # TODO: Overrides id and created_at as required
