"""
Billing and Financial Ledger Routes
Enforces backend/database total amount calculations (consultation_fee + medicine_fee).
"""

from fastapi import APIRouter, HTTPException, Query, status
from backend.schemas import BillGenerateRequest, BillStatusUpdate
from backend.database import execute_query
from typing import Optional

router = APIRouter(prefix="/api/bills", tags=["Bills"])

@router.get("")
def list_bills(payment_status: Optional[str] = Query(None, description="Filter by payment status (PAID, PENDING)")):
    sql = """
        SELECT 
            b.bill_id,
            b.patient_id,
            p.patient_name,
            b.appointment_id,
            b.bill_date,
            b.consultation_fee,
            b.medicine_fee,
            b.total_amount,
            b.payment_status
        FROM BILL b
        JOIN PATIENT p ON b.patient_id = p.patient_id
    """
    params = []
    if payment_status and payment_status.upper() in ['PAID', 'PENDING']:
        sql += " WHERE b.payment_status = ?"
        params.append(payment_status.upper())

    sql += " ORDER BY b.bill_date DESC, b.bill_id DESC"
    bills = execute_query(sql, tuple(params), fetchall=True)
    return bills or []

@router.get("/{bill_id}")
def get_bill(bill_id: int):
    sql = """
        SELECT 
            b.bill_id,
            b.patient_id,
            p.patient_name,
            p.phone,
            p.email,
            b.appointment_id,
            b.bill_date,
            b.consultation_fee,
            b.medicine_fee,
            b.total_amount,
            b.payment_status
        FROM BILL b
        JOIN PATIENT p ON b.patient_id = p.patient_id
        WHERE b.bill_id = ?
    """
    bill = execute_query(sql, (bill_id,), fetchone=True)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill record not found.")
    return bill

@router.post("", status_code=status.HTTP_201_CREATED)
def generate_bill(payload: BillGenerateRequest):
    # 1. Retrieve appointment to get patient_id
    appt = execute_query("SELECT patient_id FROM APPOINTMENT WHERE appointment_id = ?", (payload.appointment_id,), fetchone=True)
    if not appt:
        raise HTTPException(status_code=400, detail="Specified appointment does not exist.")
        
    patient_id = appt["patient_id"]

    # 2. Strict backend calculation: total_amount = consultation_fee + medicine_fee
    total_amount = round(float(payload.consultation_fee) + float(payload.medicine_fee), 2)

    # 3. Check if bill already exists for this appointment
    existing = execute_query("SELECT bill_id FROM BILL WHERE appointment_id = ?", (payload.appointment_id,), fetchone=True)
    if existing:
        # Update existing bill
        execute_query("""
            UPDATE BILL
            SET consultation_fee = ?, medicine_fee = ?, total_amount = ?, bill_date = DATE('now')
            WHERE appointment_id = ?
        """, (
            payload.consultation_fee,
            payload.medicine_fee,
            total_amount,
            payload.appointment_id
        ), commit=True)
        return {
            "success": True,
            "message": f"Bill updated successfully for Appointment #{payload.appointment_id}",
            "bill_id": existing["bill_id"],
            "total_amount": total_amount
        }
    else:
        # Insert new bill
        new_id = execute_query("""
            INSERT INTO BILL (patient_id, appointment_id, consultation_fee, medicine_fee, total_amount, payment_status)
            VALUES (?, ?, ?, ?, ?, 'PENDING')
        """, (
            patient_id,
            payload.appointment_id,
            payload.consultation_fee,
            payload.medicine_fee,
            total_amount
        ), commit=True)
        return {
            "success": True,
            "message": f"Bill generated successfully for Appointment #{payload.appointment_id}",
            "bill_id": new_id,
            "total_amount": total_amount
        }

@router.put("/{bill_id}/status")
def update_bill_status(bill_id: int, payload: BillStatusUpdate):
    bill = execute_query("SELECT bill_id FROM BILL WHERE bill_id = ?", (bill_id,), fetchone=True)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill record not found.")

    try:
        execute_query(
            "UPDATE BILL SET payment_status = ? WHERE bill_id = ?",
            (payload.payment_status, bill_id),
            commit=True
        )
        return {"success": True, "message": f"Bill status updated to {payload.payment_status}"}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update payment status.")
