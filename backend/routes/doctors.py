"""
Doctors and Departments Management Routes
"""

from fastapi import APIRouter, HTTPException, Query, status
from backend.schemas import DoctorCreate, DoctorUpdate
from backend.database import execute_query
from typing import Optional

router = APIRouter(tags=["Doctors"])

@router.get("/api/departments")
def list_departments():
    return execute_query("SELECT department_id, department_name, location FROM DEPARTMENT ORDER BY department_id", fetchall=True) or []

@router.get("/api/doctors")
def list_doctors(search: Optional[str] = Query(None, description="Search by name or specialization")):
    if search:
        search_pattern = f"%{search.strip()}%"
        sql = """
            SELECT d.doctor_id, d.doctor_name, d.specialization, d.phone, d.email, d.department_id, dept.department_name
            FROM DOCTOR d
            JOIN DEPARTMENT dept ON d.department_id = dept.department_id
            WHERE d.doctor_name LIKE ? OR d.specialization LIKE ?
            ORDER BY d.doctor_id ASC
        """
        doctors = execute_query(sql, (search_pattern, search_pattern), fetchall=True)
    else:
        sql = """
            SELECT d.doctor_id, d.doctor_name, d.specialization, d.phone, d.email, d.department_id, dept.department_name
            FROM DOCTOR d
            JOIN DEPARTMENT dept ON d.department_id = dept.department_id
            ORDER BY d.doctor_id ASC
        """
        doctors = execute_query(sql, fetchall=True)
    return doctors or []

@router.get("/api/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doctor = execute_query("""
        SELECT d.doctor_id, d.doctor_name, d.specialization, d.phone, d.email, d.department_id, dept.department_name
        FROM DOCTOR d
        JOIN DEPARTMENT dept ON d.department_id = dept.department_id
        WHERE d.doctor_id = ?
    """, (doctor_id,), fetchone=True)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found.")
    return doctor

@router.post("/api/doctors", status_code=status.HTTP_201_CREATED)
def create_doctor(payload: DoctorCreate):
    existing = execute_query("SELECT doctor_id FROM DOCTOR WHERE email = ?", (payload.email,), fetchone=True)
    if existing:
        raise HTTPException(status_code=400, detail="A doctor with this email already exists.")
        
    dept = execute_query("SELECT department_id FROM DEPARTMENT WHERE department_id = ?", (payload.department_id,), fetchone=True)
    if not dept:
        raise HTTPException(status_code=400, detail="Selected department does not exist.")

    try:
        new_id = execute_query("""
            INSERT INTO DOCTOR (doctor_name, specialization, phone, email, department_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            payload.doctor_name,
            payload.specialization,
            payload.phone,
            payload.email,
            payload.department_id
        ), commit=True)
        return {"success": True, "message": "Doctor added successfully", "doctor_id": new_id}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save doctor record.")

@router.put("/api/doctors/{doctor_id}")
def update_doctor(doctor_id: int, payload: DoctorUpdate):
    doc = execute_query("SELECT doctor_id FROM DOCTOR WHERE doctor_id = ?", (doctor_id,), fetchone=True)
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found.")
        
    dup = execute_query("SELECT doctor_id FROM DOCTOR WHERE email = ? AND doctor_id != ?", (payload.email, doctor_id), fetchone=True)
    if dup:
        raise HTTPException(status_code=400, detail="Email is already used by another doctor.")

    try:
        execute_query("""
            UPDATE DOCTOR
            SET doctor_name = ?, specialization = ?, phone = ?, email = ?, department_id = ?
            WHERE doctor_id = ?
        """, (
            payload.doctor_name,
            payload.specialization,
            payload.phone,
            payload.email,
            payload.department_id,
            doctor_id
        ), commit=True)
        return {"success": True, "message": "Doctor updated successfully"}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update doctor.")

@router.delete("/api/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doc = execute_query("SELECT doctor_id FROM DOCTOR WHERE doctor_id = ?", (doctor_id,), fetchone=True)
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found.")

    try:
        execute_query("DELETE FROM DOCTOR WHERE doctor_id = ?", (doctor_id,), commit=True)
        return {"success": True, "message": "Doctor deleted successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Cannot delete doctor with assigned appointments or clinical records.")
