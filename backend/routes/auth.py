"""
Authentication Route for Admin and Staff Login
"""

from fastapi import APIRouter, HTTPException, status
from backend.schemas import LoginRequest
from backend.database import execute_query

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login")
def login(payload: LoginRequest):
    user = execute_query(
        "SELECT user_id, name, email, role, password FROM ADMIN_USER WHERE email = ?",
        (payload.email,),
        fetchone=True
    )
    
    if not user or user["password"] != payload.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please check your credentials."
        )
        
    return {
        "success": True,
        "message": f"Welcome back, {user['name']}",
        "user": {
            "id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }
