from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.crud.user import create_user, authenticate_user
from app.db.session import get_db
from app.core.security import create_access_token

router = APIRouter()


@router.post("/register", response_description="Success registration")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        create_user(db, user)
        return {"message": "Success registration"}
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
