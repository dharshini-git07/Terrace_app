from fastapi import APIRouter, Body
import random

router = APIRouter(prefix="/auth")

# Temporary storage (for beginner)
users = {}

# 🔐 Login API
@router.post("/login")
def login(data: dict = Body(...)):
    role = data.get("role")
    phone = data.get("phone")

    # Admin fixed OTP
    if role == "admin":
        otp = "7186"
    else:
        otp = str(random.randint(1000, 9999))

    users[phone] = otp

    return {
        "message": "OTP generated",
        "otp": otp
    }

# 🔐 Verify OTP
@router.post("/verify")
def verify(data: dict = Body(...)):
    phone = data.get("phone")
    otp = data.get("otp")

    if users.get(phone) == otp:
        return {"status": "success"}
    else:
        return {"status": "failed"}