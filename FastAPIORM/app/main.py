from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session

from app.DBConnection import SessionLocal, engine
from app.model import Book, Base


myApp = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------
# SQLALCHEMY + RAW DICT SECTION  (No Pydantic, direct dict bodies)
# ---------------------------------------------------------------------

@myApp.post("/createBook", status_code=status.HTTP_201_CREATED)
def createBook(payload: dict, db: Session = Depends(get_db)):
    new_book = Book(**payload)
    if new_book.created_at is None:
        new_book.created_at = datetime.utcnow()
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"message": "Book created successfully", "book": new_book.__dict__}


@myApp.get("/getBooks")
def getBooks(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return {"data": [b.__dict__ for b in books]}


@myApp.get("/getBooks/{id}")
def getBook(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book_details": book.__dict__}


@myApp.put("/updateBook/{id}")
def updateBook(id: int, payload: dict, db: Session = Depends(get_db)):
    book_query = db.query(Book).filter(Book.id == id)
    if not book_query.first():
        raise HTTPException(status_code=404, detail="Book not found")
    book_query.update(payload, synchronize_session=False)
    db.commit()
    updated = db.query(Book).get(id)
    data = updated.__dict__
    data.pop("_sa_instance_state", None)
    return {"data": data}


@myApp.delete("/deleteBook/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteBook(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


# ---------------------------------------------------------------------
# PYDANTIC + SQLALCHEMY SECTION  (Cleaner, validated input/output)
# ---------------------------------------------------------------------

# @myApp.post("/pyd_createBook", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
# def createBookPyd(book_req: BookSchema, db: Session = Depends(get_db)):
#     new_book = Book(**book_req.dict(exclude={"id"}))
#     db.add(new_book)
#     db.commit()
#     db.refresh(new_book)
#     return new_book
#
#
# @myApp.get("/pyd_getBooks", response_model=list[BookSchema])
# def getBooksPyd(db: Session = Depends(get_db)):
#     return db.query(Book).all()
#
#
# @myApp.get("/pyd_getBook/{id}", response_model=BookSchema)
# def getBookPyd(id: int, db: Session = Depends(get_db)):
#     book = db.query(Book).filter(Book.id == id).first()
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return book
#
#
# @myApp.put("/pyd_updateBook/{id}", response_model=BookSchema)
# def updateBookPyd(id: int, book_req: BookSchema, db: Session = Depends(get_db)):
#     book_query = db.query(Book).filter(Book.id == id)
#     if not book_query.first():
#         raise HTTPException(status_code=404, detail="Book not found")
#     book_query.update(book_req.dict(exclude={"id"}), synchronize_session=False)
#     db.commit()
#     return db.query(Book).get(id)
#
#
# @myApp.delete("/pyd_deleteBook/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def deleteBookPyd(id: int, db: Session = Depends(get_db)):
#     book = db.query(Book).filter(Book.id == id).first()
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
#     db.delete(book)
#     db.commit()
#     return {"message": "Book deleted"}
