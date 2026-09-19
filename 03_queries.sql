-- ============================================================================
-- PROJECT: HOSPITAL PATIENT RECORD SYSTEM (ORACLE COE PROJECT)
-- SCRIPT: 03_queries.sql
-- PURPOSE: 20 Core SQL Queries Demonstrating Oracle SQL Concepts
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 1: Display all patients
-- Concepts: SELECT, FROM, ORDER BY
-- ----------------------------------------------------------------------------
SELECT 
    patient_id,
    patient_name,
    TO_CHAR(date_of_birth, 'YYYY-MM-DD') AS dob,
    gender,
    blood_group,
    phone,
    email,
    address
FROM PATIENT
ORDER BY patient_id;

-- ----------------------------------------------------------------------------
-- QUERY 2: Display all doctors and their departments
-- Concepts: INNER JOIN, Aliasing, Multi-table Projection
-- ----------------------------------------------------------------------------
SELECT 
    d.doctor_id,
    d.doctor_name,
    d.specialization,
    d.phone,
    d.email,
    dept.department_name,
    dept.location
FROM DOCTOR d
JOIN DEPARTMENT dept ON d.department_id = dept.department_id
ORDER BY d.doctor_id;

-- ----------------------------------------------------------------------------
-- QUERY 3: Display all available hospital departments
-- Concepts: SELECT, Projection, ORDER BY
-- ----------------------------------------------------------------------------
SELECT 
    department_id,
    department_name,
    location
FROM DEPARTMENT
ORDER BY department_id;

-- ----------------------------------------------------------------------------
-- QUERY 4: Display appointments for a particular patient (e.g., patient_id = 1)
-- Concepts: WHERE Filtering, JOIN
-- ----------------------------------------------------------------------------
SELECT 
    a.appointment_id,
    p.patient_name,
    d.doctor_name,
    TO_CHAR(a.appointment_date, 'YYYY-MM-DD') AS appt_date,
    a.appointment_time,
    a.reason,
    a.status
FROM APPOINTMENT a
JOIN PATIENT p ON a.patient_id = p.patient_id
JOIN DOCTOR d ON a.doctor_id = d.doctor_id
WHERE a.patient_id = 1
ORDER BY a.appointment_date DESC;

-- ----------------------------------------------------------------------------
-- QUERY 5: Display appointments for a particular doctor (e.g., doctor_id = 1)
-- Concepts: WHERE Filtering, JOIN
-- ----------------------------------------------------------------------------
SELECT 
    a.appointment_id,
    d.doctor_name,
    p.patient_name,
    TO_CHAR(a.appointment_date, 'YYYY-MM-DD') AS appt_date,
    a.appointment_time,
    a.reason,
    a.status
FROM APPOINTMENT a
JOIN DOCTOR d ON a.doctor_id = d.doctor_id
JOIN PATIENT p ON a.patient_id = p.patient_id
WHERE a.doctor_id = 1
ORDER BY a.appointment_date;

-- ----------------------------------------------------------------------------
-- QUERY 6: Display completed appointments
-- Concepts: WHERE condition with literal match, JOIN
-- ----------------------------------------------------------------------------
SELECT 
    a.appointment_id,
    p.patient_name,
    d.doctor_name,
    TO_CHAR(a.appointment_date, 'YYYY-MM-DD') AS appt_date,
    a.appointment_time,
    a.reason,
    a.status
FROM APPOINTMENT a
JOIN PATIENT p ON a.patient_id = p.patient_id
JOIN DOCTOR d ON a.doctor_id = d.doctor_id
WHERE a.status = 'COMPLETED'
ORDER BY a.appointment_date DESC;

-- ----------------------------------------------------------------------------
-- QUERY 7: Display a patient's medical history (e.g., patient_id = 1)
-- Concepts: Multi-table JOIN (PATIENT, MEDICAL_RECORD, DOCTOR)
-- ----------------------------------------------------------------------------
SELECT 
    mr.record_id,
    p.patient_name,
    d.doctor_name,
    TO_CHAR(mr.record_date, 'YYYY-MM-DD') AS record_date,
    mr.diagnosis,
    mr.treatment,
    mr.notes
FROM MEDICAL_RECORD mr
JOIN PATIENT p ON mr.patient_id = p.patient_id
JOIN DOCTOR d ON mr.doctor_id = d.doctor_id
WHERE mr.patient_id = 1
ORDER BY mr.record_date DESC;

-- ----------------------------------------------------------------------------
-- QUERY 8: Display medicines prescribed to a patient (e.g., patient_id = 1)
-- Concepts: Three-table JOIN (PATIENT, MEDICAL_RECORD, PRESCRIPTION)
-- ----------------------------------------------------------------------------
SELECT 
    p.patient_name,
    mr.record_id,
    mr.diagnosis,
    pr.medicine_name,
    pr.dosage,
    pr.frequency,
    pr.duration_days
FROM PRESCRIPTION pr
JOIN MEDICAL_RECORD mr ON pr.record_id = mr.record_id
JOIN PATIENT p ON mr.patient_id = p.patient_id
WHERE p.patient_id = 1
ORDER BY mr.record_date DESC, pr.prescription_id;

-- ----------------------------------------------------------------------------
-- QUERY 9: Display all pending bills
-- Concepts: Filtering on status flag, Formatted Currency Display
-- ----------------------------------------------------------------------------
SELECT 
    b.bill_id,
    p.patient_name,
    b.appointment_id,
    TO_CHAR(b.bill_date, 'YYYY-MM-DD') AS bill_date,
    b.consultation_fee,
    b.medicine_fee,
    b.total_amount,
    b.payment_status
FROM BILL b
JOIN PATIENT p ON b.patient_id = p.patient_id
WHERE b.payment_status = 'PENDING'
ORDER BY b.bill_date;

