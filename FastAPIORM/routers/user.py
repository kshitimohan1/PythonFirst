from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import model, utils, oauth2
from app.DBConnection import SessionLocal, engine, get_db
from app.model import Base
from app.schemas import UserCreate, UserResp
from app.redis_client import set_cache, get_cache, delete_cache

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/createUser", status_code=status.HTTP_201_CREATED, response_model=UserResp)
def createUsers(user: UserCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_users)):

    # password hashing
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass

    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # cache invalidation
    delete_cache("users_list")

    return new_user


@router.get("/getUser/{id}", status_code=status.HTTP_200_OK, response_model=UserResp)
def getUser(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_users)):

    cache_key = f"user_{id}"

    # Check cache
    cached_user = get_cache(cache_key)
    if cached_user:
        return cached_user  # already a dict

    # Fetch from DB
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist")

    # Save in cache
    user_dict = user.__dict__.copy()
    user_dict.pop("_sa_instance_state", None)

    set_cache(cache_key, user_dict, expiry_seconds=120)

    return user_dict

@router.get("/getUsers", status_code=status.HTTP_200_OK, response_model=List[UserResp])
def get_all_users(db: Session = Depends(get_db)):

    cache_key = "users_list"

    # Try Redis
    cached_users = get_cache(cache_key)
    if cached_users:
        return cached_users

    # Query DB
    users = db.query(model.User).all()
    result = []

    for u in users:
        data = u.__dict__.copy()
        data.pop("_sa_instance_state", None)
        result.append(data)

    # Save to Redis
    set_cache(cache_key, result, expiry_seconds=120)

    return result
