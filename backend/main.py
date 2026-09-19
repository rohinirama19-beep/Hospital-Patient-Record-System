"""
Main FastAPI Application Entry Point
Configures routes, CORS, database lifecycle, and static frontend delivery.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from backend.database import initialize_database
from backend.routes import (
    auth,
    dashboard,
    patients,
    doctors,
    appointments,
    medical_records,
    prescriptions,
    bills
)

app = FastAPI(
    title="Hospital Patient Record System API",
    description="Oracle COE Academic Project - Step 2 Backend Services",
    version="1.0.0"
)

# CORS middleware for clean API integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Event: initialize database
@app.on_event("startup")
def startup_db_client():
    initialize_database()

# Register API Routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(medical_records.router)
app.include_router(prescriptions.router)
app.include_router(bills.router)

# Mount Frontend Static Assets
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

if FRONTEND_DIR.exists():
    css_dir = FRONTEND_DIR / "css"
    js_dir = FRONTEND_DIR / "js"
    if css_dir.exists():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
    if js_dir.exists():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")

    # Clean Page Route Handlers
    @app.get("/", include_in_schema=False)
    def serve_login():
        return FileResponse(FRONTEND_DIR / "index.html")

    @app.get("/login", include_in_schema=False)
    def serve_login_alt():
        return FileResponse(FRONTEND_DIR / "index.html")

    @app.get("/dashboard", include_in_schema=False)
    def serve_dashboard():
        return FileResponse(FRONTEND_DIR / "dashboard.html")

    @app.get("/patients", include_in_schema=False)
    def serve_patients():
        return FileResponse(FRONTEND_DIR / "patients.html")

    @app.get("/doctors", include_in_schema=False)
    def serve_doctors():
        return FileResponse(FRONTEND_DIR / "doctors.html")

    @app.get("/appointments", include_in_schema=False)
    def serve_appointments():
        return FileResponse(FRONTEND_DIR / "appointments.html")

    @app.get("/medical-records", include_in_schema=False)
    def serve_medical_records():
        return FileResponse(FRONTEND_DIR / "medical-records.html")

    @app.get("/prescriptions", include_in_schema=False)
    def serve_prescriptions():
        return FileResponse(FRONTEND_DIR / "prescriptions.html")

    @app.get("/bills", include_in_schema=False)
    def serve_bills():
        return FileResponse(FRONTEND_DIR / "bills.html")
