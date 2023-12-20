"""API Router for /recycle endpoint"""
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.models import RecycledUser

from app.db.conn import get_db
from app.schemas.recycle_user import ItemRecycleUserCreate

router = APIRouter(
    prefix="/recycle",
    tags=["recycle"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_recycle_user(
    item: ItemRecycleUserCreate, db: Session = Depends(get_db)
):
    validate_recycle_user(item, db)
    new_recycled_user = RecycledUser(**item.model_dump())
    db.add(new_recycled_user)
    db.commit()
    db.refresh(new_recycled_user)
    return new_recycled_user

def validate_recycle_user(item: ItemRecycleUserCreate, db: Session):
    """
    Validate the data in the ItemRecycleUserCreate model.

    Raise HTTPException with 422 Unprocessable Entity status code if validation fails.
    """
    # Check if the ID is duplicated in the database
    if item.id is None:
        return
    existing_user = db.query(RecycledUser).filter(RecycledUser.id == item.id).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User with ID {item.id} already exists"
        )
    