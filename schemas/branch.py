from pydantic import BaseModel

class BranchCreate(BaseModel):
  name:str
