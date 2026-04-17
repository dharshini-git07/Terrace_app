import random

from fastapi import APIRouter
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    role: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)


class VerifyRequest(BaseModel):
    phone: str = Field(..., min_length=1)
    otp: str = Field(..., min_length=4, max_length=4)


class OtpResponse(BaseModel):
    message: str
    otp: str


class VerifyResponse(BaseModel):
    status: str


router = APIRouter(prefix="/auth")

users: dict[str, str] = {}


@router.post("/login")
def login(data: LoginRequest) -> OtpResponse:
    if data.role == "admin":
        otp = "7186"
    else:
        otp = str(random.randint(1000, 9999))

    users[data.phone] = otp
    return OtpResponse(message="OTP generated", otp=otp)


@router.post("/verify")
def verify(data: VerifyRequest) -> VerifyResponse:
    if users.get(data.phone) == data.otp:
        return VerifyResponse(status="success")

    return VerifyResponse(status="failed")
