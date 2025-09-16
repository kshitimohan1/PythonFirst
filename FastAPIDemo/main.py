from http import HTTPStatus
from http.client import responses
from random import randrange

from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body

from model import Book

myApp = FastAPI()

# async is optional will be using this if we are performing any async operations
@myApp.get("/")
async def message():
    return {"message " : "Hello Mohan"}

# dict will convert entire JSON body in to dictionary  and will store inside  variable name blogPayload
@myApp.post("/createBlog",status_code= status.HTTP_201_CREATED)
def createBlog(blogPayload: dict = Body(...)):
    print(blogPayload)
    return {
        "message": "Blog created successfully",
        "myPayload": blogPayload
    }

my_Book = [{"bookName": "defaultBook", "rating": 0, "id" : 1}]
@myApp.post("/createBook",status_code = status.HTTP_201_CREATED)
def createBook(new_book: Book): # it actually stores new_book as a pydentic model
    new_book_dict = new_book.dict()
    new_book_dict['id'] = randrange(0,1000)
    my_Book.append(new_book_dict)
    print(new_book)
    print(new_book.dict())      # covert to dictionary
    print(type(new_book.bookName))
    return {
        "message": "Book created successfully",
        "book": my_Book
    }

@myApp.get("/getBooks")
def get_books():
    return {"data": my_Book}


def find_index_book(id):
    for i, b in enumerate(my_Book):
        if b['id'] == id:
            return i
    return None

def findBook(id):
    for b in my_Book:
        if b["id"] == id:
            return b


@myApp.get("/getBooks/{id}")
def get_Books(id : int, response : Response):
    my_Book = findBook(id)
    if not my_Book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"plan with id : {id} was not found")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #    return {'message' : f"post with id : {id} was not found"}
    return {"book_details": my_Book}

@myApp.delete("/deleteBook/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_book(id : int):
    index =  find_index_book(id)
    my_Book.pop(index)
    return {'message': 'books is successfully deleated from your book list'}


@myApp.put("/updateBook/{id}")
def update_book(id : int, book : Book):
    index = find_index_book(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id : {id} was not found")
        #    response.status_code = status.HTTP_404_NOT_FOUND
        #    return {'message' : f"post with id : {id} was not found"}
    my_Book_dict = book.dict()
    my_Book_dict['id'] = id
    my_Book[index]  = my_Book_dict
    return {"data ": my_Book_dict}



my_workout_plan = [{"day": "monday", "workout": "BenchPress", "id" : 1},
                   {"day": "tuesday", "workout": "Barbell Row", "id" : 2},
                   {"day": "wednesday", "workout": "Dumbbell Curl", "id" : 3},
                   {"day": "thursday", "workout": "Shoulder Press", "id" : 4},
                   {"day": "friday", "workout": "Reverse Fly", "id" : 5},
                   {"day": "saturday", "workout": "Hip Thrusts", "id" : 6}]


@myApp.get("/getPlans")
def get_plan():
    return {"data": my_workout_plan}


def find_plan(id):
    for b in my_Book:
        if(b['id']) == id:
            return b

@myApp.get("/getPlans/{id}")
def get_plan(id : int, response : Response):
    plan = find_plan(id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"plan with id : {id} was not found")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #    return {'message' : f"post with id : {id} was not found"}
    return {"plan_details": plan}



