from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = "Book"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bookName = Column(String(100), nullable=False)
    rating = Column(Float, nullable=True, default=None)
    isPublished = Column(Boolean, default=False)
    publishedYear = Column(Integer, nullable=True, default=None)
    created_at = Column(DateTime, nullable=True)
    owner_id = Column(Integer,ForeignKey("Users.id", ondelete="CASCADE"),nullable=False)      ## DataType must be what data type Users have for ID since it is a foreign key
    owner = relationship("User")    ## Here will refer actual SQLAlchemy class instead of table

class User(Base):
    __tablename__ = "Users"

    email = Column(String, nullable=False, unique=True)
    password= Column(String ,nullable=False)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
