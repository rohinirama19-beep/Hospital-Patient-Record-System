-- ============================================================================
-- PROJECT: HOSPITAL PATIENT RECORD SYSTEM (ORACLE COE PROJECT)
-- SCRIPT: 07_reports.sql
-- PURPOSE: 5 Core Hospital Operational Reports
-- ============================================================================

-- ----------------------------------------------------------------------------
-- REPORT 1: PATIENT REPORT
-- Fields: Patient ID, Patient Name, Gender, Blood Group, Phone
-- ----------------------------------------------------------------------------
PROMPT ============================================================================
PROMPT REPORT 1: PATIENT DIRECTORY REPORT
PROMPT ============================================================================
SELECT 
    patient_id      AS "Patient ID",
    patient_name    AS "Patient Name",
    gender          AS "Gender",
    blood_group     AS "Blood Group",
    phone           AS "Phone Number"
FROM PATIENT
ORDER BY patient_id;

-- ----------------------------------------------------------------------------
-- REPORT 2: APPOINTMENT REPORT
-- Fields: Patient, Doctor, Department, Appointment Date, Status
-- ----------------------------------------------------------------------------
PROMPT ============================================================================
PROMPT REPORT 2: APPOINTMENT SCHEDULE & STATUS REPORT
PROMPT ============================================================================
SELECT 
    p.patient_name                           AS "Patient",
    d.doctor_name                            AS "Doctor",
    dept.department_name                     AS "Department",
    TO_CHAR(a.appointment_date, 'YYYY-MM-DD') AS "Appointment Date",
    a.status                                 AS "Status"
FROM APPOINTMENT a
JOIN PATIENT p ON a.patient_id = p.patient_id
JOIN DOCTOR d ON a.doctor_id = d.doctor_id
JOIN DEPARTMENT dept ON d.department_id = dept.department_id
ORDER BY a.appointment_date DESC, a.appointment_time;

-- ----------------------------------------------------------------------------
-- REPORT 3: MEDICAL HISTORY REPORT
-- Fields: Patient, Doctor, Diagnosis, Treatment, Record Date
-- ----------------------------------------------------------------------------
PROMPT ============================================================================
PROMPT REPORT 3: PATIENT MEDICAL HISTORY REPORT
PROMPT ============================================================================
SELECT 
    p.patient_name                        AS "Patient",
    d.doctor_name                         AS "Doctor",
    mr.diagnosis                          AS "Diagnosis",
    mr.treatment                          AS "Treatment",
    TO_CHAR(mr.record_date, 'YYYY-MM-DD') AS "Record Date"
FROM MEDICAL_RECORD mr
JOIN PATIENT p ON mr.patient_id = p.patient_id
JOIN DOCTOR d ON mr.doctor_id = d.doctor_id
ORDER BY mr.record_date DESC, p.patient_name;

-- ----------------------------------------------------------------------------
-- REPORT 4: BILL REPORT
-- Fields: Patient, Bill Date, Total Amount, Payment Status
-- ----------------------------------------------------------------------------
PROMPT ============================================================================
PROMPT REPORT 4: BILLING & REVENUE REPORT
PROMPT ============================================================================
SELECT 
    p.patient_name                       AS "Patient",
    TO_CHAR(b.bill_date, 'YYYY-MM-DD')   AS "Bill Date",
    TO_CHAR(b.total_amount, '999,990.00') AS "Total Amount",
    b.payment_status                     AS "Payment Status"
FROM BILL b
JOIN PATIENT p ON b.patient_id = p.patient_id
ORDER BY b.bill_date DESC, b.bill_id;

-- ----------------------------------------------------------------------------
-- REPORT 5: DOCTOR REPORT
-- Fields: Doctor, Specialization, Department, Total Appointments
-- ----------------------------------------------------------------------------
PROMPT ============================================================================
PROMPT REPORT 5: DOCTOR WORKLOAD REPORT
PROMPT ============================================================================
SELECT 
    d.doctor_name           AS "Doctor",
    d.specialization        AS "Specialization",
    dept.department_name    AS "Department",
    COUNT(a.appointment_id) AS "Total Appointments"
FROM DOCTOR d
JOIN DEPARTMENT dept ON d.department_id = dept.department_id
LEFT JOIN APPOINTMENT a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.doctor_name, d.specialization, dept.department_name
ORDER BY "Total Appointments" DESC;
