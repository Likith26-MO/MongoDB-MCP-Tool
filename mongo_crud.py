# mongo_crud.py
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client["classroom"]
col = db["students"]

def insert_student(doc):
    """Insert a new student with student_id as the primary key"""
    try:
        # Validate required fields
        required_fields = ["student_id", "first_name", "last_name", "age"]
        for field in required_fields:
            if field not in doc:
                raise ValueError(f"Missing required field: {field}")

        # Check if student_id already exists
        if col.find_one({"student_id": doc["student_id"]}):
            raise ValueError(f"Student ID {doc['student_id']} already exists")

        # Ensure scores is a dictionary
        if "scores" not in doc:
            doc["scores"] = {}
        
        # Ensure active field exists
        if "active" not in doc:
            doc["active"] = True

        # Insert the document
        result = col.insert_one(doc)
        
        # Return the student_id instead of ObjectId
        return doc["student_id"]
    except Exception as e:
        print(f"Error inserting student: {e}")
        raise ValueError(f"Failed to insert student: {str(e)}")

def get_student_by_id(student_id):
    """Get student by student_id instead of ObjectId"""
    try:
        return col.find_one({"student_id": student_id})
    except Exception as e:
        print(f"Error fetching student: {e}")
        return None

def list_students(limit=50, skip=0):
    """List students with optional pagination"""
    return list(col.find().sort("student_id", 1).skip(skip).limit(limit))

def update_student_by_id(student_id, update_fields):
    """Update student by student_id"""
    # Remove student_id from update fields if present
    if "student_id" in update_fields:
        del update_fields["student_id"]
    
    return col.update_one(
        {"student_id": student_id}, 
        {"$set": update_fields}
    )

def delete_student_by_id(student_id):
    """Delete student by student_id"""
    return col.delete_one({"student_id": student_id})

# Helper function to create indexes (run once)
def setup_indexes():
    """Create necessary indexes"""
    col.create_index("student_id", unique=True)

# Example usage:
if __name__ == "__main__":
    # Setup indexes
    setup_indexes()
    
    # Example student data
    sample_student = {
        "student_id": "S999",
        "first_name": "Test",
        "last_name": "User",
        "age": 22,
        "scores": {
            "math": 85,
            "cs": 90,
            "db": 88
        },
        "active": True
    }
    
    # Insert example
    try:
        _id = insert_student(sample_student)
        print(f"Inserted student with ID: {_id}")
    except ValueError as e:
        print(f"Insert error: {e}")
    
    # Query example
    student = get_student_by_id("S999")
    if student:
        print(f"Found student: {student['first_name']} {student['last_name']}")
    
    # Update example
    update_result = update_student_by_id("S999", {
        "age": 23,
        "scores.math": 95
    })
    print(f"Updated {update_result.modified_count} student(s)")
    
    # Delete example
    delete_result = delete_student_by_id("S999")
    print(f"Deleted {delete_result.deleted_count} student(s)")
