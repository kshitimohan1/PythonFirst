from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql.functions import count

from app.DBConnection import get_db
from app.model import Book as BookModel, Votes  # SQLAlchemy Model
from app.schemas import Book as BookSchema, BookCreate  # Pydantic Models
from app import oauth2
from app.redis_client import set_cache, get_cache, delete_cache

from sqlalchemy import func

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)



@router.post("/createBook", status_code=status.HTTP_201_CREATED, response_model=BookSchema)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_users)
):
    new_book = BookModel(
        **book.dict(),
        owner_id=current_user.id,
        created_at=datetime.utcnow()
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    delete_cache("books:all")

    return new_book



@router.get("/getBooks")
def getBooks(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_users), limit: int =10,skip : int =0,
             use_cache: bool = True):
    ## I want list of all the books irespective of current user so didn't added any check based on logged-in user
    #cache_key = "books:all"
    cache_key = f"books:all:limit:{limit}:skip:{skip}"


    if use_cache:
        cached_data = get_cache(cache_key)
        print("Cached data:", cached_data)
        if cached_data:
            return {"data": cached_data, "source": "redis"}

    books = (
        db.query(BookModel)
        .options(joinedload(BookModel.owner))
        .limit(limit).offset(skip).all()
    )

    ##    books = db.query(BookModel).filter(BookModel.id == current_user.id ).all()
    data = jsonable_encoder(books)

    results = (db.query(BookModel, count(BookModel.id).label("votes")).join(Votes, Votes.book_id == BookModel.id,
                                                                           isouter=True)
               .group_by(BookModel.id).limit(limit).offset(skip).all())

    serialized = []
    for book, votes in results:
        item = jsonable_encoder(book)
        item["votes"] = votes
        serialized.append(item)


    if use_cache:
        print("---- Redis Debug ----")
        print("Using cache:", use_cache)
        print("Saving key:", cache_key)
        print("Saving data:", data)
        set_cache(cache_key, data, expiry_seconds=120)

    ##return {"data": data, "source": "database"}
    return {"data": serialized, "source": "database"}


@router.get("/getBooks/{id}")
def getBook(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_users)):

    cache_key = f"book:{id}"
    cached_data = get_cache(cache_key)

    if cached_data:
        return {"book_details": cached_data, "source": "redis"}

    book = db.query(BookModel).filter(BookModel.id == id).first()
    results= db.query(BookModel).join(Votes,Votes.book_id == BookModel.id,isouter=True).group_by(BookModel.id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    data = jsonable_encoder(book)

    set_cache(cache_key, data, expiry_seconds=120)

    return {"book_details": data, "source": "database"}



@router.put("/updateBook/{id}")
def updateBook(id: int, payload: dict, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_users)):

    book_query = db.query(BookModel).filter(BookModel.id == id)
    book = book_query.first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Prevent client from updating owner_id
    if "owner_id" in payload:
        payload.pop("owner_id")

    if book.owner_id !=current_user.id:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    book_query.update(payload, synchronize_session=False)
    db.commit()

    updated = db.query(BookModel).get(id)
    data = jsonable_encoder(updated)

    delete_cache(f"book:{id}")
    delete_cache("books:all")

    return {"data": data}



@router.delete("/deleteBook/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteBook(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_users)):

    book = db.query(BookModel).filter(BookModel.id == id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.owner_id !=current_user.id:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(book)
    db.commit()

    delete_cache(f"book:{id}")
    delete_cache("books:all")

    return {"message": "Book deleted successfully"}
