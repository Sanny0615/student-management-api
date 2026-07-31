# 🎓 Student Management API

A REST API built using **FastAPI**, **SQLAlchemy**, and **SQLite** for managing student records.

## 📸 Project Preview

![Swagger UI](Screenshot%202026-07-31%20094817.png)

## 🚀 Features

- Add Student
- View Students
- Update Student
- Delete Student
- REST API Endpoints
- SQLite Database

- ## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /students | Get all students |
| GET | /students/{id} | Get student by ID |
| POST | /students | Create a new student |
| PUT | /students/{id} | Update student |
| DELETE | /students/{id} | Delete student |

- ## 🛠️ Tech Stack
  
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

  ## ⚙️ Installation

```bash
git clone https://github.com/Sanny0615/student-management-api.git
cd student-management-api
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000/docs

## 📂 Project Structure

```
student-management-api/
├── routers/
├── database.py
├── models.py
├── database_connection.py
├── main.py
├── requirements.txt
└── student.db
```

## 🚀 Future Improvements

- JWT Authentication
- Role-Based Access Control (Admin/Student)
- PostgreSQL Database
- Docker Support
- Automated Testing
- Deployment on Render

## ▶️ Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit:

```
http://127.0.0.1:8000/docs
```

## 📚 Learning Outcome

This project helped me learn:

- FastAPI
- REST APIs
- SQLAlchemy ORM
- CRUD Operations
- Backend Development

## 👨‍💻 Author

**Dulam Sunny**
