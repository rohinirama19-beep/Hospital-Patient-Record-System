-- ============================================================================
-- PROJECT: HOSPITAL PATIENT RECORD SYSTEM (ORACLE COE PROJECT)
-- SCRIPT: 02_sample_data.sql
-- PURPOSE: Populates the database with realistic sample data
-- ============================================================================

-- Clean existing data before insert (if re-running)
DELETE FROM PRESCRIPTION;
DELETE FROM BILL;
DELETE FROM MEDICAL_RECORD;
DELETE FROM APPOINTMENT;
DELETE FROM DOCTOR;
DELETE FROM PATIENT;
DELETE FROM DEPARTMENT;

-- ----------------------------------------------------------------------------
-- 1. INSERT DEPARTMENTS (5 Departments)
-- ----------------------------------------------------------------------------
INSERT INTO DEPARTMENT (department_id, department_name, location) 
VALUES (1, 'Cardiology', 'Block A, 3rd Floor');

INSERT INTO DEPARTMENT (department_id, department_name, location) 
VALUES (2, 'General Medicine', 'Block B, 1st Floor');

INSERT INTO DEPARTMENT (department_id, department_name, location) 
VALUES (3, 'Orthopedics', 'Block A, 2nd Floor');

INSERT INTO DEPARTMENT (department_id, department_name, location) 
VALUES (4, 'Pediatrics', 'Block C, 1st Floor');

INSERT INTO DEPARTMENT (department_id, department_name, location) 
VALUES (5, 'Dermatology', 'Block B, 2nd Floor');

-- ----------------------------------------------------------------------------
-- 2. INSERT DOCTORS (6 Doctors across departments)
-- ----------------------------------------------------------------------------
INSERT INTO DOCTOR (doctor_id, doctor_name, specialization, phone, email, department_id)
VALUES (1, 'Dr. Rajesh Sharma', 'Cardiologist', '9876543210', 'rajesh.sharma@hospital.org', 1);

INSERT INTO DOCTOR (doctor_id, doctor_name, specialization, phone, email, department_id)
VALUES (2, 'Dr. Priya Nair', 'Consultant Physician', '9876543211', 'priya.nair@hospital.org', 2);

INSERT INTO DOCTOR (doctor_id, doctor_name, specialization, phone, email, department_id)
VALUES (3, 'Dr. Amit Patel', 'Orthopedic Surgeon', '9876543212', 'amit.patel@hospital.org', 3);

INSERT INTO DOCTOR (doctor_id, doctor_name, specialization, phone, email, department_id)
VALUES (4, 'Dr. Sneha Rao', 'Pediatrician', '9876543213', 'sneha.rao@hospital.org', 4);

INSERT INTO DOCTOR (doctor_id, doctor_name, specialization, phone, email, department_id)
VALUES (5, 'Dr. Vikram Verma', 'Dermatologist', '9876543214', 'vikram.verma@hospital.org', 5);

INSERT INTO DOCTOR (doctor_id, doctor_name, specialization, phone, email, department_id)
VALUES (6, 'Dr. Ananya Iyer', 'Interventional Cardiologist', '9876543215', 'ananya.iyer@hospital.org', 1);

-- ----------------------------------------------------------------------------
-- 3. INSERT PATIENTS (10 Patients)
-- ----------------------------------------------------------------------------
INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at)
VALUES (1, 'Aarav Mehta', TO_DATE('1990-05-15', 'YYYY-MM-DD'), 'MALE', '9811122201', 'aarav.mehta@email.com', '12 Park Avenue, Mumbai', 'O+', TO_DATE('2026-01-10', 'YYYY-MM-DD'));

INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at)
VALUES (2, 'Diya Sen', TO_DATE('1985-08-22', 'YYYY-MM-DD'), 'FEMALE', '9811122202', 'diya.sen@email.com', '45 Lake Road, Kolkata', 'A+', TO_DATE('2026-01-12', 'YYYY-MM-DD'));

INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at)
VALUES (3, 'Rohan Gupta', TO_DATE('1998-11-03', 'YYYY-MM-DD'), 'MALE', '9811122203', 'rohan.gupta@email.com', '78 MG Road, Bangalore', 'B+', TO_DATE('2026-01-15', 'YYYY-MM-DD'));

INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at)
VALUES (4, 'Kavita Joshi', TO_DATE('1975-02-18', 'YYYY-MM-DD'), 'FEMALE', '9811122204', 'kavita.joshi@email.com', '19 Ring Road, Delhi', 'AB+', TO_DATE('2026-01-20', 'YYYY-MM-DD'));

INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at)
VALUES (5, 'Arjun Reddy', TO_DATE('2002-07-29', 'YYYY-MM-DD'), 'MALE', '9811122205', 'arjun.reddy@email.com', '88 Jubilee Hills, Hyderabad', 'O-', TO_DATE('2026-02-01', 'YYYY-MM-DD'));

INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at)
VALUES (6, 'Meera Nambiar', TO_DATE('1993-12-10', 'YYYY-MM-DD'), 'FEMALE', '9811122206', 'meera.nambiar@email.com', '34 Marine Drive, Kochi', 'A-', TO_DATE('2026-02-05', 'YYYY-MM-DD'));

INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at)
VALUES (7, 'Sanjay Kapoor', TO_DATE('1968-04-05', 'YYYY-MM-DD'), 'MALE', '9811122207', 'sanjay.kapoor@email.com', '102 Sector 14, Gurgaon', 'B-', TO_DATE('2026-02-10', 'YYYY-MM-DD'));

INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at)
VALUES (8, 'Pooja Bhatt', TO_DATE('2005-09-14', 'YYYY-MM-DD'), 'FEMALE', '9811122208', 'pooja.bhatt@email.com', '56 Civil Lines, Jaipur', 'AB-', TO_DATE('2026-02-15', 'YYYY-MM-DD'));

INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at)
VALUES (9, 'Nikhil Das', TO_DATE('1988-03-30', 'YYYY-MM-DD'), 'MALE', '9811122209', 'nikhil.das@email.com', '23 Salt Lake, Kolkata', 'O+', TO_DATE('2026-02-18', 'YYYY-MM-DD'));

INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group, created_at)
VALUES (10, 'Sunita Deshmukh', TO_DATE('1982-06-25', 'YYYY-MM-DD'), 'FEMALE', '9811122210', 'sunita.deshmukh@email.com', '67 FC Road, Pune', 'B+', TO_DATE('2026-02-20', 'YYYY-MM-DD'));

