"""
Full Integration Test Suite for Hospital Patient Record System (Step 2)
Tests: Auth, Dashboard, Patients, Doctors, Appointments, Medical Records, Prescriptions, Bills, and Static Frontend Pages.
"""

from fastapi.testclient import TestClient
from backend.main import app
from backend.database import initialize_database
import sys

def run_tests():
    print("=" * 80)
    print("RUNNING STEP 2 INTEGRATION TEST SUITE")
    print("=" * 80)

    initialize_database()
    client = TestClient(app)

    # 1. Test Static Frontend Pages
    print("\n--- 1. Testing Frontend HTML Page Routes ---")
    pages = ["/", "/login", "/dashboard", "/patients", "/doctors", "/appointments", "/medical-records", "/prescriptions", "/bills"]
    for p in pages:
        res = client.get(p)
        assert res.status_code == 200, f"Page {p} returned status {res.status_code}"
        assert "<!DOCTYPE html>" in res.text, f"Page {p} did not return valid HTML"
        print(f"  [OK] GET {p.ljust(18)} -> 200 OK")

    # 2. Test CSS and JS static file mounts
    print("\n--- 2. Testing Static Asset Delivery ---")
    css_res = client.get("/css/style.css")
    assert css_res.status_code == 200, "Failed to load /css/style.css"
    print("  [OK] GET /css/style.css    -> 200 OK")

    js_res = client.get("/js/api.js")
    assert js_res.status_code == 200, "Failed to load /js/api.js"
    print("  [OK] GET /js/api.js        -> 200 OK")

    # 3. Test Authentication
    print("\n--- 3. Testing Authentication ---")
    # Admin login
    res = client.post("/api/auth/login", json={"email": "admin@hospital.org", "password": "admin123"})
    assert res.status_code == 200 and res.json()["user"]["role"] == "ADMIN"
    print("  [OK] Admin Login (admin@hospital.org) -> 200 OK")

    # Staff login
    res = client.post("/api/auth/login", json={"email": "staff@hospital.org", "password": "staff123"})
    assert res.status_code == 200 and res.json()["user"]["role"] == "STAFF"
    print("  [OK] Staff Login (staff@hospital.org) -> 200 OK")

    # Invalid login
    res = client.post("/api/auth/login", json={"email": "admin@hospital.org", "password": "wrongpassword"})
    assert res.status_code == 401
    print("  [OK] Invalid Credentials -> 401 Unauthorized (Correctly rejected)")

    # 4. Test Dashboard API
    print("\n--- 4. Testing Dashboard Statistics ---")
    dash = client.get("/api/dashboard").json()
    stats = dash["stats"]
    assert stats["total_patients"] >= 10
    assert stats["total_doctors"] == 6
    assert stats["total_records"] >= 12
    assert stats["pending_bills"] >= 1
    assert len(dash["recent_appointments"]) > 0
    assert len(dash["recent_records"]) > 0
    print(f"  [OK] Dashboard stats verified: {stats}")

    # 5. Test Patients CRUD
    print("\n--- 5. Testing Patients API ---")
    # List patients
    patients = client.get("/api/patients").json()
    assert len(patients) >= 10
    print(f"  [OK] GET /api/patients -> {len(patients)} patients loaded")

    # Search patient
    search_res = client.get("/api/patients?search=Aarav").json()
    assert len(search_res) >= 1 and search_res[0]["patient_name"] == "Aarav Mehta"
    print("  [OK] Search patient by name -> Found Aarav Mehta")

    # Create new patient
    new_patient_payload = {
        "patient_name": "Integration Test Patient",
        "date_of_birth": "1994-04-12",
        "gender": "MALE",
        "phone": "9800011122",
        "email": "test.patient@hospital.org",
        "address": "456 Test Street, Pune",
        "blood_group": "O+"
    }
    create_res = client.post("/api/patients", json=new_patient_payload)
    assert create_res.status_code == 201
    new_p_id = create_res.json()["patient_id"]
    print(f"  [OK] POST /api/patients -> Created patient ID #{new_p_id}")

    # Patient details view
    p_details = client.get(f"/api/patients/{new_p_id}/details").json()
    assert p_details["patient"]["patient_name"] == "Integration Test Patient"
    print("  [OK] GET /api/patients/{id}/details -> Demographic profile loaded")

    # Update patient
    new_patient_payload["patient_name"] = "Integration Test Patient Updated"
    update_res = client.put(f"/api/patients/{new_p_id}", json=new_patient_payload)
    assert update_res.status_code == 200
    print("  [OK] PUT /api/patients/{id} -> Patient name updated")

    # Delete patient
    del_res = client.delete(f"/api/patients/{new_p_id}")
    assert del_res.status_code == 200
    print(f"  [OK] DELETE /api/patients/{new_p_id} -> Deleted successfully")

    # 6. Test Doctors and Departments
    print("\n--- 6. Testing Doctors & Departments API ---")
    depts = client.get("/api/departments").json()
    assert len(depts) == 5
    print(f"  [OK] GET /api/departments -> {len(depts)} departments loaded")

    doctors = client.get("/api/doctors").json()
    assert len(doctors) == 6
    print(f"  [OK] GET /api/doctors -> {len(doctors)} doctors loaded")

    # 7. Test Appointments Scheduling & Status Transitions
    print("\n--- 7. Testing Appointments API ---")
    appts = client.get("/api/appointments").json()
    assert len(appts) >= 15
    print(f"  [OK] GET /api/appointments -> {len(appts)} appointments loaded")

    # Filter appointments by status
    scheduled_appts = client.get("/api/appointments?status=SCHEDULED").json()
    assert all(a["status"] == "SCHEDULED" for a in scheduled_appts)
    print(f"  [OK] Filter /api/appointments?status=SCHEDULED -> {len(scheduled_appts)} items")

    # Create appointment (defaults to SCHEDULED)
    new_appt_payload = {
        "patient_id": 1,
        "doctor_id": 1,
        "appointment_date": "2026-04-01",
        "appointment_time": "11:00 AM",
        "reason": "Routine Checkup"
    }
    create_appt_res = client.post("/api/appointments", json=new_appt_payload)
    assert create_appt_res.status_code == 201
    new_appt_id = create_appt_res.json()["appointment_id"]
    print(f"  [OK] POST /api/appointments -> Scheduled appointment ID #{new_appt_id}")

    # Mark appointment as COMPLETED
    status_res = client.put(f"/api/appointments/{new_appt_id}/status", json={"status": "COMPLETED"})
    assert status_res.status_code == 200
    print("  [OK] PUT /api/appointments/{id}/status -> Marked as COMPLETED")

    # 8. Test Medical Records & Prescriptions
    print("\n--- 8. Testing Medical Records & Prescriptions API ---")
    records = client.get("/api/medical-records").json()
    assert len(records) >= 12
    print(f"  [OK] GET /api/medical-records -> {len(records)} records loaded")

    # Create medical record
    new_record_payload = {
        "patient_id": 1,
        "doctor_id": 1,
        "appointment_id": new_appt_id,
        "diagnosis": "Seasonal Influenza",
        "treatment": "Antipyretics, hydration",
        "notes": "Mild throat redness."
    }
    rec_res = client.post("/api/medical-records", json=new_record_payload)
    assert rec_res.status_code == 201
    new_rec_id = rec_res.json()["record_id"]
    print(f"  [OK] POST /api/medical-records -> Created record ID #{new_rec_id}")

    # Create prescription for this record
    new_presc_payload = {
        "record_id": new_rec_id,
        "medicine_name": "Paracetamol 500mg",
        "dosage": "1 tablet",
        "frequency": "Thrice daily after meals",
        "duration_days": 5
    }
    presc_res = client.post("/api/prescriptions", json=new_presc_payload)
    assert presc_res.status_code == 201
    print(f"  [OK] POST /api/prescriptions -> Issued prescription for record #{new_rec_id}")

    # 9. Test Bills (Server-side calculation)
    print("\n--- 9. Testing Billing API & Server Calculations ---")
    bills = client.get("/api/bills").json()
    assert len(bills) >= 12
    print(f"  [OK] GET /api/bills -> {len(bills)} bills loaded")

    # Generate bill for new_appt_id
    consult_fee = 600.00
    med_fee = 325.50
    expected_total = 925.50
    bill_payload = {
        "appointment_id": new_appt_id,
        "consultation_fee": consult_fee,
        "medicine_fee": med_fee
    }
    gen_bill_res = client.post("/api/bills", json=bill_payload)
    assert gen_bill_res.status_code == 201
    bill_data = gen_bill_res.json()
    assert bill_data["total_amount"] == expected_total, f"Expected {expected_total}, got {bill_data['total_amount']}"
    new_bill_id = bill_data["bill_id"]
    print(f"  [OK] POST /api/bills -> Generated Bill #{new_bill_id} | Verified Server Total: INR {expected_total}")

    # Toggle payment status to PAID
    pay_res = client.put(f"/api/bills/{new_bill_id}/status", json={"payment_status": "PAID"})
    assert pay_res.status_code == 200
    print("  [OK] PUT /api/bills/{id}/status -> Updated to PAID")

    print("\n" + "=" * 80)
    print("ALL INTEGRATION TESTS PASSED WITH ZERO ERRORS!")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()
