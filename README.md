Absolutely! I’ve reformatted the README with **clear, readable fonts and spacing**, structured headings, and consistent code blocks—perfect for GitHub display. Here’s the final **clean and professional version**:

---

# MongoDB-MCP-Tool

A comprehensive **MongoDB CRUD system** with **FastAPI backend**, **Streamlit frontend**, and **MCP (Model Context Protocol)** integration for AI tool discovery.

---

## 🚀 Features

* **RESTful API**: Full CRUD operations via FastAPI
* **Web Interface**: Streamlit-based control panel
* **MongoDB Integration**: Direct database operations
* **MCP Support**: AI tool discovery via Model Context Protocol
* **Testing Scripts**: PowerShell scripts for API testing
* **Sample Data**: Auto-populates 150 student records

---

## 📋 Prerequisites

* Python 3.8+
* MongoDB (local installation)
* Required Python packages:

```bash
pip install fastapi uvicorn pymongo streamlit requests pydantic python-multipart
```

---

## 🛠 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/MongoDB-MCP-Tool.git
cd MongoDB-MCP-Tool
```

2. **Ensure MongoDB is running**:

```bash
# Start MongoDB manually
mongod

# Or start as a service (Linux)
sudo systemctl start mongod
```

3. **Populate Database with Sample Data**:

```bash
python populate_mongo.py
```

---

## 🏃‍♂️ Running the Application

### 1️⃣ Start FastAPI Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

* **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 2️⃣ Start Streamlit Frontend

```bash
streamlit run mcp.py
```

* Open in browser: [http://localhost:8501](http://localhost:8501)

---

## 📁 Project Structure

```
MongoDB-MCP-Tool/
├── mongo_crud.py          # MongoDB CRUD operations
├── main.py                # FastAPI app with MCP endpoints
├── api_server.py          # Alternative FastAPI implementation
├── mongo_mcp_tool.py      # Complete MCP tool implementation
├── mcp.py                 # Streamlit interface + MCP router
├── populate_mongo.py      # Sample data generator
├── test_mongo_mcp.ps1     # PowerShell API tests
└── lan.py                  # LangGraph integration example
```

---

## 🔧 API Endpoints

**CRUD Operations**

* `POST /students` – Create new student
* `GET /students` – List students (with pagination)
* `GET /students/{id}` – Get student by MongoDB ID
* `PATCH /students/{id}` – Update student
* `DELETE /students/{id}` – Delete student

**MCP Discovery**

* `GET /mcp` – Discover available tools and capabilities

---

## 🎯 Usage Examples

**Create a Student**

```bash
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
```

**List Students**

```bash
curl "http://localhost:8000/students?limit=5&skip=0"
```

**Update Student**

```bash
curl -X PATCH "http://localhost:8000/students/{mongo_id}" \
-H "Content-Type: application/json" \
-d '{"age": 23}'
```

---

## 🖥 Streamlit Interface

* List, Create, Search, Update, Delete students
* Pagination and form validation

```bash
streamlit run mcp.py
```

---

## 🧪 Testing

* **PowerShell Tests**:

```powershell
.\test_mongo_mcp.ps1
```

* **Manual API Testing**:
  Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔍 MCP Integration

```python
from mcp import MCPClient

mongo_mcp = MCPClient("http://127.0.0.1:8000/mcp")
tools = mongo_mcp.discover()
```

* Enables AI tools to discover and interact with your MongoDB CRUD system.

---

## 🐛 Troubleshooting

* **MongoDB Connection Error**: Ensure MongoDB is running and check `mongo_crud.py` connection string
* **Port Already in Use**: Change port or kill existing process
* **Streamlit Connection Issues**: Ensure FastAPI server is running first

**Database Reset**

```bash
mongo
use classroom
db.students.deleteMany({})
python populate_mongo.py
```

---

## 📊 Sample Data Structure

```json
{
  "student_id": "S001",
  "first_name": "First1",
  "last_name": "Last1",
  "age": 19,
  "scores": {"math": 61, "cs": 56, "db": 51},
  "active": true
}
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## ⚡ Quick Start Summary

1. Start **MongoDB**
2. Start **FastAPI backend**:

```bash
uvicorn main:app --reload
```

3. Start **Streamlit frontend**:

```bash
streamlit run mcp.py
```

4. Access APIs at [http://localhost:8000/docs](http://localhost:8000/docs)
5. Access Streamlit UI at [http://localhost:8501](http://localhost:8501)

