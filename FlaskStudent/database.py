from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL database URL (Replace with your MySQL details)
DATABASE_URL = "mysql+pymysql://bssuser:Bssuser%40123@localhost/student_db"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()