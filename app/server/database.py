import json
import uuid
from datetime import datetime, timedelta
from pprint import pprint
from typing import Dict, List

import motor.motor_asyncio
from bson import ObjectId
from configs import (
    MONGO_URL
)

print(MONGO_URL)
class AsyncMongoConnect:
    def __init__(self, database):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        self.db = self.client[database]

    @staticmethod
    def student_helper(student) -> dict:
        return {
            "id": str(student["_id"]),
            "fullname": student["fullname"],
            "email": student["email"],
            "course_of_study": student["course_of_study"],
            "year": student["year"],
            "GPA": student["gpa"],
        }
    
    async def retrieve_students(self, table_name: str):
        collection = self.db[table_name]
        students = []

        async for student in collection.find():
            students.append(
                self.student_helper(student)
            )
        
        return students
    
    async def retrieve_student(self, table_name: str, id: str) -> dict:
        collection = self.db[table_name]
        student = await collection.find_one({"_id": ObjectId(id)})
        if student:
            return self.student_helper(student=student)
    
    async def add_student(self, table_name: str, student_data: dict) -> dict:
        collection = self.db[table_name]
        student = await collection.insert_one(student_data)
        return {"_id": str(student.inserted_id)}
    
    # Update a student with a matching ID
    async def update_student(self, id: str, table_name: str,  data: dict):
        # Return false if an empty request body is sent.
        collection = self.db[table_name]
        if len(data) < 1:
            return False
        student = await collection.find_one({"_id": ObjectId(id)})
        if student:
            updated_student = await collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            if updated_student:
                return True
            return False
    
    async def delete_student(self, table_name: str, id: str):
        collection = self.db[table_name]
        student = collection.find({'_id': ObjectId(id)})
        if student:
            await collection.delete_one({'_id': ObjectId(id)})
            return True
        return False

