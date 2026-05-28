from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schema.schemas import (
    RegisterSchema,
    VerifyOtpSchema,
    LoginSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema
)

from app.controller.auth_controller import (
    register_controller,
    verify_otp_controller,
    login_controller,
    forgot_password_controller,
    reset_password_controller,
    resend_otp_controller
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(
    data: RegisterSchema,
    db: Session = Depends(get_db)
):
    return register_controller(data, db)


@router.post("/verify-otp")
def verify_otp(
    data: VerifyOtpSchema,
    db: Session = Depends(get_db)
):
    return verify_otp_controller(data, db)


@router.post("/login")
def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):
    return login_controller(data, db)


@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordSchema,
    db: Session = Depends(get_db)
):
    return forgot_password_controller(data, db)


@router.post("/reset-password")
def reset_password(
    data: ResetPasswordSchema,
    db: Session = Depends(get_db)
):
    return reset_password_controller(data, db)


@router.post("/resend-otp")
def resend_otp(
    data: ForgotPasswordSchema,
    db: Session = Depends(get_db)
):
    return resend_otp_controller(data, db)
