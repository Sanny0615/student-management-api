#routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm


from models.user import UserDB
from database.database_connection import get_db
from security import hash_password,verify_password,create_access_token


from schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin
)

router=APIRouter()

@router.post("/users",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def user_register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    hashed_password = hash_password(user.password)

    db_user = UserDB(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
    
    except IntegrityError:
            db.rollback()
    
            raise HTTPException(
                status_code=400,
                detail="Something went wrong while creating user"
            )
    
    return db_user


@router.post("/login")
def user_login(
    user: OAuth2PasswordRequestForm = Depends(),
    db:Session=Depends(get_db)
):
    db_user = db.query(UserDB).filter(
            UserDB.username == user.username
        ).first()
    
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="Invalid username or password"
        )
    verified_password=verify_password(user.password,db_user.password)
    if verified_password:

        access_token = create_access_token(
            {"sub": str(db_user.id)}
        )

        return {
            "access_token":access_token,
            "token_type":"bearer"
        }
    return {"message": "Invalid username or password"}
    