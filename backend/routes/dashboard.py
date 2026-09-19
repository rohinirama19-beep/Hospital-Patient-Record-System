"""
Dashboard Statistics and Activity Feeds
"""

from fastapi import APIRouter
from backend.database import execute_query
from datetime import date

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("")
def get_dashboard_data():
    today_str = date.today().strftime("%Y-%m-%d")
    
    # 1. Database-derived statistics
    total_patients = execute_query("SELECT COUNT(*) as count FROM PATIENT", fetchone=True)["count"]
    total_doctors = execute_query("SELECT COUNT(*) as count FROM DOCTOR", fetchone=True)["count"]
    total_records = execute_query("SELECT COUNT(*) as count FROM MEDICAL_RECORD", fetchone=True)["count"]
    pending_bills = execute_query("SELECT COUNT(*) as count FROM BILL WHERE payment_status = 'PENDING'", fetchone=True)["count"]
    
    # Today's appointments (if no matches for today's system date, count SCHEDULED appointments)
    today_appts_res = execute_query("SELECT COUNT(*) as count FROM APPOINTMENT WHERE appointment_date = ?", (today_str,), fetchone=True)
    today_appts = today_appts_res["count"] if today_appts_res else 0
    if today_appts == 0:
        # Fallback to count of active scheduled appointments
        today_appts = execute_query("SELECT COUNT(*) as count FROM APPOINTMENT WHERE status = 'SCHEDULED'", fetchone=True)["count"]

    # 2. Recent Appointments
    recent_appointments = execute_query("""
        SELECT 
            a.appointment_id,
            p.patient_name,
            d.doctor_name,
            a.appointment_date,
            a.appointment_time,
            a.status
        FROM APPOINTMENT a
        JOIN PATIENT p ON a.patient_id = p.patient_id
        JOIN DOCTOR d ON a.doctor_id = d.doctor_id
        ORDER BY a.appointment_date DESC, a.appointment_id DESC
        LIMIT 5
    """, fetchall=True)

    # 3. Recent Medical Records
    recent_records = execute_query("""
        SELECT 
            mr.record_id,
            p.patient_name,
            d.doctor_name,
            mr.diagnosis,
            mr.record_date
        FROM MEDICAL_RECORD mr
        JOIN PATIENT p ON mr.patient_id = p.patient_id
        JOIN DOCTOR d ON mr.doctor_id = d.doctor_id
        ORDER BY mr.record_date DESC, mr.record_id DESC
        LIMIT 5
    """, fetchall=True)

    return {
        "stats": {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "today_appointments": today_appts,
            "total_records": total_records,
            "pending_bills": pending_bills
        },
        "recent_appointments": recent_appointments or [],
        "recent_records": recent_records or []
    }
