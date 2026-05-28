from sqlalchemy.orm import Session

from app.schema.schemas import (
    RegisterSchema,
    VerifyOtpSchema,
    LoginSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema
)

from app.service.auth_service import AuthService


def register_controller(
    data: RegisterSchema,
    db: Session
):
    return AuthService.register_user(data, db)


def verify_otp_controller(
    data: VerifyOtpSchema,
    db: Session
):
    return AuthService.verify_otp(data, db)


def login_controller(
    data: LoginSchema,
    db: Session
):
    return AuthService.login_user(data, db)


def forgot_password_controller(
    data: ForgotPasswordSchema,
    db: Session
):
    return AuthService.forgot_password(data, db)


def reset_password_controller(
    data: ResetPasswordSchema,
    db: Session
):
    return AuthService.reset_password(data, db)


def resend_otp_controller(
    data: ForgotPasswordSchema,
    db: Session
):
    return AuthService.resend_otp(data, db)