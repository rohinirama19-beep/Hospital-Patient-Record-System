-- ============================================================================
-- PROJECT: HOSPITAL PATIENT RECORD SYSTEM (ORACLE COE PROJECT)
-- SCRIPT: 06_integrity_tests.sql
-- PURPOSE: Verify and demonstrate Data Integrity Constraints
-- ============================================================================

SET SERVEROUTPUT ON;

PROMPT ============================================================================
PROMPT RUNNING AUTOMATED CONSTRAINT INTEGRITY SUITE
PROMPT ============================================================================

-- ----------------------------------------------------------------------------
-- TEST 1: Valid Patient Insertion (Expected: SUCCESS)
-- ----------------------------------------------------------------------------
BEGIN
    INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group)
    VALUES (99, 'Test Valid Patient', TO_DATE('1995-01-01', 'YYYY-MM-DD'), 'MALE', '9999988888', 'test.valid@hospital.org', '100 Test St', 'O+');
    
    DBMS_OUTPUT.PUT_LINE('TEST 1 [Valid Patient Insert]: PASSED (Row inserted successfully)');
    ROLLBACK; -- Clean up test row
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('TEST 1 [Valid Patient Insert]: FAILED (' || SQLERRM || ')');
        ROLLBACK;
END;
/

-- ----------------------------------------------------------------------------
-- TEST 2: Invalid doctor_id in appointment (Expected: FK Constraint ORA-02291)
-- ----------------------------------------------------------------------------
BEGIN
    INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
    VALUES (999, 1, 9999, TO_DATE('2026-03-10', 'YYYY-MM-DD'), '10:00 AM', 'Test Check', 'SCHEDULED');
    
    DBMS_OUTPUT.PUT_LINE('TEST 2 [Invalid Doctor FK]: FAILED (Invalid FK was improperly allowed)');
    ROLLBACK;
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -2291 THEN
            DBMS_OUTPUT.PUT_LINE('TEST 2 [Invalid Doctor FK]: PASSED (Correctly rejected by FK constraint fk_appt_doctor: ' || SQLERRM || ')');
        ELSE
            DBMS_OUTPUT.PUT_LINE('TEST 2 [Invalid Doctor FK]: ERROR (' || SQLERRM || ')');
        END IF;
        ROLLBACK;
END;
/

-- ----------------------------------------------------------------------------
-- TEST 3: Invalid patient_id in medical record (Expected: FK Constraint ORA-02291)
-- ----------------------------------------------------------------------------
BEGIN
    INSERT INTO MEDICAL_RECORD (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, record_date)
    VALUES (999, 9999, 1, 1, 'Test Diagnosis', 'Test Treatment', SYSDATE);
    
    DBMS_OUTPUT.PUT_LINE('TEST 3 [Invalid Patient FK]: FAILED (Invalid FK was improperly allowed)');
    ROLLBACK;
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -2291 THEN
            DBMS_OUTPUT.PUT_LINE('TEST 3 [Invalid Patient FK]: PASSED (Correctly rejected by FK constraint fk_mr_patient: ' || SQLERRM || ')');
        ELSE
            DBMS_OUTPUT.PUT_LINE('TEST 3 [Invalid Patient FK]: ERROR (' || SQLERRM || ')');
        END IF;
        ROLLBACK;
END;
/

