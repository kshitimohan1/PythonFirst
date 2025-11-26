from fastapi import FastAPI

from app import oauth2
from app.DBConnection import  engine
from app.model import  Base
from routers import book, user, auth
from app.config import settings

print(settings.secret_key)

myApp = FastAPI()
Base.metadata.create_all(bind=engine)

myApp.include_router(book.router)
myApp.include_router(user.router)
myApp.include_router(auth.router)
