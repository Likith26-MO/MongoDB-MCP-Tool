# mcp.py
from fastapi import APIRouter
import streamlit as st
import requests
import json
import pandas as pd

# Keep existing FastAPI router
mcp_router = APIRouter()

@mcp_router.get("/mcp")
def mcp_discover():
    """
    Returns the MCP tool description.
    Clients like LangGraph can use this to discover available actions.
    """
    return {
        "tools": [
            {
                "name": "list_students",
                "description": "Get a list of students with optional pagination",
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
            },
            # Add update/delete descriptions similarly
        ]
    }

# Add Streamlit interface
def streamlit_app():
    st.title("MongoDB Control Panel (MCP)")
    
    # Sidebar for operations
    operation = st.sidebar.selectbox(
        "Select Operation",
        ["List Students", "Create Student", "Search Student", "Update Student", "Delete Student"]
    )
    
    if operation == "List Students":
        st.header("Student List")
        limit = st.slider("Number of students to show", 1, 50, 10)
        skip = st.number_input("Skip records", 0)
        
        if st.button("Fetch Students"):
            response = requests.get(f"http://localhost:8000/students?limit={limit}&skip={skip}")
            if response.status_code == 200:
                students = response.json()
                df = pd.DataFrame(students)
                st.dataframe(df)
            else:
                st.error("Failed to fetch students")
    
    elif operation == "Create Student":
        st.header("Create New Student")
        with st.form("create_student"):
            student_id = st.text_input("Student ID")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            age = st.number_input("Age", 1, 100)
            
            st.subheader("Scores")
            math_score = st.number_input("Math Score", 0, 100)
            cs_score = st.number_input("CS Score", 0, 100)
            db_score = st.number_input("DB Score", 0, 100)
            
            active = st.checkbox("Active", True)
            submitted = st.form_submit_button("Create")
            
            if submitted:
                if not student_id or not first_name or not last_name:
                    st.error("Please fill all required fields!")
                else:
                    student_data = {
                        "student_id": student_id,
                        "first_name": first_name,
                        "last_name": last_name,
                        "age": int(age),
                        "scores": {
                            "math": int(math_score),
                            "cs": int(cs_score),
                            "db": int(db_score)
                        },
                        "active": active
                    }
                    
                    try:
                        response = requests.post(
                            "http://localhost:8000/students",
                            json=student_data,
                            headers={"Content-Type": "application/json"}
                        )
                        
                        if response.status_code == 200:
                            st.success(f"Student {student_id} created successfully!")
                            st.json(response.json())
                        else:
                            st.error(f"Failed to create student: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to server: {e}")

    elif operation == "Search Student":
        st.header("Search Student")
        student_id = st.text_input("Enter Student ID")
        
        if st.button("Search"):
            response = requests.get(f"http://localhost:8000/students/{student_id}")
            if response.status_code == 200:
                student = response.json()
                st.json(student)
            else:
                st.error("Student not found")
    
    elif operation == "Update Student":
        st.header("Update Student")
        student_id = st.text_input("Enter Student ID")
        
        if student_id:
            response = requests.get(f"http://localhost:8000/students/{student_id}")
            if response.status_code == 200:
                student = response.json()
                with st.form("update_student"):
                    new_first_name = st.text_input("First Name", student["first_name"])
                    new_last_name = st.text_input("Last Name", student["last_name"])
                    new_age = st.number_input("Age", 1, 100, student["age"])
                    new_math = st.number_input("Math Score", 0, 100, student["scores"]["math"])
                    new_cs = st.number_input("CS Score", 0, 100, student["scores"]["cs"])
                    new_db = st.number_input("DB Score", 0, 100, student["scores"]["db"])
                    
                    if st.form_submit_button("Update"):
                        update_data = {
                            "first_name": new_first_name,
                            "last_name": new_last_name,
                            "age": new_age,
                            "scores": {
                                "math": new_math,
                                "cs": new_cs,
                                "db": new_db
                            }
                        }
                        
                        response = requests.patch(
                            f"http://localhost:8000/students/{student_id}",
                            json=update_data
                        )
                        
                        if response.status_code == 200:
                            st.success("Student updated successfully!")
                        else:
                            st.error("Failed to update student")
            else:
                st.error("Student not found")
    
    elif operation == "Delete Student":
        st.header("Delete Student")
        student_id = st.text_input("Enter Student ID")
        
        # First check if student exists
        if student_id:
            check_response = requests.get(f"http://localhost:8000/students/{student_id}")
            if check_response.status_code == 200:
                student = check_response.json()
                st.write(f"Found student: {student['first_name']} {student['last_name']}")
                st.warning("⚠️ This action cannot be undone!")
                
                confirm = st.checkbox("I understand and want to delete this student")
                if confirm and st.button("Delete Student"):
                    try:
                        response = requests.delete(f"http://localhost:8000/students/{student_id}")
                        if response.status_code == 200:
                            st.success(f"Student {student_id} deleted successfully!")
                        else:
                            st.error("Failed to delete student")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to server: {e}")
            elif check_response.status_code == 404:
                st.error(f"Student with ID {student_id} not found")
            else:
                st.error("Error checking student existence")

if __name__ == "__main__":
    # Replace the problematic bootstrap code with simple streamlit run
    streamlit_app()
