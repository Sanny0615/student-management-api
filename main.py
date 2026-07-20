from fastapi import FastAPI, HTTPException
from models import Student
from database import students,t
from routers import students
from database_connection import engine,Base
from models import StudentDB

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(students.router)

@app.get("/")
def home():
  return {"message":"Hello Krish"}






