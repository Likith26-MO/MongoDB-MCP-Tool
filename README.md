MongoDB MCP CRUD System
A comprehensive MongoDB CRUD (Create, Read, Update, Delete) system with FastAPI backend, Streamlit frontend, and MCP (Model Context Protocol) integration.

🚀 Features
RESTful API: FastAPI backend with full CRUD operations

Web Interface: Streamlit-based control panel

MongoDB Integration: Direct database operations

MCP Support: Model Context Protocol for AI tool discovery

Testing Scripts: PowerShell scripts for API testing

Sample Data: Automatic population with 150 student records

📋 Prerequisites
Python 3.8+

MongoDB (local installation)

Required Python packages

🛠 Installation
Clone or download the project files

Install Python dependencies:

bash
pip install fastapi uvicorn pymongo streamlit requests pydantic python-multipart
Ensure MongoDB is running:

bash
# If using local MongoDB
mongod

# Or start as service
sudo systemctl start mongod
🏃‍♂️ Quick Start
1. Populate Database with Sample Data
bash
python populate_mongo.py
2. Start the FastAPI Server
bash
# Option 1: Using main.py (with MCP endpoints)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using api_server.py (basic CRUD only)
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000

# Option 3: Using mongo_mcp_tool.py (alternative implementation)
uvicorn mongo_mcp_tool:app --reload --host 0.0.0.0 --port 8000
3. Access the Application
API Documentation: http://localhost:8000/docs
Streamlit Interface: streamlit run mcp.py
MCP Discovery: http://localhost:8000/mcp

📁 Project Structure
text
├── mongo_crud.py          # MongoDB CRUD operations
├── main.py               # FastAPI app with MCP endpoints
├── api_server.py         # Alternative FastAPI implementation
├── mongo_mcp_tool.py     # Complete MCP tool implementation
├── mcp.py               # Streamlit interface + MCP router
├── populate_mongo.py     # Sample data generator
├── test_mongo_mcp.ps1    # PowerShell API tests
└── lan.py               # LangGraph integration example
🔧 API Endpoints
CRUD Operations
POST /students - Create new student

GET /students - List students (with pagination)

GET /students/{id} - Get student by MongoDB ID

PATCH /students/{id} - Update student

DELETE /students/{id} - Delete student

MCP Discovery
GET /mcp - Discover available tools and capabilities

🎯 Usage Examples
Create a Student
bash
curl -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "S999",
    "first_name": "John",
    "last_name": "Doe",
    "age": 22,
    "scores": {"math": 95, "cs": 88, "db": 92},
    "active": true
  }'
List Students
bash
curl "http://localhost:8000/students?limit=5&skip=0"
Update Student
bash
curl -X PATCH "http://localhost:8000/students/{mongo_id}" \
  -H "Content-Type: application/json" \
  -d '{"age": 23}'
🖥 Streamlit Interface
The Streamlit app provides a user-friendly interface for all operations:

List Students: View students with pagination

Create Student: Add new students with form validation

Search Student: Find students by ID or MongoDB _id

Update Student: Modify existing student records

Delete Student: Remove students with confirmation

Run with: streamlit run mcp.py

🧪 Testing
PowerShell Tests
powershell
.\test_mongo_mcp.ps1
Manual API Testing
Access Swagger UI: http://localhost:8000/docs

Use the interactive documentation to test endpoints

Or use the provided PowerShell script

🔍 MCP Integration
The system supports MCP (Model Context Protocol) for AI tool discovery:

python
from mcp import MCPClient

# Connect to MCP server
mongo_mcp = MCPClient("http://127.0.0.1:8000/mcp")

# Discover available tools
tools = mongo_mcp.discover()
🐛 Troubleshooting
Common Issues
MongoDB Connection Error

Ensure MongoDB is running: mongod

Check connection string in mongo_crud.py

Port Already in Use

Change port in uvicorn command: --port 8001

Or kill existing process: lsof -ti:8000 | xargs kill -9

Streamlit Connection Issues

Ensure FastAPI server is running first

Check if API is accessible: curl http://localhost:8000/

Create/Delete Not Working

Use the updated mcp.py with proper error handling

Check student exists before deletion

Database Reset
bash
# Clear existing data
mongo
use classroom
db.students.deleteMany({})

# Repopulate
python populate_mongo.py
📊 Sample Data Structure
Each student document contains:

json
{
  "student_id": "S001",
  "first_name": "First1",
  "last_name": "Last1", 
  "age": 19,
  "scores": {"math": 61, "cs": 56, "db": 51},
  "active": true
}
🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Create a Pull Request
