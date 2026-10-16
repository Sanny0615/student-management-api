from fastapi import FastAPI
from routers import students,branches,users
from database.database_connection import engine,Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(students.router)
app.include_router(branches.router)
app.include_router(users.router)

@app.get("/")
def home():
  return {"message":"Hello Krish"}






