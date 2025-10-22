# populate_mongo.py
from mongo_crud import insert_student

for i in range(1, 151):
    doc = {
        "student_id": f"S{i:03}",
        "first_name": f"First{i}",
        "last_name": f"Last{i}",
        "age": 18 + i % 5,
        "scores": {"math": 60 + i % 40, "cs": 55 + i % 45, "db": 50 + i % 50},
        "active": True
    }
    insert_student(doc)

print("Inserted 150 sample student records.")
