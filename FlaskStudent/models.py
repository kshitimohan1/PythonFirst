from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)  # String(50) for MySQL compatibility
    age = Column(Integer)
    grade = Column(String(10))