from fastapi import FastAPI, HTTPException,APIRouter,Depends
from database import students,t
from models import Student,StudentDB
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database_connection import get_db

router=APIRouter()



@router.get("/students/{id}")
def get_students(id:int,db:Session=Depends(get_db)):
  students=db.query(StudentDB).all()
  if id == 0:
    return students
  student=db.query(StudentDB).filter(StudentDB.id==id).first()
  if student is None:
    raise HTTPException(
    status_code=404,
    detail="student not found"
  )
  return student

@router.get("/teachers")
def teachers():
  return t

@router.post("/students")
def add_student(student: Student,db:Session=Depends(get_db)):
  db_student=StudentDB(
    id=student.id,
    name=student.name,
    branch=student.branch
  )

  try:
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
  except IntegrityError:
    db.rollback()

    raise HTTPException(
      status_code=400,
      detail="Student ID already exists"
    )

  return {"message":"successfully added"}


    
"""
@router.put("/students/{id}")
def update_student(id:int,student:Student):
  for i in students:
    if i["id"]==id:
      i["name"]=student.name
      i["branch"]=student.branch
      return {"message":"student updated Successfully"}
  raise HTTPException(
    status_code=404,
    detail="Student noy found"
  )

@router.delete1("/students/{id}")
def del_student(id:int):
  for i,val in enumerate(students):
    if val["id"]==id:
      del students[i]
      return {"message": f"student id:{id} deleted Successfully"}
  raise HTTPException(
    status_code=404,
    detail="Student not Found"
  )"""

@router.put("/students/{id}")
def update_student(id:int,student: Student,db:Session=Depends(get_db)):

  db_student=db.query(StudentDB).filter(StudentDB.id==id).first()
  db_student.name=student.name
  db_student.branch=student.branch

  if db_student is None:
    raise HTTPException(
      status_code=404,
      detail="Student not found"
    )

  try:
    db.commit()
    db.refresh(db_student)
  except IntegrityError:
    db.rollback()

    raise HTTPException(
      status_code=400,
      detail="Student thing went wrong"
    )

  return db_student

@router.delete("/student/{id}")
def delete_student(id:int,db:Session=Depends(get_db)):
  db_student=db.query(StudentDB).filter(StudentDB.id==id).first()
  if db_student is None:
    raise HTTPException(
      status_code=404,
      detail="student not Found"
    )
  db.delete(db_student)
  db.commit()
  return {"message":"{id} id student record has been deleted"}

  


  