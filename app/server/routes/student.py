from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import AsyncMongoConnect
from server.models.student import (
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel
)

router = APIRouter()

@router.post("/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    mg = AsyncMongoConnect(database="school")
    student = jsonable_encoder(student)
    new_student = await mg.add_student(
        table_name="students", 
        student_data=student
    )
    return ResponseModel(new_student, "Student added successfully.")

@router.get("/{id}", description="get a student")
async def get_student(id):
    mg = AsyncMongoConnect(database="school")
    student = await mg.retrieve_student("students", id=id)
    print(student)
    return ResponseModel(student, "Get student sucessfully")

@router.get("/", description="get all students")
async def get_student():
    mg = AsyncMongoConnect(database="school")
    students = await mg.retrieve_students("students")
    print(students)
    return ResponseModel(students, "Get all students sucessfully")

@router.put("/{id}")
async def update_student_data(id: str, req: UpdateStudentModel=Body(...)):
    mg = AsyncMongoConnect(database='school')
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req)
    updated_student = await mg.update_student(id, 'students', req)

    if updated_student:
        return ResponseModel(
            "Student with ID: {} name update is successful".format(id),
            "Student name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )

@router.delete("/{id}", description='Delete follow _id')
async def delete_a_student(id: str):
    mg = AsyncMongoConnect(database='school')
    result = await mg.delete_student('students', id)

    if result:
        return ResponseModel(
            f"Student with ID: {id} was deleted",
            "Delete student sucessfully!!"
        )
    
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )
    