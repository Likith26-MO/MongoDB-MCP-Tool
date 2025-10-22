# api_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson.objectid import ObjectId
from typing import Optional, Dict, Any
import mongo_crud

app = FastAPI()

class StudentIn(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    age: int
    scores: Dict[str,int]
    active: Optional[bool] = True

@app.post("/students")
def create_student(s: StudentIn):
    _id = mongo_crud.insert_student(s.dict())
    return {"inserted_id": str(_id)}

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
        raise HTTPException(status_code=404, detail="Not found")
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
