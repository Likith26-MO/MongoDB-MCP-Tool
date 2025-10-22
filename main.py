# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import mongo_crud

app = FastAPI(title="MongoDB MCP + CRUD Tool")

# ---------------- CRUD ----------------
class StudentIn(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    age: int
    scores: Dict[str,int]
    active: Optional[bool] = True

@app.post("/students")
async def create_student(s: StudentIn):
    try:
        student_id = mongo_crud.insert_student(s.dict())
        return {"inserted_id": student_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students")
def get_students(limit: int = 50, skip: int = 0):
    docs = mongo_crud.list_students(limit=limit, skip=skip)
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

@app.get("/students/{id}")
def get_student(id: str):
    doc = mongo_crud.get_student_by_id(id)
    if not doc:
        return {"detail": "Not found"}
    doc["_id"] = str(doc["_id"])
    return doc

@app.patch("/students/{id}")
def patch_student(id: str, update: dict):
    res = mongo_crud.update_student_by_id(id, update)
    return {"matched": res.matched_count, "modified": res.modified_count}

@app.delete("/students/{id}")
def remove_student(id: str):
    res = mongo_crud.delete_student_by_id(id)
    return {"deleted": res.deleted_count}

# ---------------- MCP ----------------
@app.get("/mcp")
def mcp_discover():
    return {
        "tools": [
            {
                "name": "list_students",
                "description": "Get a list of students",
                "route": "/students",
                "method": "GET",
                "inputs": {"limit": "int", "skip": "int"},
                "outputs": "list of student objects"
            },
            {
                "name": "create_student",
                "description": "Insert a new student record",
                "route": "/students",
                "method": "POST",
                "inputs": {"student_id": "str", "first_name": "str", "last_name": "str", "age": "int", "scores": "dict", "active": "bool"},
                "outputs": "inserted_id"
            }
        ]
    }
