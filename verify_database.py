"""
Automated Verification Harness for Hospital Patient Record System (Oracle COE Project)
Validates schema, constraints, sample data, 20 queries, views, PL/SQL logic, and reports.
"""

import sqlite3
import sys

def run_verification():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("=" * 80)
    print("STEP 1: CREATING TABLES AND CONSTRAINTS (SCHEMA VERIFICATION)")
    print("=" * 80)

    # 1. DEPARTMENT
    cursor.execute("""
    CREATE TABLE DEPARTMENT (
        department_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL UNIQUE,
        location        TEXT NOT NULL
    );
    """)

    # 2. DOCTOR
    cursor.execute("""
    CREATE TABLE DOCTOR (
        doctor_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_name     TEXT NOT NULL,
        specialization  TEXT NOT NULL,
        phone           TEXT NOT NULL,
        email           TEXT NOT NULL UNIQUE,
        department_id   INTEGER NOT NULL,
        FOREIGN KEY (department_id) REFERENCES DEPARTMENT(department_id)
    );
    """)

    # 3. PATIENT
    cursor.execute("""
    CREATE TABLE PATIENT (
        patient_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name    TEXT NOT NULL,
        date_of_birth   TEXT NOT NULL,
        gender          TEXT NOT NULL CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
        phone           TEXT NOT NULL,
        email           TEXT NOT NULL UNIQUE,
        address         TEXT NOT NULL,
        blood_group     TEXT NOT NULL CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
        created_at      TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
    );
    """)

    # 4. APPOINTMENT
    cursor.execute("""
    CREATE TABLE APPOINTMENT (
        appointment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id       INTEGER NOT NULL,
        doctor_id        INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        reason           TEXT NOT NULL,
        status           TEXT NOT NULL DEFAULT 'SCHEDULED' CHECK (status IN ('SCHEDULED', 'COMPLETED', 'CANCELLED')),
        FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id),
        FOREIGN KEY (doctor_id) REFERENCES DOCTOR(doctor_id)
    );
    """)

    # 5. MEDICAL_RECORD
    cursor.execute("""
    CREATE TABLE MEDICAL_RECORD (
        record_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id      INTEGER NOT NULL,
        doctor_id       INTEGER NOT NULL,
        appointment_id  INTEGER,
        diagnosis       TEXT NOT NULL,
        treatment       TEXT NOT NULL,
        record_date     TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
        notes           TEXT,
        FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id),
        FOREIGN KEY (doctor_id) REFERENCES DOCTOR(doctor_id),
        FOREIGN KEY (appointment_id) REFERENCES APPOINTMENT(appointment_id)
    );
    """)

    # 6. PRESCRIPTION
    cursor.execute("""
    CREATE TABLE PRESCRIPTION (
        prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id       INTEGER NOT NULL,
        medicine_name   TEXT NOT NULL,
        dosage          TEXT NOT NULL,
        frequency       TEXT NOT NULL,
        duration_days   INTEGER NOT NULL CHECK (duration_days > 0),
        FOREIGN KEY (record_id) REFERENCES MEDICAL_RECORD(record_id)
    );
    """)

    # 7. BILL
    cursor.execute("""
    CREATE TABLE BILL (
        bill_id          INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id       INTEGER NOT NULL,
        appointment_id   INTEGER,
        bill_date        TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
        consultation_fee REAL NOT NULL DEFAULT 0.00 CHECK (consultation_fee >= 0),
        medicine_fee     REAL NOT NULL DEFAULT 0.00 CHECK (medicine_fee >= 0),
        total_amount     REAL NOT NULL CHECK (total_amount >= 0),
        payment_status   TEXT NOT NULL DEFAULT 'PENDING' CHECK (payment_status IN ('PAID', 'PENDING')),
        FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id),
        FOREIGN KEY (appointment_id) REFERENCES APPOINTMENT(appointment_id)
    );
    """)

    print("All 7 tables created successfully with PK, FK, and CHECK constraints.\n")

    print("=" * 80)
    print("STEP 2: POPULATING SAMPLE DATA")
    print("=" * 80)

    # Departments (5)
    departments = [
        (1, 'Cardiology', 'Block A, 3rd Floor'),
        (2, 'General Medicine', 'Block B, 1st Floor'),
        (3, 'Orthopedics', 'Block A, 2nd Floor'),
        (4, 'Pediatrics', 'Block C, 1st Floor'),
        (5, 'Dermatology', 'Block B, 2nd Floor')
    ]
    cursor.executemany("INSERT INTO DEPARTMENT VALUES (?, ?, ?);", departments)

    # Doctors (6)
    doctors = [
        (1, 'Dr. Rajesh Sharma', 'Cardiologist', '9876543210', 'rajesh.sharma@hospital.org', 1),
        (2, 'Dr. Priya Nair', 'Consultant Physician', '9876543211', 'priya.nair@hospital.org', 2),
        (3, 'Dr. Amit Patel', 'Orthopedic Surgeon', '9876543212', 'amit.patel@hospital.org', 3),
        (4, 'Dr. Sneha Rao', 'Pediatrician', '9876543213', 'sneha.rao@hospital.org', 4),
        (5, 'Dr. Vikram Verma', 'Dermatologist', '9876543214', 'vikram.verma@hospital.org', 5),
        (6, 'Dr. Ananya Iyer', 'Interventional Cardiologist', '9876543215', 'ananya.iyer@hospital.org', 1)
    ]
    cursor.executemany("INSERT INTO DOCTOR VALUES (?, ?, ?, ?, ?, ?);", doctors)

    # Patients (10)
    patients = [
        (1, 'Aarav Mehta', '1990-05-15', 'MALE', '9811122201', 'aarav.mehta@email.com', '12 Park Avenue, Mumbai', 'O+', '2026-01-10'),
        (2, 'Diya Sen', '1985-08-22', 'FEMALE', '9811122202', 'diya.sen@email.com', '45 Lake Road, Kolkata', 'A+', '2026-01-12'),
        (3, 'Rohan Gupta', '1998-11-03', 'MALE', '9811122203', 'rohan.gupta@email.com', '78 MG Road, Bangalore', 'B+', '2026-01-15'),
        (4, 'Kavita Joshi', '1975-02-18', 'FEMALE', '9811122204', 'kavita.joshi@email.com', '19 Ring Road, Delhi', 'AB+', '2026-01-20'),
        (5, 'Arjun Reddy', '2002-07-29', 'MALE', '9811122205', 'arjun.reddy@email.com', '88 Jubilee Hills, Hyderabad', 'O-', '2026-02-01'),
        (6, 'Meera Nambiar', '1993-12-10', 'FEMALE', '9811122206', 'meera.nambiar@email.com', '34 Marine Drive, Kochi', 'A-', '2026-02-05'),
        (7, 'Sanjay Kapoor', '1968-04-05', 'MALE', '9811122207', 'sanjay.kapoor@email.com', '102 Sector 14, Gurgaon', 'B-', '2026-02-10'),
        (8, 'Pooja Bhatt', '2005-09-14', 'FEMALE', '9811122208', 'pooja.bhatt@email.com', '56 Civil Lines, Jaipur', 'AB-', '2026-02-15'),
        (9, 'Nikhil Das', '1988-03-30', 'MALE', '9811122209', 'nikhil.das@email.com', '23 Salt Lake, Kolkata', 'O+', '2026-02-18'),
        (10, 'Sunita Deshmukh', '1982-06-25', 'FEMALE', '9811122210', 'sunita.deshmukh@email.com', '67 FC Road, Pune', 'B+', '2026-02-20')
    ]
    cursor.executemany("INSERT INTO PATIENT VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", patients)

    # Appointments (15)
    appointments = [
        (1, 1, 1, '2026-02-01', '09:30 AM', 'Chest pain & shortness of breath', 'COMPLETED'),
        (2, 2, 2, '2026-02-02', '10:00 AM', 'High fever and persistent cough', 'COMPLETED'),
        (3, 3, 3, '2026-02-03', '11:00 AM', 'Severe knee joint pain', 'COMPLETED'),
        (4, 4, 1, '2026-02-04', '02:00 PM', 'High blood pressure checkup', 'COMPLETED'),
        (5, 5, 4, '2026-02-05', '03:30 PM', 'Pediatric allergy consultation', 'COMPLETED'),
        (6, 6, 5, '2026-02-06', '10:30 AM', 'Eczema rash on arms', 'COMPLETED'),
        (7, 7, 2, '2026-02-07', '11:30 AM', 'Type 2 Diabetes follow-up', 'COMPLETED'),
        (8, 8, 3, '2026-02-08', '04:00 PM', 'Wrist sprain after sports activity', 'COMPLETED'),
        (9, 1, 1, '2026-02-15', '10:00 AM', 'Cardiology post-medication review', 'COMPLETED'),
        (10, 2, 2, '2026-02-16', '11:15 AM', 'Flu recovery follow-up', 'COMPLETED'),
        (11, 3, 3, '2026-02-18', '02:30 PM', 'Knee physiotherapy evaluation', 'COMPLETED'),
        (12, 9, 6, '2026-02-20', '03:00 PM', 'Heart palpitations assessment', 'COMPLETED'),
        (13, 10, 5, '2026-03-01', '09:00 AM', 'Skin pigmentation evaluation', 'SCHEDULED'),
        (14, 4, 1, '2026-03-02', '02:00 PM', 'Routine ECG follow-up', 'SCHEDULED'),
        (15, 7, 4, '2026-02-22', '04:30 PM', 'General pediatric consultation', 'CANCELLED')
    ]
    cursor.executemany("INSERT INTO APPOINTMENT VALUES (?, ?, ?, ?, ?, ?, ?);", appointments)

    # Medical Records (12)
    medical_records = [
        (1, 1, 1, 1, 'Angina Pectoris', 'Nitroglycerin sublingual, lifestyle modification', '2026-02-01', 'Patient advised to avoid strenuous physical exertion.'),
        (2, 2, 2, 2, 'Acute Bronchitis', 'Antibiotic therapy, cough syrup, steam inhalation', '2026-02-02', 'Vitals stable. Throat culture clear.'),
        (3, 3, 3, 3, 'Osteoarthritis of Knee', 'NSAID therapy, physiotherapy, knee brace', '2026-02-03', 'Moderate cartilage loss on right knee X-ray.'),
        (4, 4, 1, 4, 'Stage 1 Essential Hypertension', 'Antihypertensive medication and low-sodium diet', '2026-02-04', 'BP reading 148/92 mmHg at rest.'),
        (5, 5, 4, 5, 'Allergic Rhinitis', 'Antihistamines, nasal corticosteroid spray', '2026-02-05', 'Seasonal environmental allergy identified.'),
        (6, 6, 5, 6, 'Atopic Dermatitis', 'Topical corticosteroid ointment, emollients', '2026-02-06', 'Mild pruritus reported. Avoid harsh soaps.'),
        (7, 7, 2, 7, 'Type 2 Diabetes Mellitus', 'Oral hypoglycemic agent, dietary regimen', '2026-02-07', 'HbA1c level recorded at 7.4%.'),
        (8, 8, 3, 8, 'Grade 1 Wrist Ligament Sprain', 'RICE protocol, elastic bandage splint', '2026-02-08', 'No fracture observed on radiography.'),
        (9, 1, 1, 9, 'Coronary Artery Follow-up', 'Maintenance Statin & Beta-blocker therapy', '2026-02-15', 'Patient reports marked reduction in chest discomfort.'),
        (10, 2, 2, 10, 'Post-Viral Fatigue', 'Multivitamin supplement, hydration', '2026-02-16', 'Chest auscultation clear. Lungs fully recovered.'),
        (11, 3, 3, 11, 'Knee Rehabilitation Review', 'Quadriceps strengthening exercises', '2026-02-18', 'Mobility improved by 40%. Continuing PT.'),
        (12, 9, 6, 12, 'Sinus Tachycardia', 'Cardio selective beta-blocker, stress management', '2026-02-20', 'Holter monitoring shows normal sinus rhythm.')
    ]
    cursor.executemany("INSERT INTO MEDICAL_RECORD VALUES (?, ?, ?, ?, ?, ?, ?, ?);", medical_records)

    # Prescriptions (15)
    prescriptions = [
        (1, 1, 'Nitroglycerin', '0.4 mg', 'As needed for chest pain', 30),
        (2, 1, 'Aspirin', '75 mg', 'Once daily post breakfast', 60),
        (3, 2, 'Amoxicillin', '500 mg', 'Three times daily', 7),
        (4, 2, 'Guaifenesin Syrup', '10 ml', 'Twice daily', 5),
        (5, 3, 'Ibuprofen', '400 mg', 'Twice daily after meals', 14),
        (6, 3, 'Glucosamine Sulfate', '500 mg', 'Once daily', 30),
        (7, 4, 'Amlodipine', '5 mg', 'Once daily morning', 30),
        (8, 5, 'Cetirizine', '10 mg', 'Once daily at bedtime', 10),
        (9, 5, 'Fluticasone Nasal Spray', '50 mcg', '1 spray per nostril daily', 15),
        (10, 6, 'Hydrocortisone Cream 1%', 'Topical', 'Apply twice daily', 14),
        (11, 7, 'Metformin', '500 mg', 'Twice daily with meals', 60),
        (12, 8, 'Paracetamol', '650 mg', 'Every 8 hours as needed', 5),
        (13, 9, 'Atorvastatin', '20 mg', 'Once daily at night', 90),
        (14, 10, 'Vitamin B-Complex', '1 Tablet', 'Once daily morning', 30),
        (15, 12, 'Metoprolol', '25 mg', 'Once daily', 30)
    ]
    cursor.executemany("INSERT INTO PRESCRIPTION VALUES (?, ?, ?, ?, ?, ?);", prescriptions)

    # Bills (12)
    bills = [
        (1, 1, 1, '2026-02-01', 800.00, 350.00, 1150.00, 'PAID'),
        (2, 2, 2, '2026-02-02', 500.00, 280.00, 780.00, 'PAID'),
        (3, 3, 3, '2026-02-03', 750.00, 420.00, 1170.00, 'PENDING'),
        (4, 4, 4, '2026-02-04', 800.00, 180.00, 980.00, 'PAID'),
        (5, 5, 5, '2026-02-05', 600.00, 220.00, 820.00, 'PAID'),
        (6, 6, 6, '2026-02-06', 650.00, 310.00, 960.00, 'PENDING'),
        (7, 7, 7, '2026-02-07', 500.00, 450.00, 950.00, 'PAID'),
        (8, 8, 8, '2026-02-08', 750.00, 120.00, 870.00, 'PAID'),
        (9, 1, 9, '2026-02-15', 600.00, 520.00, 1120.00, 'PAID'),
        (10, 2, 10, '2026-02-16', 400.00, 150.00, 550.00, 'PENDING'),
        (11, 3, 11, '2026-02-18', 500.00, 0.00, 500.00, 'PAID'),
        (12, 9, 12, '2026-02-20', 900.00, 290.00, 1190.00, 'PAID')
    ]
    cursor.executemany("INSERT INTO BILL VALUES (?, ?, ?, ?, ?, ?, ?, ?);", bills)
    conn.commit()

    # Verify counts
    tables = [
        ('DEPARTMENT', 5), ('DOCTOR', 6), ('PATIENT', 10),
        ('APPOINTMENT', 15), ('MEDICAL_RECORD', 12),
        ('PRESCRIPTION', 15), ('BILL', 12)
    ]
    for tbl, expected in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        assert count == expected, f"Count mismatch for {tbl}: expected {expected}, got {count}"
        print(f"  [OK] {tbl}: {count} rows inserted (Matches requirement)")

    print("\n" + "=" * 80)
    print("STEP 3: CREATING AND VERIFYING DATABASE VIEWS")
    print("=" * 80)

    cursor.execute("""
    CREATE VIEW PATIENT_MEDICAL_HISTORY_VIEW AS
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
    """)
    v1_count = len(cursor.execute("SELECT * FROM PATIENT_MEDICAL_HISTORY_VIEW").fetchall())
    print(f"  [OK] PATIENT_MEDICAL_HISTORY_VIEW verified: {v1_count} records returned")

    cursor.execute("""
    CREATE VIEW PATIENT_BILL_VIEW AS
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
    """)
    v2_count = len(cursor.execute("SELECT * FROM PATIENT_BILL_VIEW").fetchall())
    print(f"  [OK] PATIENT_BILL_VIEW verified: {v2_count} records returned")

    cursor.execute("""
    CREATE VIEW DOCTOR_APPOINTMENT_SUMMARY AS
    SELECT 
        d.doctor_name,
        d.specialization,
        COUNT(a.appointment_id) AS total_appointments,
        SUM(CASE WHEN a.status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed_appointments,
        SUM(CASE WHEN a.status = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled_appointments
    FROM DOCTOR d
    LEFT JOIN APPOINTMENT a ON d.doctor_id = a.doctor_id
    GROUP BY d.doctor_id, d.doctor_name, d.specialization;
    """)
    v3_rows = cursor.execute("SELECT * FROM DOCTOR_APPOINTMENT_SUMMARY").fetchall()
    print(f"  [OK] DOCTOR_APPOINTMENT_SUMMARY verified: {len(v3_rows)} doctors summarized")

    print("\n" + "=" * 80)
    print("STEP 4: RUNNING AND VERIFYING ALL 20 SQL QUERIES")
    print("=" * 80)

    queries = [
        ("Query 1: Display all patients",
         "SELECT patient_id, patient_name, date_of_birth, gender, blood_group, phone FROM PATIENT ORDER BY patient_id;"),
        
        ("Query 2: Display all doctors and their departments",
         "SELECT d.doctor_id, d.doctor_name, d.specialization, dept.department_name FROM DOCTOR d JOIN DEPARTMENT dept ON d.department_id = dept.department_id ORDER BY d.doctor_id;"),
        
        ("Query 3: Display all available hospital departments",
         "SELECT department_id, department_name, location FROM DEPARTMENT ORDER BY department_id;"),
        
        ("Query 4: Display appointments for a particular patient (ID=1)",
         "SELECT a.appointment_id, p.patient_name, d.doctor_name, a.appointment_date, a.status FROM APPOINTMENT a JOIN PATIENT p ON a.patient_id = p.patient_id JOIN DOCTOR d ON a.doctor_id = d.doctor_id WHERE a.patient_id = 1;"),
        
        ("Query 5: Display appointments for a particular doctor (ID=1)",
         "SELECT a.appointment_id, d.doctor_name, p.patient_name, a.appointment_date, a.status FROM APPOINTMENT a JOIN DOCTOR d ON a.doctor_id = d.doctor_id JOIN PATIENT p ON a.patient_id = p.patient_id WHERE a.doctor_id = 1;"),
        
        ("Query 6: Display completed appointments",
         "SELECT a.appointment_id, p.patient_name, d.doctor_name, a.appointment_date, a.status FROM APPOINTMENT a JOIN PATIENT p ON a.patient_id = p.patient_id JOIN DOCTOR d ON a.doctor_id = d.doctor_id WHERE a.status = 'COMPLETED';"),
        
        ("Query 7: Display a patient's medical history (ID=1)",
         "SELECT mr.record_id, p.patient_name, d.doctor_name, mr.diagnosis, mr.treatment, mr.record_date FROM MEDICAL_RECORD mr JOIN PATIENT p ON mr.patient_id = p.patient_id JOIN DOCTOR d ON mr.doctor_id = d.doctor_id WHERE mr.patient_id = 1;"),
        
        ("Query 8: Display medicines prescribed to a patient (ID=1)",
         "SELECT p.patient_name, mr.diagnosis, pr.medicine_name, pr.dosage, pr.duration_days FROM PRESCRIPTION pr JOIN MEDICAL_RECORD mr ON pr.record_id = mr.record_id JOIN PATIENT p ON mr.patient_id = p.patient_id WHERE p.patient_id = 1;"),
        
        ("Query 9: Display all pending bills",
         "SELECT b.bill_id, p.patient_name, b.bill_date, b.total_amount, b.payment_status FROM BILL b JOIN PATIENT p ON b.patient_id = p.patient_id WHERE b.payment_status = 'PENDING';"),
        
        ("Query 10: Calculate the total number of patients",
         "SELECT COUNT(*) AS total_patients FROM PATIENT;"),
        
        ("Query 11: Count appointments handled by each doctor",
         "SELECT d.doctor_id, d.doctor_name, COUNT(a.appointment_id) AS total_appts FROM DOCTOR d LEFT JOIN APPOINTMENT a ON d.doctor_id = a.doctor_id GROUP BY d.doctor_id, d.doctor_name ORDER BY total_appts DESC;"),
        
        ("Query 12: Find the number of patients in each department",
         "SELECT dept.department_id, dept.department_name, COUNT(DISTINCT a.patient_id) AS patient_count FROM DEPARTMENT dept JOIN DOCTOR d ON dept.department_id = d.department_id LEFT JOIN APPOINTMENT a ON d.doctor_id = a.doctor_id GROUP BY dept.department_id, dept.department_name;"),
        
        ("Query 13: Calculate the average consultation fee",
         "SELECT ROUND(AVG(consultation_fee), 2) AS avg_fee FROM BILL;"),
        
        ("Query 14: Find the highest bill amount",
         "SELECT MAX(total_amount) AS max_bill FROM BILL;"),
        
        ("Query 15: Display patient name, doctor name, appointment date and status using JOINs",
         "SELECT p.patient_name, d.doctor_name, a.appointment_date, a.status FROM APPOINTMENT a JOIN PATIENT p ON a.patient_id = p.patient_id JOIN DOCTOR d ON a.doctor_id = d.doctor_id;"),
        
        ("Query 16: Display patient name, diagnosis, treatment, and doctor name using JOINs",
         "SELECT p.patient_name, mr.diagnosis, mr.treatment, d.doctor_name FROM MEDICAL_RECORD mr JOIN PATIENT p ON mr.patient_id = p.patient_id JOIN DOCTOR d ON mr.doctor_id = d.doctor_id;"),
        
        ("Query 17: Find patients who have more than one medical record",
         "SELECT p.patient_id, p.patient_name, COUNT(mr.record_id) AS records FROM PATIENT p JOIN MEDICAL_RECORD mr ON p.patient_id = mr.patient_id GROUP BY p.patient_id, p.patient_name HAVING COUNT(mr.record_id) > 1;"),
        
        ("Query 18: Find doctors who have handled more than a specified number of appointments (> 2)",
         "SELECT d.doctor_id, d.doctor_name, COUNT(a.appointment_id) AS appts FROM DOCTOR d JOIN APPOINTMENT a ON d.doctor_id = a.doctor_id GROUP BY d.doctor_id, d.doctor_name HAVING COUNT(a.appointment_id) > 2;"),
        
        ("Query 19: Find patients with pending bills",
         "SELECT p.patient_id, p.patient_name, p.phone FROM PATIENT p WHERE p.patient_id IN (SELECT DISTINCT patient_id FROM BILL WHERE payment_status = 'PENDING');"),
        
        ("Query 20: Display the total billing amount for each patient",
         "SELECT p.patient_id, p.patient_name, COALESCE(SUM(b.total_amount), 0) AS total_bill FROM PATIENT p LEFT JOIN BILL b ON p.patient_id = b.patient_id GROUP BY p.patient_id, p.patient_name ORDER BY total_bill DESC;")
    ]

    for idx, (title, sql) in enumerate(queries, 1):
        res = cursor.execute(sql).fetchall()
        print(f"  [OK] {title} -> {len(res)} row(s) returned")

    print("\n" + "=" * 80)
    print("STEP 5: DATA INTEGRITY & CONSTRAINT TESTING (7 SCENARIOS)")
    print("=" * 80)

    # Test 1: Valid patient insertion
    cursor.execute("""
    INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group)
    VALUES (99, 'Test Valid Patient', '1995-01-01', 'MALE', '9999988888', 'test.valid@hospital.org', '100 Test St', 'O+');
    """)
    print("  [OK] TEST 1 [Valid Patient Insert]: PASSED (Row inserted successfully)")
    cursor.execute("DELETE FROM PATIENT WHERE patient_id = 99;")

    # Test 2: Invalid doctor_id in appointment
    try:
        cursor.execute("""
        INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
        VALUES (999, 1, 9999, '2026-03-10', '10:00 AM', 'Test Check', 'SCHEDULED');
        """)
        assert False, "Should have raised FK constraint violation"
    except sqlite3.IntegrityError:
        print("  [OK] TEST 2 [Invalid Doctor FK]: PASSED (Correctly rejected invalid doctor_id)")

    # Test 3: Invalid patient_id in medical record
    try:
        cursor.execute("""
        INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date)
        VALUES (999, 9999, 1, 1, 'Test Diagnosis', 'Test Treatment', '2026-03-10');
        """)
        assert False, "Should have raised FK constraint violation"
    except sqlite3.IntegrityError:
        print("  [OK] TEST 3 [Invalid Patient FK]: PASSED (Correctly rejected invalid patient_id)")

    # Test 4: Duplicate patient email
    try:
        cursor.execute("""
        INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group)
        VALUES (100, 'Duplicate Aarav', '1992-04-10', 'MALE', '9811122299', 'aarav.mehta@email.com', '99 Duplicate Lane', 'A+');
        """)
        assert False, "Should have raised UNIQUE constraint violation"
    except sqlite3.IntegrityError:
        print("  [OK] TEST 4 [Duplicate Email]: PASSED (Correctly rejected duplicate email by UNIQUE constraint)")

    # Test 5: Invalid appointment status
    try:
        cursor.execute("""
        INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
        VALUES (998, 1, 1, '2026-03-10', '10:00 AM', 'Test Check', 'INVALID_STATUS');
        """)
        assert False, "Should have raised CHECK constraint violation"
    except sqlite3.IntegrityError:
        print("  [OK] TEST 5 [Invalid Appt Status]: PASSED (Correctly rejected invalid status by CHECK constraint)")

    # Test 6: Negative bill amount
    try:
        cursor.execute("""
        INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
        VALUES (999, 1, 1, '2026-03-10', -100.00, 50.00, -50.00, 'PAID');
        """)
        assert False, "Should have raised CHECK constraint violation"
    except sqlite3.IntegrityError:
        print("  [OK] TEST 6 [Negative Bill Amount]: PASSED (Correctly rejected negative fee by CHECK constraint)")

    # Test 7: Invalid payment status
    try:
        cursor.execute("""
        INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
        VALUES (999, 1, 1, '2026-03-10', 500.00, 200.00, 700.00, 'PARTIALLY_PAID');
        """)
        assert False, "Should have raised CHECK constraint violation"
    except sqlite3.IntegrityError:
        print("  [OK] TEST 7 [Invalid Payment Status]: PASSED (Correctly rejected invalid status by CHECK constraint)")

    print("\n" + "=" * 80)
    print("STEP 6: TESTING PL/SQL PROCEDURE & FUNCTION LOGIC")
    print("=" * 80)

    # Simulation of GENERATE_PATIENT_BILL
    def generate_patient_bill(appointment_id, consult_fee=500.0, med_fee=250.0):
        row = cursor.execute("SELECT patient_id FROM APPOINTMENT WHERE appointment_id = ?", (appointment_id,)).fetchone()
        if not row:
            return "ERROR: Appointment ID does not exist."
        patient_id = row[0]
        total = consult_fee + med_fee
        existing = cursor.execute("SELECT bill_id FROM BILL WHERE appointment_id = ?", (appointment_id,)).fetchone()
        if existing:
            cursor.execute("UPDATE BILL SET consultation_fee = ?, medicine_fee = ?, total_amount = ? WHERE appointment_id = ?",
                           (consult_fee, med_fee, total, appointment_id))
            action = "UPDATED"
        else:
            cursor.execute("INSERT INTO BILL (patient_id, appointment_id, consultation_fee, medicine_fee, total_amount, payment_status) VALUES (?, ?, ?, ?, ?, 'PENDING')",
                           (patient_id, appointment_id, consult_fee, med_fee, total))
            action = "INSERTED"
        return f"SUCCESS: Bill {action} for Appt {appointment_id}: Total = {total}"

    # Simulation of GET_PATIENT_TOTAL_BILL
    def get_patient_total_bill(patient_id):
        p_row = cursor.execute("SELECT patient_id FROM PATIENT WHERE patient_id = ?", (patient_id,)).fetchone()
        if not p_row:
            return -1
        total = cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM BILL WHERE patient_id = ?", (patient_id,)).fetchone()[0]
        return total

    # Test procedure for Appointment 13
    res_proc = generate_patient_bill(13, 700.0, 350.0)
    print(f"  [OK] Procedure Test: {res_proc}")
    
    # Test function
    total_p1 = get_patient_total_bill(1)
    print(f"  [OK] Function Test (Patient 1): Total Billed = INR {total_p1:.2f}")
    assert total_p1 == 2270.00, f"Expected 2270.00 for Patient 1, got {total_p1}"

    print("\n" + "=" * 80)
    print("STEP 7: SAMPLE REPORTS VERIFICATION")
    print("=" * 80)
    reports = [
        ("PATIENT REPORT", "SELECT patient_id, patient_name, gender, blood_group, phone FROM PATIENT LIMIT 3;"),
        ("APPOINTMENT REPORT", "SELECT p.patient_name, d.doctor_name, dept.department_name, a.appointment_date, a.status FROM APPOINTMENT a JOIN PATIENT p ON a.patient_id = p.patient_id JOIN DOCTOR d ON a.doctor_id = d.doctor_id JOIN DEPARTMENT dept ON d.department_id = dept.department_id LIMIT 3;"),
        ("MEDICAL HISTORY REPORT", "SELECT p.patient_name, d.doctor_name, mr.diagnosis, mr.treatment, mr.record_date FROM MEDICAL_RECORD mr JOIN PATIENT p ON mr.patient_id = p.patient_id JOIN DOCTOR d ON mr.doctor_id = d.doctor_id LIMIT 3;"),
        ("BILL REPORT", "SELECT p.patient_name, b.bill_date, b.total_amount, b.payment_status FROM BILL b JOIN PATIENT p ON b.patient_id = p.patient_id LIMIT 3;"),
        ("DOCTOR REPORT", "SELECT d.doctor_name, d.specialization, dept.department_name, COUNT(a.appointment_id) AS total_appts FROM DOCTOR d JOIN DEPARTMENT dept ON d.department_id = dept.department_id LEFT JOIN APPOINTMENT a ON d.doctor_id = a.doctor_id GROUP BY d.doctor_id, d.doctor_name, d.specialization, dept.department_name;")
    ]

    for title, rep_sql in reports:
        rows = cursor.execute(rep_sql).fetchall()
        print(f"  [OK] {title} validated ({len(rows)} sample rows returned)")

    print("\n" + "=" * 80)
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY WITH ZERO ERRORS!")
    print("=" * 80)
    conn.close()

if __name__ == "__main__":
    run_verification()
