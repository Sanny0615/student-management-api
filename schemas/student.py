#schemas/student.py

from pydantic import BaseModel, ConfigDict

# ---------- PYDANTIC MODELS ----------

class StudentCreate(BaseModel):
    name: str
    branch_id: int


class StudentUpdate(BaseModel):
    name: str
    branch_id: int


class StudentResponse(BaseModel):
    id: int
    name: str
    branch_id: int
    user_id: int

    model_config = ConfigDict(
        from_attributes=True
    )

