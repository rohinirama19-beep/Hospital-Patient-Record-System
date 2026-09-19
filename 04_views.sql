-- ============================================================================
-- PROJECT: HOSPITAL PATIENT RECORD SYSTEM (ORACLE COE PROJECT)
-- SCRIPT: 04_views.sql
-- PURPOSE: Create and test Oracle Database Views
-- ============================================================================

-- ----------------------------------------------------------------------------
-- VIEW 1: PATIENT_MEDICAL_HISTORY_VIEW
-- Combines patient details, attending physician, department, appointment date,
-- diagnosis, treatment, and medical record date.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW PATIENT_MEDICAL_HISTORY_VIEW AS
SELECT 
    p.patient_name,
    d.doctor_name,
    dept.department_name,
    a.appointment_date,
    mr.diagnosis,
    mr.treatment,
    mr.record_date
FROM MEDICAL_RECORD mr
JOIN PATIENT p ON mr.patient_id = p.patient_id
JOIN DOCTOR d ON mr.doctor_id = d.doctor_id
JOIN DEPARTMENT dept ON d.department_id = dept.department_id
LEFT JOIN APPOINTMENT a ON mr.appointment_id = a.appointment_id;

-- ----------------------------------------------------------------------------
-- VIEW 2: PATIENT_BILL_VIEW
-- Displays billing breakdown, appointment reference, and payment status.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW PATIENT_BILL_VIEW AS
SELECT 
    p.patient_name,
    b.appointment_id,
    b.bill_date,
    b.consultation_fee,
    b.medicine_fee,
    b.total_amount,
    b.payment_status
FROM BILL b
JOIN PATIENT p ON b.patient_id = p.patient_id;

-- ----------------------------------------------------------------------------
-- VIEW 3: DOCTOR_APPOINTMENT_SUMMARY
-- Displays performance summary for doctors including appointment counts 
-- categorized by status.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW DOCTOR_APPOINTMENT_SUMMARY AS
SELECT 
    d.doctor_name,
    d.specialization,
    COUNT(a.appointment_id) AS total_appointments,
    SUM(CASE WHEN a.status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed_appointments,
    SUM(CASE WHEN a.status = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled_appointments
FROM DOCTOR d
LEFT JOIN APPOINTMENT a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.doctor_name, d.specialization;

-- ----------------------------------------------------------------------------
-- VERIFICATION SELECT QUERIES
-- ----------------------------------------------------------------------------
SELECT * FROM PATIENT_MEDICAL_HISTORY_VIEW;

SELECT * FROM PATIENT_BILL_VIEW;

SELECT * FROM DOCTOR_APPOINTMENT_SUMMARY;
