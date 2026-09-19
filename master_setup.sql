-- ============================================================================
-- PROJECT: HOSPITAL PATIENT RECORD SYSTEM (ORACLE COE PROJECT)
-- SCRIPT: master_setup.sql
-- PURPOSE: Master runner script to execute complete setup sequentially
-- USAGE IN SQL*PLUS / SQL DEVELOPER:
--   @01_schema_ddl.sql
--   @02_sample_data.sql
--   @04_views.sql
--   @05_plsql.sql
--   @03_queries.sql
--   @06_integrity_tests.sql
--   @07_reports.sql
-- ============================================================================

SET FEEDBACK ON;
SET SERVEROUTPUT ON;
SET LINESIZE 200;
SET PAGESIZE 50;

PROMPT ============================================================================
PROMPT STEP 1: CREATING TABLES AND CONSTRAINTS (01_schema_ddl.sql)
PROMPT ============================================================================
@@01_schema_ddl.sql

PROMPT ============================================================================
PROMPT STEP 2: INSERTING SAMPLE DATA (02_sample_data.sql)
PROMPT ============================================================================
@@02_sample_data.sql

PROMPT ============================================================================
PROMPT STEP 3: CREATING VIEWS (04_views.sql)
PROMPT ============================================================================
@@04_views.sql

PROMPT ============================================================================
PROMPT STEP 4: COMPILING PL/SQL OBJECTS (05_plsql.sql)
PROMPT ============================================================================
@@05_plsql.sql

PROMPT ============================================================================
PROMPT STEP 5: RUNNING 20 VERIFICATION QUERIES (03_queries.sql)
PROMPT ============================================================================
@@03_queries.sql

PROMPT ============================================================================
PROMPT STEP 6: RUNNING INTEGRITY CONSTRAINT TESTS (06_integrity_tests.sql)
PROMPT ============================================================================
@@06_integrity_tests.sql

PROMPT ============================================================================
PROMPT STEP 7: GENERATING OPERATIONAL REPORTS (07_reports.sql)
PROMPT ============================================================================
@@07_reports.sql

PROMPT ============================================================================
PROMPT MASTER SETUP COMPLETED SUCCESSFULLY!
PROMPT ============================================================================
