"""
Appointments Scheduling and Status Transition Routes
"""

from fastapi import APIRouter, HTTPException, Query, status
from backend.schemas import AppointmentCreate, AppointmentUpdate, AppointmentStatusUpdate
from backend.database import execute_query
from typing import Optional

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

@router.get("")
def list_appointments(
    date: Optional[str] = Query(None, description="Filter by appointment date (YYYY-MM-DD)"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (SCHEDULED, COMPLETED, CANCELLED)")
):
    sql = """
        SELECT 
            a.appointment_id,
            a.patient_id,
            p.patient_name,
            a.doctor_id,
            d.doctor_name,
            d.specialization,
            a.appointment_date,
            a.appointment_time,
            a.reason,
            a.status
        FROM APPOINTMENT a
        JOIN PATIENT p ON a.patient_id = p.patient_id
        JOIN DOCTOR d ON a.doctor_id = d.doctor_id
        WHERE 1=1
    """
    params = []
    if date:
        sql += " AND a.appointment_date = ?"
        params.append(date)
    if status_filter:
        sql += " AND a.status = ?"
        params.append(status_filter)

    sql += " ORDER BY a.appointment_date DESC, a.appointment_time DESC"
    appointments = execute_query(sql, tuple(params), fetchall=True)
    return appointments or []

@router.get("/{appointment_id}")
def get_appointment(appointment_id: int):
    sql = """
        SELECT 
            a.appointment_id,
            a.patient_id,
            p.patient_name,
            a.doctor_id,
            d.doctor_name,
            a.appointment_date,
            a.appointment_time,
            a.reason,
            a.status
        FROM APPOINTMENT a
        JOIN PATIENT p ON a.patient_id = p.patient_id
        JOIN DOCTOR d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_id = ?
    """
    appt = execute_query(sql, (appointment_id,), fetchone=True)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    return appt

@router.post("", status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate):
    # Verify patient
    p = execute_query("SELECT patient_id FROM PATIENT WHERE patient_id = ?", (payload.patient_id,), fetchone=True)
    if not p:
        raise HTTPException(status_code=400, detail="Selected patient does not exist.")
        
    # Verify doctor
    d = execute_query("SELECT doctor_id FROM DOCTOR WHERE doctor_id = ?", (payload.doctor_id,), fetchone=True)
    if not d:
        raise HTTPException(status_code=400, detail="Selected doctor does not exist.")

    try:
        new_id = execute_query("""
            INSERT INTO APPOINTMENT (patient_id, doctor_id, appointment_date, appointment_time, reason, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            payload.patient_id,
            payload.doctor_id,
            payload.appointment_date,
            payload.appointment_time,
            payload.reason,
            payload.status or "SCHEDULED"
        ), commit=True)
        return {"success": True, "message": "Appointment booked successfully", "appointment_id": new_id}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to schedule appointment.")

@router.put("/{appointment_id}")
def update_appointment(appointment_id: int, payload: AppointmentUpdate):
    appt = execute_query("SELECT appointment_id FROM APPOINTMENT WHERE appointment_id = ?", (appointment_id,), fetchone=True)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found.")

    try:
        execute_query("""
            UPDATE APPOINTMENT
            SET appointment_date = ?, appointment_time = ?, reason = ?, status = ?
            WHERE appointment_id = ?
        """, (
            payload.appointment_date,
            payload.appointment_time,
            payload.reason,
            payload.status,
            appointment_id
        ), commit=True)
        return {"success": True, "message": "Appointment updated successfully"}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update appointment.")

@router.put("/{appointment_id}/status")
def update_appointment_status(appointment_id: int, payload: AppointmentStatusUpdate):
    appt = execute_query("SELECT appointment_id FROM APPOINTMENT WHERE appointment_id = ?", (appointment_id,), fetchone=True)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found.")

    try:
        execute_query(
            "UPDATE APPOINTMENT SET status = ? WHERE appointment_id = ?",
            (payload.status, appointment_id),
            commit=True
        )
        return {"success": True, "message": f"Appointment marked as {payload.status}"}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update appointment status.")
