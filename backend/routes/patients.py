"""
Patients CRUD and Medical History Routing
"""

from fastapi import APIRouter, HTTPException, Query, status
from backend.schemas import PatientCreate, PatientUpdate
from backend.database import execute_query
from typing import Optional

router = APIRouter(prefix="/api/patients", tags=["Patients"])

@router.get("")
def list_patients(search: Optional[str] = Query(None, description="Search by name or phone")):
    if search:
        search_pattern = f"%{search.strip()}%"
        sql = """
            SELECT patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at
            FROM PATIENT
            WHERE patient_name LIKE ? OR phone LIKE ?
            ORDER BY patient_id DESC
        """
        patients = execute_query(sql, (search_pattern, search_pattern), fetchall=True)
    else:
        sql = """
            SELECT patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at
            FROM PATIENT
            ORDER BY patient_id DESC
        """
        patients = execute_query(sql, fetchall=True)
    return patients or []

@router.get("/{patient_id}")
def get_patient(patient_id: int):
    patient = execute_query(
        "SELECT * FROM PATIENT WHERE patient_id = ?",
        (patient_id,),
        fetchone=True
    )
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")
    return patient

@router.get("/{patient_id}/details")
def get_patient_details(patient_id: int):
    patient = execute_query(
        "SELECT * FROM PATIENT WHERE patient_id = ?",
        (patient_id,),
        fetchone=True
    )
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")

    appointments = execute_query("""
        SELECT a.appointment_id, d.doctor_name, a.appointment_date, a.appointment_time, a.reason, a.status
        FROM APPOINTMENT a
        JOIN DOCTOR d ON a.doctor_id = d.doctor_id
        WHERE a.patient_id = ?
        ORDER BY a.appointment_date DESC
    """, (patient_id,), fetchall=True)

    medical_history = execute_query("""
        SELECT mr.record_id, d.doctor_name, mr.diagnosis, mr.treatment, mr.record_date, mr.notes
        FROM MEDICAL_RECORD mr
        JOIN DOCTOR d ON mr.doctor_id = d.doctor_id
        WHERE mr.patient_id = ?
        ORDER BY mr.record_date DESC
    """, (patient_id,), fetchall=True)

    bills = execute_query("""
        SELECT b.bill_id, b.appointment_id, b.bill_date, b.consultation_fee, b.medicine_fee, b.total_amount, b.payment_status
        FROM BILL b
        WHERE b.patient_id = ?
        ORDER BY b.bill_date DESC
    """, (patient_id,), fetchall=True)

    return {
        "patient": patient,
        "appointments": appointments or [],
        "medical_history": medical_history or [],
        "bills": bills or []
    }

@router.post("", status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate):
    existing = execute_query("SELECT patient_id FROM PATIENT WHERE email = ?", (payload.email,), fetchone=True)
    if existing:
        raise HTTPException(status_code=400, detail="A patient with this email already exists.")
    
    try:
        new_id = execute_query("""
            INSERT INTO PATIENT (patient_name, date_of_birth, gender, phone, email, address, blood_group)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            payload.patient_name,
            payload.date_of_birth,
            payload.gender,
            payload.phone,
            payload.email,
            payload.address,
            payload.blood_group
        ), commit=True)
        return {"success": True, "message": "Patient registered successfully", "patient_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save patient record.")

@router.put("/{patient_id}")
def update_patient(patient_id: int, payload: PatientUpdate):
    patient = execute_query("SELECT patient_id FROM PATIENT WHERE patient_id = ?", (patient_id,), fetchone=True)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")
        
    dup = execute_query("SELECT patient_id FROM PATIENT WHERE email = ? AND patient_id != ?", (payload.email, patient_id), fetchone=True)
    if dup:
        raise HTTPException(status_code=400, detail="Email is already in use by another patient.")

    try:
        execute_query("""
            UPDATE PATIENT
            SET patient_name = ?, date_of_birth = ?, gender = ?, phone = ?, email = ?, address = ?, blood_group = ?
            WHERE patient_id = ?
        """, (
            payload.patient_name,
            payload.date_of_birth,
            payload.gender,
            payload.phone,
            payload.email,
            payload.address,
            payload.blood_group,
            patient_id
        ), commit=True)
        return {"success": True, "message": "Patient updated successfully"}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update patient record.")

@router.delete("/{patient_id}")
def delete_patient(patient_id: int):
    patient = execute_query("SELECT patient_id FROM PATIENT WHERE patient_id = ?", (patient_id,), fetchone=True)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")

    try:
        execute_query("DELETE FROM PATIENT WHERE patient_id = ?", (patient_id,), commit=True)
        return {"success": True, "message": "Patient record deleted successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Cannot delete patient because they have related appointments, medical records, or bills.")
