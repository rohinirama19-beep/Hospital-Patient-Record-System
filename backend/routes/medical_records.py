"""
Medical Records Management Routes
"""

from fastapi import APIRouter, HTTPException, Query, status
from backend.schemas import MedicalRecordCreate, MedicalRecordUpdate
from backend.database import execute_query
from typing import Optional

router = APIRouter(prefix="/api/medical-records", tags=["Medical Records"])

@router.get("")
def list_medical_records(search: Optional[str] = Query(None, description="Search by patient name")):
    sql = """
        SELECT 
            mr.record_id,
            mr.patient_id,
            p.patient_name,
            mr.doctor_id,
            d.doctor_name,
            mr.appointment_id,
            mr.diagnosis,
            mr.treatment,
            mr.record_date,
            mr.notes
        FROM MEDICAL_RECORD mr
        JOIN PATIENT p ON mr.patient_id = p.patient_id
        JOIN DOCTOR d ON mr.doctor_id = d.doctor_id
    """
    params = []
    if search:
        sql += " WHERE p.patient_name LIKE ?"
        params.append(f"%{search.strip()}%")

    sql += " ORDER BY mr.record_date DESC, mr.record_id DESC"
    records = execute_query(sql, tuple(params), fetchall=True)
    return records or []

@router.get("/{record_id}")
def get_medical_record(record_id: int):
    sql = """
        SELECT 
            mr.record_id,
            mr.patient_id,
            p.patient_name,
            mr.doctor_id,
            d.doctor_name,
            mr.appointment_id,
            mr.diagnosis,
            mr.treatment,
            mr.record_date,
            mr.notes
        FROM MEDICAL_RECORD mr
        JOIN PATIENT p ON mr.patient_id = p.patient_id
        JOIN DOCTOR d ON mr.doctor_id = d.doctor_id
        WHERE mr.record_id = ?
    """
    rec = execute_query(sql, (record_id,), fetchone=True)
    if not rec:
        raise HTTPException(status_code=404, detail="Medical record not found.")
        
    prescriptions = execute_query("""
        SELECT prescription_id, medicine_name, dosage, frequency, duration_days
        FROM PRESCRIPTION
        WHERE record_id = ?
        ORDER BY prescription_id
    """, (record_id,), fetchall=True)
    
    rec["prescriptions"] = prescriptions or []
    return rec

@router.post("", status_code=status.HTTP_201_CREATED)
def create_medical_record(payload: MedicalRecordCreate):
    p = execute_query("SELECT patient_id FROM PATIENT WHERE patient_id = ?", (payload.patient_id,), fetchone=True)
    if not p:
        raise HTTPException(status_code=400, detail="Invalid patient.")
        
    d = execute_query("SELECT doctor_id FROM DOCTOR WHERE doctor_id = ?", (payload.doctor_id,), fetchone=True)
    if not d:
        raise HTTPException(status_code=400, detail="Invalid doctor.")

    try:
        new_id = execute_query("""
            INSERT INTO MEDICAL_RECORD (patient_id, doctor_id, appointment_id, diagnosis, treatment, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            payload.patient_id,
            payload.doctor_id,
            payload.appointment_id,
            payload.diagnosis,
            payload.treatment,
            payload.notes or ""
        ), commit=True)
        return {"success": True, "message": "Medical record saved successfully", "record_id": new_id}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save medical record.")

@router.put("/{record_id}")
def update_medical_record(record_id: int, payload: MedicalRecordUpdate):
    rec = execute_query("SELECT record_id FROM MEDICAL_RECORD WHERE record_id = ?", (record_id,), fetchone=True)
    if not rec:
        raise HTTPException(status_code=404, detail="Medical record not found.")

    try:
        execute_query("""
            UPDATE MEDICAL_RECORD
            SET diagnosis = ?, treatment = ?, notes = ?
            WHERE record_id = ?
        """, (
            payload.diagnosis,
            payload.treatment,
            payload.notes or "",
            record_id
        ), commit=True)
        return {"success": True, "message": "Medical record updated successfully"}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update medical record.")
