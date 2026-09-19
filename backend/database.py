"""
Database Connection Manager for Hospital Patient Record System
Supports Oracle Database (via oracledb) with automatic fallback to embedded SQLite (hospital.db).
"""

import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "hospital.db"

# Environment variables for Oracle connection
ORACLE_USER = os.getenv("ORACLE_USER", "")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "")
ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:1521/XEPDB1")

USE_ORACLE = bool(ORACLE_USER and ORACLE_PASSWORD)

def get_connection():
    if USE_ORACLE:
        try:
            import oracledb
            conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
            return conn, "oracle"
        except Exception as e:
            print(f"[DB Warning] Failed to connect to Oracle ({e}). Falling back to embedded SQLite.")
    
    conn = sqlite3.connect(str(DB_FILE))
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn, "sqlite"

def execute_query(sql: str, params: tuple = (), fetchone: bool = False, fetchall: bool = False, commit: bool = False):
    conn, db_type = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        
        result = None
        if fetchone:
            row = cursor.fetchone()
            if row:
                if db_type == "sqlite":
                    result = dict(row)
                else:
                    cols = [col[0].lower() for col in cursor.description]
                    result = dict(zip(cols, row))
        elif fetchall:
            rows = cursor.fetchall()
            if db_type == "sqlite":
                result = [dict(row) for row in rows]
            else:
                cols = [col[0].lower() for col in cursor.description]
                result = [dict(zip(cols, row)) for row in rows]
                
        last_id = cursor.lastrowid if db_type == "sqlite" else None
        
        if commit:
            conn.commit()
            
        return result if (fetchone or fetchall) else last_id
    finally:
        conn.close()

def initialize_database():
    """Initializes and seeds the database if it doesn't already exist."""
    conn = sqlite3.connect(str(DB_FILE))
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Check if PATIENT table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='PATIENT';")
    if cursor.fetchone() is not None:
        conn.close()
        return

    print("[DB] Initializing database tables and seed data...")

    # 1. ADMIN_USER for authentication
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ADMIN_USER (
        user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT NOT NULL,
        email         TEXT NOT NULL UNIQUE,
        password      TEXT NOT NULL,
        role          TEXT NOT NULL CHECK (role IN ('ADMIN', 'STAFF'))
    );
    """)

    # 2. DEPARTMENT
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DEPARTMENT (
        department_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL UNIQUE,
        location        TEXT NOT NULL
    );
    """)

    # 3. DOCTOR
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DOCTOR (
        doctor_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_name     TEXT NOT NULL,
        specialization  TEXT NOT NULL,
        phone           TEXT NOT NULL,
        email           TEXT NOT NULL UNIQUE,
        department_id   INTEGER NOT NULL,
        FOREIGN KEY (department_id) REFERENCES DEPARTMENT(department_id)
    );
    """)

    # 4. PATIENT
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS PATIENT (
        patient_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name    TEXT NOT NULL,
        date_of_birth   TEXT NOT NULL,
        gender          TEXT NOT NULL CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
        phone           TEXT NOT NULL,
        email           TEXT NOT NULL UNIQUE,
        address         TEXT NOT NULL,
        blood_group     TEXT NOT NULL CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
        created_at      TEXT NOT NULL DEFAULT (DATE('now'))
    );
    """)

    # 5. APPOINTMENT
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS APPOINTMENT (
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

    # 6. MEDICAL_RECORD
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS MEDICAL_RECORD (
        record_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id      INTEGER NOT NULL,
        doctor_id       INTEGER NOT NULL,
        appointment_id  INTEGER,
        diagnosis       TEXT NOT NULL,
        treatment       TEXT NOT NULL,
        record_date     TEXT NOT NULL DEFAULT (DATE('now')),
        notes           TEXT,
        FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id),
        FOREIGN KEY (doctor_id) REFERENCES DOCTOR(doctor_id),
        FOREIGN KEY (appointment_id) REFERENCES APPOINTMENT(appointment_id)
    );
    """)

    # 7. PRESCRIPTION
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS PRESCRIPTION (
        prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id       INTEGER NOT NULL,
        medicine_name   TEXT NOT NULL,
        dosage          TEXT NOT NULL,
        frequency       TEXT NOT NULL,
        duration_days   INTEGER NOT NULL CHECK (duration_days > 0),
        FOREIGN KEY (record_id) REFERENCES MEDICAL_RECORD(record_id)
    );
    """)

    # 8. BILL
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS BILL (
        bill_id          INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id       INTEGER NOT NULL,
        appointment_id   INTEGER,
        bill_date        TEXT NOT NULL DEFAULT (DATE('now')),
        consultation_fee REAL NOT NULL DEFAULT 0.00 CHECK (consultation_fee >= 0),
        medicine_fee     REAL NOT NULL DEFAULT 0.00 CHECK (medicine_fee >= 0),
        total_amount     REAL NOT NULL CHECK (total_amount >= 0),
        payment_status   TEXT NOT NULL DEFAULT 'PENDING' CHECK (payment_status IN ('PAID', 'PENDING')),
        FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id),
        FOREIGN KEY (appointment_id) REFERENCES APPOINTMENT(appointment_id)
    );
    """)

    # Seed Admin & Staff Users
    admin_users = [
        ('System Administrator', 'admin@hospital.org', 'admin123', 'ADMIN'),
        ('Hospital Staff', 'staff@hospital.org', 'staff123', 'STAFF')
    ]
    cursor.executemany("INSERT INTO ADMIN_USER (name, email, password, role) VALUES (?, ?, ?, ?);", admin_users)

    # Seed Departments
    departments = [
        (1, 'Cardiology', 'Block A, 3rd Floor'),
        (2, 'General Medicine', 'Block B, 1st Floor'),
        (3, 'Orthopedics', 'Block A, 2nd Floor'),
        (4, 'Pediatrics', 'Block C, 1st Floor'),
        (5, 'Dermatology', 'Block B, 2nd Floor')
    ]
    cursor.executemany("INSERT INTO DEPARTMENT VALUES (?, ?, ?);", departments)

    # Seed Doctors
    doctors = [
        (1, 'Dr. Rajesh Sharma', 'Cardiologist', '9876543210', 'rajesh.sharma@hospital.org', 1),
        (2, 'Dr. Priya Nair', 'Consultant Physician', '9876543211', 'priya.nair@hospital.org', 2),
        (3, 'Dr. Amit Patel', 'Orthopedic Surgeon', '9876543212', 'amit.patel@hospital.org', 3),
        (4, 'Dr. Sneha Rao', 'Pediatrician', '9876543213', 'sneha.rao@hospital.org', 4),
        (5, 'Dr. Vikram Verma', 'Dermatologist', '9876543214', 'vikram.verma@hospital.org', 5),
        (6, 'Dr. Ananya Iyer', 'Interventional Cardiologist', '9876543215', 'ananya.iyer@hospital.org', 1)
    ]
    cursor.executemany("INSERT INTO DOCTOR VALUES (?, ?, ?, ?, ?, ?);", doctors)

    # Seed Patients
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

    # Seed Appointments
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

    # Seed Medical Records
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

    # Seed Prescriptions
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

    # Seed Bills
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
    conn.close()
    print("[DB] Initialization completed successfully.")
