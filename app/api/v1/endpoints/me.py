from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import User
from app.db.session import get_db
from app.api.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=User)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user