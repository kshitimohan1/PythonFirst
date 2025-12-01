from fastapi.params import Depends
from jose import JWTError, jwt
from datetime import  datetime,timedelta
from fastapi import HTTPException, status
from pydantic.v1.schema import schema

from fastapi.security import  OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from app import model
from app.DBConnection import get_db
from app.config import settings
from app.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

Secret_Key= settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRES_MINUTES= settings.access_token_expires_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expires= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expires})
    emcode_jwt =jwt.encode(to_encode,Secret_Key, algorithm=ALGORITHM)
    return emcode_jwt



def verify_access_token(token: str, credentials_exceptions):
    try:
        payload =jwt.decode(token,Secret_Key,algorithms=[ALGORITHM])
        user_id : str = payload.get("user_id")
        if user_id is None:
            raise credentials_exceptions
        token_data = TokenData(id = str(user_id))
    except JWTError:
        raise credentials_exceptions
    return token_data

def get_current_users(token : str = Depends(oauth2_scheme), db: Session =Depends(get_db)):
    credentials_exceptions = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail =f"Could not validate credentials",
                                           headers = {"www-authenticate" : "Bearer"})
    token = verify_access_token(token,credentials_exceptions)
    user = db.query(model.User).filter(model.User.id == token.id).first()
    return user