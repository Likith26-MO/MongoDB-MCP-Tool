# mongo_mcp_tool.py
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Dict, Optional

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["student"]
col = db["students"]

app = FastAPI(title="MongoDB MCP Tool", version="1.0")

# Data model
class Student(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    age: int
    scores: Dict[str, int]
    active: Optional[bool] = True


# ---------- CRUD ENDPOINTS ----------

@app.get("/")
def home():
    return {"message": "MongoDB MCP Tool is running!"}


# CREATE
@app.post("/students")
def create_student(student: Student):
    result = col.insert_one(student.dict())
    return {"inserted_id": str(result.inserted_id)}


# READ ALL
@app.get("/students")
def get_students(limit: int = 10, skip: int = 0):
    docs = list(col.find().skip(skip).limit(limit))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


# READ ONE
@app.get("/students/{student_id}")
def get_student(student_id: str):
    student = col.find_one({"student_id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student["_id"] = str(student["_id"])
    return student


# UPDATE
@app.put("/students/{student_id}")
def update_student(student_id: str, update_data: dict):
    result = col.update_one({"student_id": student_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}


# DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    result = col.delete_one({"student_id": student_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


# ---------- MCP DISCOVERY ENDPOINT ----------

@app.get("/mcp")
def mcp_discover():
    """
    This endpoint describes available tools for MCP clients like LangGraph.
    """
    return {
        "tools": [
            {"name": "create_student", "route": "/students", "method": "POST"},
            {"name": "get_students", "route": "/students", "method": "GET"},
            {"name": "get_student", "route": "/students/{student_id}", "method": "GET"},
            {"name": "update_student", "route": "/students/{student_id}", "method": "PUT"},
            {"name": "delete_student", "route": "/students/{student_id}", "method": "DELETE"},
        ]
    }
