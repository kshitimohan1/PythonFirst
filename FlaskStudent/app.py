"""
 Problem with this is for every API we need to add in swagger.json
from flask import Flask, request, jsonify, make_response
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, crud
from flask_swagger_ui import get_swaggerui_blueprint

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Initialize Flask app
app = Flask(__name__, static_folder="static")

# Setup Swagger UI
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "My Flask API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Standard response format
def create_response(data, status_code=200, message="Success"):
    response_data = {
        "status": "success" if status_code // 100 == 2 else "error",
        "message": message,
        "data": data
    }
    return make_response(jsonify(response_data), status_code)

# Create a new student
@app.route("/students/", methods=["POST"])
def create_student():
    with SessionLocal() as db:
        student_data = request.json
        student = crud.create_student(db, student_data)
        return create_response(
            {"id": student.id, "name": student.name, "age": student.age, "grade": student.grade},
            status_code=201,
            message="Student created successfully"
        )

# Get a student by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def read_student(student_id: int):
    with SessionLocal() as db:
        student = crud.get_student(db, student_id)
        if not student:
            return create_response(None, status_code=404, message="Student not found")
        return create_response(
            {"id": student.id, "name": student.name, "age": student.age, "grade": student.grade},
            status_code=200,
            message="Student retrieved successfully"
        )

# Get all students
@app.route("/students/", methods=["GET"])
def read_students():
    with SessionLocal() as db:
        students = crud.get_students(db)
        student_list = [{"id": s.id, "name": s.name, "age": s.age, "grade": s.grade} for s in students]
        return create_response(student_list, status_code=200, message="Students retrieved successfully")

# Update a student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id: int):
    with SessionLocal() as db:
        student_data = request.json
        student = crud.update_student(db, student_id, student_data)
        if not student:
            return create_response(None, status_code=404, message="Student not found")
        return create_response(
            {"id": student.id, "name": student.name, "age": student.age, "grade": student.grade},
            status_code=200,
            message="Student updated successfully"
        )

# Delete a student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id: int):
    with SessionLocal() as db:
        student = crud.delete_student(db, student_id)
        if not student:
            return create_response(None, status_code=404, message="Student not found")
        return create_response(None, status_code=200, message="Student deleted successfully")

# Run the application
if __name__ == "__main__":
    app.run(debug=True, port=8001)
"""


from flask import Flask
from flask_restx import Api, Resource, fields
from database import engine, SessionLocal
import models, crud

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize Flask app
app = Flask(__name__)
api = Api(app, version="1.0", title="Student API", description="API for managing students")

# Define API Namespace
ns = api.namespace("students", description="Student operations")

# Define Student Model (Auto-Docs in Swagger)
student_model = api.model(
    "Student",
    {
        "id": fields.Integer(readOnly=True, description="The student unique identifier"),
        "name": fields.String(required=True, description="Student's name"),
        "age": fields.Integer(required=True, description="Student's age"),
        "grade": fields.String(required=True, description="Student's grade"),
    },
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@ns.route("/")
class StudentList(Resource):
    @ns.doc("list_students")
    @ns.marshal_list_with(student_model)
    def get(self):
        """Retrieve all students"""
        db = next(get_db())
        return crud.get_students(db)

    @ns.doc("create_student")
    @ns.expect(student_model)  # Auto-generates request body in Swagger
    @ns.marshal_with(student_model, code=201)  # Auto-generates response model
    def post(self):
        """Create a new student"""
        db = next(get_db())
        student_data = api.payload
        student = crud.create_student(db, student_data)
        return student, 201


@ns.route("/<int:student_id>")
@ns.response(404, "Student not found")
@ns.param("student_id", "The student identifier")
class Student(Resource):
    @ns.doc("get_student")
    @ns.marshal_with(student_model)
    def get(self, student_id):
        """Retrieve a student by ID"""
        db = next(get_db())
        student = crud.get_student(db, student_id)
        if not student:
            api.abort(404, "Student not found")
        return student

    @ns.doc("update_student")
    @ns.expect(student_model)
    @ns.marshal_with(student_model)
    def put(self, student_id):
        """Update a student"""
        db = next(get_db())
        student_data = api.payload
        student = crud.update_student(db, student_id, student_data)
        if not student:
            api.abort(404, "Student not found")
        return student

    @ns.doc("delete_student")
    def delete(self, student_id):
        """Delete a student"""
        db = next(get_db())
        student = crud.delete_student(db, student_id)
        if not student:
            api.abort(404, "Student not found")
        return {"message": "Student deleted successfully"}, 200


# Register Namespace
api.add_namespace(ns)

if __name__ == "__main__":
    app.run(debug=True, port=8001)
