"""API Router for /recycle endpoint"""
from fastapi import APIRouter, Depends, status
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
    """Handle POST /recycle

    TODO
    1. Receive item endpoint
    2. Validate if there is no error on the data
    3. Return created user after creation

    HttpException:
    422 Error => If id is duplicated

    REFERENCE
    https://fastapi.tiangolo.com/tutorial/sql-databases/

    Use with RecycledUser Class
    """