-- ----------------------------------------------------------------------------
-- QUERY 10: Calculate the total number of patients
-- Concepts: Aggregate Function COUNT()
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_patients
FROM PATIENT;

-- ----------------------------------------------------------------------------
-- QUERY 11: Count appointments handled by each doctor
-- Concepts: Aggregate Function COUNT(), GROUP BY, JOIN
-- ----------------------------------------------------------------------------
SELECT 
    d.doctor_id,
    d.doctor_name,
    dept.department_name,
    COUNT(a.appointment_id) AS total_appointments
FROM DOCTOR d
JOIN DEPARTMENT dept ON d.department_id = dept.department_id
LEFT JOIN APPOINTMENT a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.doctor_name, dept.department_name
ORDER BY total_appointments DESC, d.doctor_name;

-- ----------------------------------------------------------------------------
-- QUERY 12: Find the number of patients in each department
-- Concepts: DISTINCT COUNT(), Multiple JOINs, GROUP BY
-- ----------------------------------------------------------------------------
SELECT 
    dept.department_id,
    dept.department_name,
    COUNT(DISTINCT a.patient_id) AS unique_patients_served
FROM DEPARTMENT dept
JOIN DOCTOR d ON dept.department_id = d.department_id
LEFT JOIN APPOINTMENT a ON d.doctor_id = a.doctor_id
GROUP BY dept.department_id, dept.department_name
ORDER BY unique_patients_served DESC;

-- ----------------------------------------------------------------------------
-- QUERY 13: Calculate the average consultation fee
-- Concepts: Aggregate Function AVG(), ROUND()
-- ----------------------------------------------------------------------------
SELECT 
    ROUND(AVG(consultation_fee), 2) AS average_consultation_fee
FROM BILL;

-- ----------------------------------------------------------------------------
-- QUERY 14: Find the highest bill amount
-- Concepts: Aggregate Function MAX()
-- ----------------------------------------------------------------------------
SELECT 
    MAX(total_amount) AS highest_bill_amount
FROM BILL;

-- ----------------------------------------------------------------------------
-- QUERY 15: Display patient name, doctor name, appointment date, and status using JOINs
-- Concepts: Multiple INNER JOINs, Date Formatting
-- ----------------------------------------------------------------------------
SELECT 
    p.patient_name,
    d.doctor_name,
    TO_CHAR(a.appointment_date, 'YYYY-MM-DD') AS appointment_date,
    a.appointment_time,
    a.status AS appointment_status
FROM APPOINTMENT a
JOIN PATIENT p ON a.patient_id = p.patient_id
JOIN DOCTOR d ON a.doctor_id = d.doctor_id
ORDER BY a.appointment_date, a.appointment_time;

-- ----------------------------------------------------------------------------
-- QUERY 16: Display patient name, diagnosis, treatment, and doctor name using JOINs
-- Concepts: Multi-table relational linkage
-- ----------------------------------------------------------------------------
SELECT 
    p.patient_name,
    mr.diagnosis,
    mr.treatment,
    d.doctor_name,
    TO_CHAR(mr.record_date, 'YYYY-MM-DD') AS record_date
FROM MEDICAL_RECORD mr
JOIN PATIENT p ON mr.patient_id = p.patient_id
JOIN DOCTOR d ON mr.doctor_id = d.doctor_id
ORDER BY mr.record_date DESC;

-- ----------------------------------------------------------------------------
-- QUERY 17: Find patients who have more than one medical record
-- Concepts: GROUP BY, HAVING, COUNT() Filtering
-- ----------------------------------------------------------------------------
SELECT 
    p.patient_id,
    p.patient_name,
    p.phone,
    COUNT(mr.record_id) AS record_count
FROM PATIENT p
JOIN MEDICAL_RECORD mr ON p.patient_id = mr.patient_id
GROUP BY p.patient_id, p.patient_name, p.phone
HAVING COUNT(mr.record_id) > 1
ORDER BY record_count DESC;

-- ----------------------------------------------------------------------------
-- QUERY 18: Find doctors who have handled more than a specified number of appointments (e.g. > 2)
-- Concepts: GROUP BY, HAVING Clause on aggregated counts
-- ----------------------------------------------------------------------------
SELECT 
    d.doctor_id,
    d.doctor_name,
    d.specialization,
    COUNT(a.appointment_id) AS appointments_handled
FROM DOCTOR d
JOIN APPOINTMENT a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.doctor_name, d.specialization
HAVING COUNT(a.appointment_id) > 2
ORDER BY appointments_handled DESC;

-- ----------------------------------------------------------------------------
-- QUERY 19: Find patients with pending bills
-- Concepts: Subquery with IN operator, DISTINCT
-- ----------------------------------------------------------------------------
SELECT 
    p.patient_id,
    p.patient_name,
    p.phone,
    p.email
FROM PATIENT p
WHERE p.patient_id IN (
    SELECT DISTINCT b.patient_id 
    FROM BILL b 
    WHERE b.payment_status = 'PENDING'
)
ORDER BY p.patient_id;

-- ----------------------------------------------------------------------------
-- QUERY 20: Display the total billing amount for each patient
-- Concepts: SUM(), GROUP BY, LEFT JOIN (includes patients with zero bills)
-- ----------------------------------------------------------------------------
SELECT 
    p.patient_id,
    p.patient_name,
    NVL(SUM(b.total_amount), 0) AS total_billed_amount,
    COUNT(b.bill_id) AS bill_count
FROM PATIENT p
LEFT JOIN BILL b ON p.patient_id = b.patient_id
GROUP BY p.patient_id, p.patient_name
ORDER BY total_billed_amount DESC;
