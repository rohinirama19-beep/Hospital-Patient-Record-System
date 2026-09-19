-- ============================================================================
-- PROJECT: HOSPITAL PATIENT RECORD SYSTEM (ORACLE COE PROJECT)
-- SCRIPT: 05_plsql.sql
-- PURPOSE: PL/SQL Procedure and Function with Execution Test Blocks
-- ============================================================================

SET SERVEROUTPUT ON;

-- ----------------------------------------------------------------------------
-- 1. PL/SQL PROCEDURE: GENERATE_PATIENT_BILL
-- Purpose: Accepts an appointment_id, retrieves patient details, computes 
--          total = consultation_fee + medicine_fee, inserts or updates the 
--          BILL table, and handles exceptions cleanly.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE GENERATE_PATIENT_BILL (
    p_appointment_id   IN NUMBER,
    p_consultation_fee IN NUMBER DEFAULT 500.00,
    p_medicine_fee     IN NUMBER DEFAULT 250.00
) AS
    v_patient_id    APPOINTMENT.patient_id%TYPE;
    v_total_amount  NUMBER(10,2);
    v_existing_bill NUMBER;
BEGIN
    -- Step 1: Validate appointment and fetch patient_id
    SELECT patient_id INTO v_patient_id
    FROM APPOINTMENT
    WHERE appointment_id = p_appointment_id;

    -- Step 2: Calculate total amount
    v_total_amount := p_consultation_fee + p_medicine_fee;

    -- Step 3: Check if bill already exists for this appointment
    SELECT COUNT(*) INTO v_existing_bill
    FROM BILL
    WHERE appointment_id = p_appointment_id;

    IF v_existing_bill > 0 THEN
        -- Step 4a: Update existing bill
        UPDATE BILL
        SET consultation_fee = p_consultation_fee,
            medicine_fee     = p_medicine_fee,
            total_amount     = v_total_amount,
            bill_date        = SYSDATE
        WHERE appointment_id = p_appointment_id;

        DBMS_OUTPUT.PUT_LINE('SUCCESS: Bill updated for Appointment ID ' || p_appointment_id || 
                             '. Total: INR ' || v_total_amount);
    ELSE
        -- Step 4b: Insert new bill
        INSERT INTO BILL (
            patient_id,
            appointment_id,
            bill_date,
            consultation_fee,
            medicine_fee,
            total_amount,
            payment_status
        ) VALUES (
            v_patient_id,
            p_appointment_id,
            SYSDATE,
            p_consultation_fee,
            p_medicine_fee,
            v_total_amount,
            'PENDING'
        );

        DBMS_OUTPUT.PUT_LINE('SUCCESS: New bill generated for Appointment ID ' || p_appointment_id || 
                             '. Total: INR ' || v_total_amount);
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('ERROR: Appointment ID ' || p_appointment_id || ' does not exist.');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('ERROR: Exception in GENERATE_PATIENT_BILL: ' || SQLERRM);
END GENERATE_PATIENT_BILL;
/

-- ----------------------------------------------------------------------------
-- 2. PL/SQL FUNCTION: GET_PATIENT_TOTAL_BILL
-- Purpose: Accepts a patient_id and returns the total billed amount using SUM().
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION GET_PATIENT_TOTAL_BILL (
    p_patient_id IN NUMBER
) RETURN NUMBER AS
    v_total_billed   NUMBER(10,2) := 0;
    v_patient_count  NUMBER := 0;
BEGIN
    -- Verify if patient exists
    SELECT COUNT(*) INTO v_patient_count
    FROM PATIENT
    WHERE patient_id = p_patient_id;

    IF v_patient_count = 0 THEN
        -- Patient not found
        RETURN -1;
    END IF;

    -- Calculate sum of all bills for this patient
    SELECT NVL(SUM(total_amount), 0) INTO v_total_billed
    FROM BILL
    WHERE patient_id = p_patient_id;

    RETURN v_total_billed;

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('ERROR in GET_PATIENT_TOTAL_BILL: ' || SQLERRM);
        RETURN 0;
END GET_PATIENT_TOTAL_BILL;
/

-- ----------------------------------------------------------------------------
-- 3. TEST EXECUTION BLOCKS
-- ----------------------------------------------------------------------------

-- A. Test Procedure: Generate bill for Appointment 13 (which currently has no bill)
BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Testing GENERATE_PATIENT_BILL Procedure ---');
    GENERATE_PATIENT_BILL(p_appointment_id => 13, p_consultation_fee => 700.00, p_medicine_fee => 350.00);
    
    -- Test procedure error handling with invalid appointment
    GENERATE_PATIENT_BILL(p_appointment_id => 9999);
END;
/

-- B. Test Function: Retrieve total billing for patients
SELECT 
    patient_id,
    patient_name,
    GET_PATIENT_TOTAL_BILL(patient_id) AS total_amount_billed
FROM PATIENT
WHERE patient_id IN (1, 2, 3, 5, 10)
ORDER BY patient_id;
