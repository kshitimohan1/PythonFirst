from sqlalchemy.orm import Session
import models

# Create a new student
def create_student(db: Session, student_data: dict):
    db_student = models.Student(**student_data)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Get a student by ID
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# Get all students
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

# Update a student
def update_student(db: Session, student_id: int, student_data: dict):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        for key, value in student_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

# Delete a student
def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student