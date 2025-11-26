from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import UserLogin, Token
from app.model import User
from app.DBConnection import get_db
from app import utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with email '{user_credentials.username}' is invalid"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = oauth2.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
