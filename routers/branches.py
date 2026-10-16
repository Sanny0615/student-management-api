from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.branch import BranchCreate
from models.branch import BranchDB
from database.database_connection import get_db

router=APIRouter()
# ==============
# ============================================================
# BRANCH - CREATE
# ============================================================

@router.post(
    "/branches",
    status_code=status.HTTP_201_CREATED
)
def add_branch(
    branch: BranchCreate,
    db: Session = Depends(get_db)
):

    db_branch = BranchDB(
        name=branch.name
    )

    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)

    return db_branch


# ============================================================
# BRANCH - GET ONE WITH STUDENTS
# ============================================================

@router.get("/branches/{id}")
def get_branch(
    id: int,
    db: Session = Depends(get_db)
):

    branch = db.query(BranchDB).filter(
        BranchDB.id == id
    ).first()

    if branch is None:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

    return {
        "id": branch.id,
        "name": branch.name,
        "students": [
            {
                "id": student.id,
                "name": student.name
            }
            for student in branch.students
        ]
    }


# ============================================================
# BRANCH - DELETE
# ============================================================

@router.delete("/branches/{id}")
def delete_branch(
    id: int,
    db: Session = Depends(get_db)
):

    branch = db.query(BranchDB).filter(
        BranchDB.id == id
    ).first()

    if branch is None:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

    # Don't delete branch if students are still present
    if branch.students:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete branch because students exist"
        )

    db.delete(branch)
    db.commit()

    return {
        "message": f"Branch {id} deleted successfully"
    }