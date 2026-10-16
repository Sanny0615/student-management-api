from sqlalchemy import Column, Integer, String
from database.database_connection import Base
from sqlalchemy.orm import relationship



class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String,nullable=False,default="student")

    student = relationship(
            "StudentDB",
            back_populates="user",
            uselist=False
        )
"""

  "username": "sunnny12",
  "email": "dv@gmail.com",
  "password": "1234sunny"
}"""