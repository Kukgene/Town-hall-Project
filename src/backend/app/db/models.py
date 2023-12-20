"""Schema in Database"""
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import VARCHAR, TIMESTAMP, INTEGER
from sqlalchemy.sql import func


from .conn import Base


class RecycledUser(Base):
    """Schema for RecycledUser in Database"""

    __tablename__ = "recycle_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR(50))
    phone_number = Column(VARCHAR())
    bags = Column(Integer)
    # pylint: disable-next=not-callable
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
