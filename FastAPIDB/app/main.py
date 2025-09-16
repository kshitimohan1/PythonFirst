from app.DBConnection import get_connection
from app.model import Book
from fastapi import FastAPI, status, HTTPException, Response
from datetime import datetime

myApp = FastAPI()


conn = get_connection()
cursor = conn.cursor()

def create_table():
    create_query = """
    CREATE TABLE IF NOT EXISTS "Book" (
        id SERIAL PRIMARY KEY,
        bookName VARCHAR(255) NOT NULL,
        rating INTEGER,
        published BOOLEAN DEFAULT FALSE,
        publishedYear INTEGER,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    cursor.execute(create_query)
    # No need conn.commit() if autocommit=True
    print("Table 'Book' checked/created.")

create_table()

@myApp.post("/createBook", status_code=status.HTTP_201_CREATED)
def createBook(new_book: Book):
    if new_book.created_at is None:
        new_book.created_at = datetime.utcnow()

    cursor.execute(
        """INSERT INTO "Book" (bookName, rating, published, publishedYear, created_at)
           VALUES (%s, %s, %s, %s, %s)
           RETURNING *
        """,
        (
            new_book.bookName,
            new_book.rating,
            new_book.isPublished,
            new_book.publishedYear,
            new_book.created_at
        )
    )
    return {
        "message": "Book created successfully",
        "book": new_book
    }


# GET endpoint
@myApp.get("/getBooks")
def getBooks():
    cursor.execute('SELECT * FROM "Book"')
    rows = cursor.fetchall()
    return {"data": rows}



@myApp.get("/getBooks/{id}")
def get_Books(id : int, response : Response):
    cursor.execute("""Select * from "Book" where id = %s """,(str(id),))
    #(id) Just the value id, same as id whereas (id,) A tuple with one element
    my_Book = cursor.fetchone()
    if not my_Book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id : {id} was not found")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #    return {'message' : f"post with id : {id} was not found"}
    return {"book_details": my_Book}





@myApp.delete("/deleteBook/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_book(id : int):
    cursor.execute("""Delete from "Book" where id = %s returning *""", (str(id),))
    deleated_post =cursor.fetchone()
    if deleated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id : {id} was not found or being deleted")
    return {'message': 'books is successfully deleated from your book list'}








@myApp.put("/updateBook/{id}", status_code=status.HTTP_200_OK)
def update_book(id: int, book: Book):
    cursor.execute(
        """
        UPDATE "Book"
        SET bookName = %s, rating = %s, published = %s, publishedYear = %s
        WHERE id = %s
        RETURNING *
        """,
        (
            book.bookName,
            book.rating,
            book.isPublished,
            book.publishedYear,
            str(id)
        )
    )
    updated_book = cursor.fetchone()
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
    return {"data": updated_book}

