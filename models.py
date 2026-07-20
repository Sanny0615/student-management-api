from pydantic import BaseModel
from sqlalchemy import Column,Integer,String
from database_connection import Base

class Student(BaseModel):
  id:int
  name:str
  branch:str

class StudentDB(Base):
  __tablename__="students"

  id=Column(Integer,primary_key=True)
  name=Column(String)
  branch=Column(String)
