import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.auth import hash_password, verify_password
from app.redis_client import redis_client
from app.utils.otp import generate_otp
from app.utils.jwt_handler import create_access_token
from app.tasks import send_otp_email
from app.rate_limiter import check_rate_limit


class AuthService:

    @staticmethod
    def register_user(data, db: Session):

        existing_user = db.query(User).filter(
            User.email == data.email
        ).first()

        if existing_user:
            raise HTTPException(400, "User already exists")

        check_rate_limit(
            key=f"register_limit:{data.email}",
            limit=3,
            window=300
        )

        otp = generate_otp()

        redis_client.setex(
            f"verify:{data.email}",
            300,
            otp
        )

        redis_client.setex(
            f"user_data:{data.email}",
            300,
            json.dumps({
                "email": data.email,
                "password": hash_password(data.password)
            })
        )

        send_otp_email.delay(data.email, otp)

        return {
            "message": "OTP sent successfully"
        }

    @staticmethod
    def verify_otp(data, db: Session):

        stored_otp = redis_client.get(
            f"verify:{data.email}"
        )

        if not stored_otp:
            raise HTTPException(400, "OTP expired")

        if stored_otp != data.otp:
            raise HTTPException(400, "Invalid OTP")

        user_data = redis_client.get(
            f"user_data:{data.email}"
        )

        if not user_data:
            raise HTTPException(
                400,
                "Registration session expired"
            )

        user_data = json.loads(user_data)

        user = User(
            email=user_data["email"],
            password=user_data["password"],
            is_verified=True
        )

        db.add(user)
        db.commit()

        redis_client.delete(f"verify:{data.email}")
        redis_client.delete(f"user_data:{data.email}")

        return {
            "message": "Account verified successfully"
        }

    @staticmethod
    def login_user(data, db: Session):

        user = db.query(User).filter(
            User.email == data.email
        ).first()

        if not user:
            raise HTTPException(
                400,
                "Invalid credentials"
            )

        if not verify_password(
            data.password,
            user.password
        ):
            raise HTTPException(
                400,
                "Invalid credentials"
            )

        if not user.is_verified:
            raise HTTPException(
                400,
                "Please verify your account"
            )

        token = create_access_token({
            "sub": user.email
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    @staticmethod
    def forgot_password(data, db: Session):

        user = db.query(User).filter(
            User.email == data.email
        ).first()

        if not user:
            raise HTTPException(
                404,
                "User not found"
            )

        check_rate_limit(
            key=f"forgot_password:{data.email}",
            limit=3,
            window=300
        )

        otp = generate_otp()

        redis_client.setex(
            f"reset:{data.email}",
            300,
            otp
        )

        send_otp_email.delay(
            data.email,
            otp
        )

        return {
            "message": "Password reset OTP sent"
        }

    @staticmethod
    def reset_password(data, db: Session):

        stored_otp = redis_client.get(
            f"reset:{data.email}"
        )

        if not stored_otp:
            raise HTTPException(
                400,
                "OTP expired"
            )

        if stored_otp != data.otp:
            raise HTTPException(
                400,
                "Invalid OTP"
            )

        user = db.query(User).filter(
            User.email == data.email
        ).first()

        if not user:
            raise HTTPException(
                404,
                "User not found"
            )

        user.password = hash_password(
            data.new_password
        )

        db.commit()

        redis_client.delete(
            f"reset:{data.email}"
        )

        return {
            "message": "Password reset successful"
        }

    @staticmethod
    def resend_otp(data, db: Session):

        user = db.query(User).filter(
            User.email == data.email
        ).first()

        if not user:
            raise HTTPException(
                404,
                "User not found"
            )

        check_rate_limit(
            key=f"resend_otp:{data.email}",
            limit=3,
            window=300
        )

        otp = generate_otp()

        redis_client.setex(
            f"verify:{data.email}",
            300,
            otp
        )

        send_otp_email.delay(
            data.email,
            otp
        )

        return {
            "message": "OTP resent successfully"
        }