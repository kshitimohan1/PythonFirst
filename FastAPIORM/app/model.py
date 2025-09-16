from sqlalchemy import Column, Integer, String, Boolean, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "Book"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bookName = Column(String(100), nullable=False)
    rating = Column(Float, nullable=True, default=None)
    isPublished = Column(Boolean, default=False)
    publishedYear = Column(Integer, nullable=True, default=None)
    created_at = Column(DateTime, nullable=True)


class User(Base):
    __tablename__ = "Users"

    email = Column(String, nullable=False, unique=True)
    password= Column(String ,nullable=False)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
