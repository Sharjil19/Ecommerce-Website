
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserRegister, UserResponse
from app.core.security import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    # Normalize email before checking for duplicates
    email = user_data.email.lower().strip()

    # Check whether the email is already registered
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    # Hash the password before saving it
    hashed_password = hash_password(user_data.password)

    # Vendors require admin approval
    vendor_status = (
        "pending" if user_data.role == "vendor" else None
    )

    new_user = User(
        full_name=user_data.full_name.strip(),
        email=email,
        hashed_password=hashed_password,
        role=user_data.role,
        is_active=True,
        vendor_status=vendor_status
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register user"
        )

    return new_user
