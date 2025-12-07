from fastapi import FastAPI

from app import oauth2
from app.DBConnection import  engine
from app.model import  Base
from routers import book, user, auth, vote
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
print(settings.secret_key)

myApp = FastAPI()
Base.metadata.create_all(bind=engine)

origins =[]
myApp.add_middleware(
    CORSMiddleware,
    allow_origin=[origins],
    allow_credentials=True,
    allow_headers= ["*"],
    allow_methods=["*"]
)

myApp.include_router(book.router)
myApp.include_router(user.router)
myApp.include_router(auth.router)
myApp.include_router(vote.router)