-- ----------------------------------------------------------------------------
-- TEST 4: Duplicate Patient Email (Expected: UNIQUE Constraint ORA-00001)
-- ----------------------------------------------------------------------------
BEGIN
    -- 'aarav.mehta@email.com' already exists for patient 1
    INSERT INTO PATIENT (patient_id, patient_name, date_of_birth, gender, phone, email, address, blood_group)
    VALUES (100, 'Duplicate Aarav', TO_DATE('1992-04-10', 'YYYY-MM-DD'), 'MALE', '9811122299', 'aarav.mehta@email.com', '99 Duplicate Lane', 'A+');
    
    DBMS_OUTPUT.PUT_LINE('TEST 4 [Duplicate Email]: FAILED (Duplicate email was improperly allowed)');
    ROLLBACK;
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        DBMS_OUTPUT.PUT_LINE('TEST 4 [Duplicate Email]: PASSED (Correctly rejected duplicate email by UNIQUE constraint)');
        ROLLBACK;
    WHEN OTHERS THEN
        IF SQLCODE = -1 THEN
            DBMS_OUTPUT.PUT_LINE('TEST 4 [Duplicate Email]: PASSED (Correctly rejected duplicate email by UNIQUE constraint: ORA-00001)');
        ELSE
            DBMS_OUTPUT.PUT_LINE('TEST 4 [Duplicate Email]: ERROR (' || SQLERRM || ')');
        END IF;
        ROLLBACK;
END;
/

-- ----------------------------------------------------------------------------
-- TEST 5: Invalid Appointment Status (Expected: CHECK Constraint ORA-02290)
-- ----------------------------------------------------------------------------
BEGIN
    INSERT INTO APPOINTMENT (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status)
    VALUES (998, 1, 1, TO_DATE('2026-03-10', 'YYYY-MM-DD'), '10:00 AM', 'Test Check', 'INVALID_STATUS');
    
    DBMS_OUTPUT.PUT_LINE('TEST 5 [Invalid Appt Status]: FAILED (Invalid status was improperly allowed)');
    ROLLBACK;
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -2290 THEN
            DBMS_OUTPUT.PUT_LINE('TEST 5 [Invalid Appt Status]: PASSED (Correctly rejected invalid status by CHECK constraint chk_appt_status)');
        ELSE
            DBMS_OUTPUT.PUT_LINE('TEST 5 [Invalid Appt Status]: ERROR (' || SQLERRM || ')');
        END IF;
        ROLLBACK;
END;
/

-- ----------------------------------------------------------------------------
-- TEST 6: Negative Bill Amount (Expected: CHECK Constraint ORA-02290)
-- ----------------------------------------------------------------------------
BEGIN
    INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
    VALUES (999, 1, 1, SYSDATE, -100.00, 50.00, -50.00, 'PAID');
    
    DBMS_OUTPUT.PUT_LINE('TEST 6 [Negative Bill Amount]: FAILED (Negative amount was improperly allowed)');
    ROLLBACK;
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -2290 THEN
            DBMS_OUTPUT.PUT_LINE('TEST 6 [Negative Bill Amount]: PASSED (Correctly rejected negative fee by CHECK constraint chk_bill_consult_fee/chk_bill_total)');
        ELSE
            DBMS_OUTPUT.PUT_LINE('TEST 6 [Negative Bill Amount]: ERROR (' || SQLERRM || ')');
        END IF;
        ROLLBACK;
END;
/

-- ----------------------------------------------------------------------------
-- TEST 7: Invalid Payment Status (Expected: CHECK Constraint ORA-02290)
-- ----------------------------------------------------------------------------
BEGIN
    INSERT INTO BILL (bill_id, patient_id, appointment_id, bill_date, consultation_fee, medicine_fee, total_amount, payment_status)
    VALUES (999, 1, 1, SYSDATE, 500.00, 200.00, 700.00, 'PARTIALLY_PAID');
    
    DBMS_OUTPUT.PUT_LINE('TEST 7 [Invalid Payment Status]: FAILED (Invalid payment status was improperly allowed)');
    ROLLBACK;
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -2290 THEN
            DBMS_OUTPUT.PUT_LINE('TEST 7 [Invalid Payment Status]: PASSED (Correctly rejected invalid status by CHECK constraint chk_bill_status)');
        ELSE
            DBMS_OUTPUT.PUT_LINE('TEST 7 [Invalid Payment Status]: ERROR (' || SQLERRM || ')');
        END IF;
        ROLLBACK;
END;
/
