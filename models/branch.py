from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database_connection import Base
# ----------Branch DATABASE MODELS ----------

class BranchDB(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    students = relationship(
        "StudentDB",
        back_populates="branch"
    )
