from multiprocessing.sharedctypes import synchronized
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from fastapi.encoders import jsonable_encoder

from app.DBConnection import get_db
from app.model import Votes, Book
from app.schemas import Book as BookSchema, BookCreate, Vote  # Pydantic Models
from app import oauth2
from app.redis_client import set_cache, get_cache, delete_cache

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def votes(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_users)):


    book = db.query(Book).filter(Book.id == vote.book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Book with id {vote.book_id} doesn't exist ")

    vote_query = db.query(Votes).filter(Votes.book_id == vote.book_id, Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"User {current_user.id} has already votes for book {vote.book_id}")
        new_vote =Votes(book_id = vote.book_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote "}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session = False)
        db.commit()
        return {"message": "Successfully added vote "}




