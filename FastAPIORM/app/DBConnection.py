from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import sessionmaker

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SQLAlchemy_DB_URL = 'postgresql://postgres:Aqadmin%40123@localhost/fastapi'
engine = create_engine(SQLAlchemy_DB_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()