-- ----------------------------------------------------------------------------
-- 4. INSERT APPOINTMENTS (15 Appointments: 10 COMPLETED, 3 SCHEDULED, 2 CANCELLED)
-- ----------------------------------------------------------------------------
INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (1, 1, 1, TO_DATE('2026-02-01', 'YYYY-MM-DD'), '09:30 AM', 'Chest pain & shortness of breath', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (2, 2, 2, TO_DATE('2026-02-02', 'YYYY-MM-DD'), '10:00 AM', 'High fever and persistent cough', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (3, 3, 3, TO_DATE('2026-02-03', 'YYYY-MM-DD'), '11:00 AM', 'Severe knee joint pain', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (4, 4, 1, TO_DATE('2026-02-04', 'YYYY-MM-DD'), '02:00 PM', 'High blood pressure checkup', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (5, 5, 4, TO_DATE('2026-02-05', 'YYYY-MM-DD'), '03:30 PM', 'Pediatric allergy consultation', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (6, 6, 5, TO_DATE('2026-02-06', 'YYYY-MM-DD'), '10:30 AM', 'Eczema rash on arms', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (7, 7, 2, TO_DATE('2026-02-07', 'YYYY-MM-DD'), '11:30 AM', 'Type 2 Diabetes follow-up', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (8, 8, 3, TO_DATE('2026-02-08', 'YYYY-MM-DD'), '04:00 PM', 'Wrist sprain after sports activity', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (9, 1, 1, TO_DATE('2026-02-15', 'YYYY-MM-DD'), '10:00 AM', 'Cardiology post-medication review', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (10, 2, 2, TO_DATE('2026-02-16', 'YYYY-MM-DD'), '11:15 AM', 'Flu recovery follow-up', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (11, 3, 3, TO_DATE('2026-02-18', 'YYYY-MM-DD'), '02:30 PM', 'Knee physiotherapy evaluation', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (12, 9, 6, TO_DATE('2026-02-20', 'YYYY-MM-DD'), '03:00 PM', 'Heart palpitations assessment', 'COMPLETED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (13, 10, 5, TO_DATE('2026-03-01', 'YYYY-MM-DD'), '09:00 AM', 'Skin pigmentation evaluation', 'SCHEDULED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (14, 4, 1, TO_DATE('2026-03-02', 'YYYY-MM-DD'), '02:00 PM', 'Routine ECG follow-up', 'SCHEDULED');

INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
VALUES (15, 7, 4, TO_DATE('2026-02-22', 'YYYY-MM-DD'), '04:30 PM', 'General pediatric consultation', 'CANCELLED');

-- ----------------------------------------------------------------------------
-- 5. INSERT MEDICAL RECORDS (12 Medical Records)
-- (Patients 1, 2, 3 have multiple records)
-- ----------------------------------------------------------------------------
INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (1, 1, 1, 1, 'Angina Pectoris', 'Nitroglycerin sublingual, lifestyle modification', TO_DATE('2026-02-01', 'YYYY-MM-DD'), 'Patient advised to avoid strenuous physical exertion.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (2, 2, 2, 2, 'Acute Bronchitis', 'Antibiotic therapy, cough syrup, steam inhalation', TO_DATE('2026-02-02', 'YYYY-MM-DD'), 'Vitals stable. Throat culture clear.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (3, 3, 3, 3, 'Osteoarthritis of Knee', 'NSAID therapy, physiotherapy, knee brace', TO_DATE('2026-02-03', 'YYYY-MM-DD'), 'Moderate cartilage loss on right knee X-ray.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (4, 4, 1, 4, 'Stage 1 Essential Hypertension', 'Antihypertensive medication and low-sodium diet', TO_DATE('2026-02-04', 'YYYY-MM-DD'), 'BP reading 148/92 mmHg at rest.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (5, 5, 4, 5, 'Allergic Rhinitis', 'Antihistamines, nasal corticosteroid spray', TO_DATE('2026-02-05', 'YYYY-MM-DD'), 'Seasonal environmental allergy identified.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (6, 6, 5, 6, 'Atopic Dermatitis', 'Topical corticosteroid ointment, emollients', TO_DATE('2026-02-06', 'YYYY-MM-DD'), 'Mild pruritus reported. Avoid harsh soaps.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (7, 7, 2, 7, 'Type 2 Diabetes Mellitus', 'Oral hypoglycemic agent, dietary regimen', TO_DATE('2026-02-07', 'YYYY-MM-DD'), 'HbA1c level recorded at 7.4%.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (8, 8, 3, 8, 'Grade 1 Wrist Ligament Sprain', 'RICE protocol, elastic bandage splint', TO_DATE('2026-02-08', 'YYYY-MM-DD'), 'No fracture observed on radiography.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (9, 1, 1, 9, 'Coronary Artery Follow-up', 'Maintenance Statin & Beta-blocker therapy', TO_DATE('2026-02-15', 'YYYY-MM-DD'), 'Patient reports marked reduction in chest discomfort.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (10, 2, 2, 10, 'Post-Viral Fatigue', 'Multivitamin supplement, hydration', TO_DATE('2026-02-16', 'YYYY-MM-DD'), 'Chest auscultation clear. Lungs fully recovered.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (11, 3, 3, 11, 'Knee Rehabilitation Review', 'Quadriceps strengthening exercises', TO_DATE('2026-02-18', 'YYYY-MM-DD'), 'Mobility improved by 40%. Continuing PT.');

INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date, notes)
VALUES (12, 9, 6, 12, 'Sinus Tachycardia', 'Cardio selective beta-blocker, stress management', TO_DATE('2026-02-20', 'YYYY-MM-DD'), 'Holter monitoring shows normal sinus rhythm.');

-- ----------------------------------------------------------------------------
-- 6. INSERT PRESCRIPTIONS (15 Prescriptions)
-- ----------------------------------------------------------------------------
INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (1, 1, 'Nitroglycerin', '0.4 mg', 'As needed for chest pain', 30);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (2, 1, 'Aspirin', '75 mg', 'Once daily post breakfast', 60);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (3, 2, 'Amoxicillin', '500 mg', 'Three times daily', 7);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (4, 2, 'Guaifenesin Syrup', '10 ml', 'Twice daily', 5);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (5, 3, 'Ibuprofen', '400 mg', 'Twice daily after meals', 14);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (6, 3, 'Glucosamine Sulfate', '500 mg', 'Once daily', 30);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (7, 4, 'Amlodipine', '5 mg', 'Once daily morning', 30);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (8, 5, 'Cetirizine', '10 mg', 'Once daily at bedtime', 10);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (9, 5, 'Fluticasone Nasal Spray', '50 mcg', '1 spray per nostril daily', 15);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (10, 6, 'Hydrocortisone Cream 1%', 'Topical', 'Apply twice daily', 14);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (11, 7, 'Metformin', '500 mg', 'Twice daily with meals', 60);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (12, 8, 'Paracetamol', '650 mg', 'Every 8 hours as needed', 5);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (13, 9, 'Atorvastatin', '20 mg', 'Once daily at night', 90);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (14, 10, 'Vitamin B-Complex', '1 Tablet', 'Once daily morning', 30);

INSERT INTO PRESCRIPTION (prescription_id, record_id, medicine_name, dosage, frequency, duration_days)
VALUES (15, 12, 'Metoprolol', '25 mg', 'Once daily', 30);

-- ----------------------------------------------------------------------------
-- 7. INSERT BILLS (12 Bills: consultation + medicine fees, PAID & PENDING)
-- ----------------------------------------------------------------------------
INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (1, 1, 1, TO_DATE('2026-02-01', 'YYYY-MM-DD'), 800.00, 350.00, 1150.00, 'PAID');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (2, 2, 2, TO_DATE('2026-02-02', 'YYYY-MM-DD'), 500.00, 280.00, 780.00, 'PAID');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (3, 3, 3, TO_DATE('2026-02-03', 'YYYY-MM-DD'), 750.00, 420.00, 1170.00, 'PENDING');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (4, 4, 4, TO_DATE('2026-02-04', 'YYYY-MM-DD'), 800.00, 180.00, 980.00, 'PAID');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (5, 5, 5, TO_DATE('2026-02-05', 'YYYY-MM-DD'), 600.00, 220.00, 820.00, 'PAID');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (6, 6, 6, TO_DATE('2026-02-06', 'YYYY-MM-DD'), 650.00, 310.00, 960.00, 'PENDING');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (7, 7, 7, TO_DATE('2026-02-07', 'YYYY-MM-DD'), 500.00, 450.00, 950.00, 'PAID');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (8, 8, 8, TO_DATE('2026-02-08', 'YYYY-MM-DD'), 750.00, 120.00, 870.00, 'PAID');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (9, 1, 9, TO_DATE('2026-02-15', 'YYYY-MM-DD'), 600.00, 520.00, 1120.00, 'PAID');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (10, 2, 10, TO_DATE('2026-02-16', 'YYYY-MM-DD'), 400.00, 150.00, 550.00, 'PENDING');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (11, 3, 11, TO_DATE('2026-02-18', 'YYYY-MM-DD'), 500.00, 0.00, 500.00, 'PAID');

INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
VALUES (12, 9, 12, TO_DATE('2026-02-20', 'YYYY-MM-DD'), 900.00, 290.00, 1190.00, 'PAID');

COMMIT;
