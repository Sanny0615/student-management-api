#models/student.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database_connection import Base

#-----student database tables--------

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    branch_id = Column(
        Integer,
        ForeignKey("branches.id")
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    branch = relationship(
        "BranchDB",
        back_populates="students"
    )

    user=relationship(
        "UserDB",
        back_populates="student"
    )

