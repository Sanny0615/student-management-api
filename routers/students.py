#routers/
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate
)

from models.student import StudentDB
from models.branch import BranchDB
from models.user import UserDB

from database.database_connection import get_db
from security import get_current_user,require_admin


router = APIRouter()


# ============================================================
# STUDENT - GET ALL / FILTER
# ============================================================

@router.get(
    "/students",
    response_model=List[StudentResponse]
)
def get_students(
    branch: str | None = None,
    name: str | None = None,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    query = db.query(StudentDB)

    # Filter by branch name
    if branch:
        query = query.join(BranchDB).filter(
            BranchDB.name == branch
        )

    # Filter by student name
    if name:
        query = query.filter(
            StudentDB.name == name
        )

    students = query.all()

    if not students:
        raise HTTPException(
            status_code=404,
            detail="Students not found"
        )

    return students


# ============================================================
# STUDENT - GET ONE
# ============================================================

@router.get(
    "/students/{id}",
    response_model=StudentResponse
)
def get_student(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    student = db.query(StudentDB).filter(
        StudentDB.id == id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# ============================================================
# STUDENT - CREATE
# ============================================================

@router.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def add_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # Check whether branch exists
    branch = db.query(BranchDB).filter(
        BranchDB.id == student.branch_id
    ).first()

    if branch is None:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
            
        )

    # Create student
    db_student = StudentDB(
        name=student.name,
        branch_id=student.branch_id,
        user_id=current_user.id
    )

    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Something went wrong while creating student"
        )

    return db_student


# ============================================================
# STUDENT - UPDATE
# ============================================================

@router.put(
    "/students/{id}",
    response_model=StudentResponse
)
def update_student(
    id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # Find student
    db_student = db.query(StudentDB).filter(
        StudentDB.id == id
    ).first()

    if db_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if current_user.role != "admin":
        if current_user.id != db_student.user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update your own student record"
            )

    # Check whether new branch exists
    branch = db.query(BranchDB).filter(
        BranchDB.id == student.branch_id
    ).first()

    if branch is None:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

    # Update student
    db_student.name = student.name
    db_student.branch_id = student.branch_id

    try:
        db.commit()
        db.refresh(db_student)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Something went wrong while updating student"
        )

    return db_student


# ============================================================
# STUDENT - DELETE
# ============================================================

@router.delete("/students/{id}")
def delete_student(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_admin)
):
    db_student = db.query(StudentDB).filter(
        StudentDB.id == id
    ).first()

    if db_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(db_student)
    db.commit()

    return {
        "message": f"Student {id} deleted successfully"
    }