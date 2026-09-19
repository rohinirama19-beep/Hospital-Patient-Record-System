"""
Prescriptions Management Routes
"""

from fastapi import APIRouter, HTTPException, status
from backend.schemas import PrescriptionCreate
from backend.database import execute_query

router = APIRouter(prefix="/api/prescriptions", tags=["Prescriptions"])

@router.get("")
def list_prescriptions():
    sql = """
        SELECT 
            pr.prescription_id,
            pr.record_id,
            p.patient_id,
            p.patient_name,
            d.doctor_name,
            pr.medicine_name,
            pr.dosage,
            pr.frequency,
            pr.duration_days,
            mr.diagnosis,
            mr.record_date
        FROM PRESCRIPTION pr
        JOIN MEDICAL_RECORD mr ON pr.record_id = mr.record_id
        JOIN PATIENT p ON mr.patient_id = p.patient_id
        JOIN DOCTOR d ON mr.doctor_id = d.doctor_id
        ORDER BY pr.prescription_id DESC
    """
    prescriptions = execute_query(sql, fetchall=True)
    return prescriptions or []

@router.post("", status_code=status.HTTP_201_CREATED)
def create_prescription(payload: PrescriptionCreate):
    mr = execute_query("SELECT record_id FROM MEDICAL_RECORD WHERE record_id = ?", (payload.record_id,), fetchone=True)
    if not mr:
        raise HTTPException(status_code=400, detail="Associated medical record does not exist.")

    try:
        new_id = execute_query("""
            INSERT INTO PRESCRIPTION (record_id, medicine_name, dosage, frequency, duration_days)
            VALUES (?, ?, ?, ?, ?)
        """, (
            payload.record_id,
            payload.medicine_name,
            payload.dosage,
            payload.frequency,
            payload.duration_days
        ), commit=True)
        return {"success": True, "message": "Prescription added successfully", "prescription_id": new_id}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save prescription.")
