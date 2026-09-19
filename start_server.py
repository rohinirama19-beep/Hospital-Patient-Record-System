"""
FastAPI Server Launcher for Hospital Patient Record System
"""

import uvicorn
import os
import sys

if __name__ == "__main__":
    print("=" * 80)
    print("       STARTING HOSPITAL PATIENT RECORD SYSTEM — FASTAPI BACKEND")
    print("=" * 80)
    print("  Application URL: http://localhost:8000")
    print("  API Documentation: http://localhost:8000/docs")
    print("  Admin Credentials: admin@hospital.org / admin123")
    print("  Staff Credentials: staff@hospital.org / staff123")
    print("=" * 80)
    print("Press Ctrl+C to stop the server.\n")

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
