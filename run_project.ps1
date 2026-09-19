# ==============================================================================
# HOSPITAL PATIENT RECORD SYSTEM - POWERSHELL RUNNER
# Oracle COE Academic Project
# ==============================================================================

param (
    [string]$Mode = "menu"
)

$Host.UI.RawUI.WindowTitle = "Hospital Patient Record System (Oracle COE)"

function Show-Banner {
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host "         HOSPITAL PATIENT RECORD SYSTEM - ORACLE COE PROJECT                   " -ForegroundColor Yellow -BackgroundColor Black
    Write-Host "                   POWERSHELL EXECUTION HARNESS                                 " -ForegroundColor White
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Menu {
    Show-Banner
    Write-Host "Select an option to run:" -ForegroundColor Green
    Write-Host " [1] Run Complete Database System (Schema, 20 Queries, Views, PL/SQL, Reports)" -ForegroundColor White
    Write-Host " [2] View Database Schema & Constraints" -ForegroundColor White
    Write-Host " [3] Run 20 Core SQL Queries (with formatted ASCII tables)" -ForegroundColor White
    Write-Host " [4] Query Database Views (Medical History, Billing, Doctor Summary)" -ForegroundColor White
    Write-Host " [5] Test PL/SQL Business Logic (Procedure & Function)" -ForegroundColor White
    Write-Host " [6] Run Data Integrity & Constraint Tests (7 Scenarios)" -ForegroundColor White
    Write-Host " [7] Generate 5 Core Operational Reports" -ForegroundColor White
    Write-Host " [8] Run Fast Verification Test Suite (verify_database.py)" -ForegroundColor White
    Write-Host " [9] Execute in Oracle SQL*Plus / SQL Developer (@master_setup.sql)" -ForegroundColor Yellow
    Write-Host " [0] Exit" -ForegroundColor Red
    Write-Host ""
    $choice = Read-Host "Enter your choice [0-9]"
    return $choice
}

# Ensure script runs in its own directory
Set-Location -Path $PSScriptRoot

if ($Mode -eq "menu") {
    do {
        $choice = Show-Menu
        switch ($choice) {
            "1" { python run_hospital_system.py all; break }
            "2" { python run_hospital_system.py schema; break }
            "3" { python run_hospital_system.py queries; break }
            "4" { python run_hospital_system.py views; break }
            "5" { python run_hospital_system.py plsql; break }
            "6" { python run_hospital_system.py integrity; break }
            "7" { python run_hospital_system.py reports; break }
            "8" { python verify_database.py; break }
            "9" {
                Write-Host ""
                Write-Host "To execute directly in Oracle SQL*Plus or Oracle SQL Developer:" -ForegroundColor Yellow
                Write-Host " 1. Open SQL*Plus: sqlplus username/password@localhost:1521/XEPDB1" -ForegroundColor White
                Write-Host " 2. Run: @master_setup.sql" -ForegroundColor White
                Write-Host " All 7 SQL scripts will execute sequentially." -ForegroundColor Green
                break
            }
            "0" { Write-Host "Exiting. Good luck with your Oracle COE evaluation!" -ForegroundColor Green; exit }
            default { Write-Host "Invalid choice, please enter 0-9." -ForegroundColor Red }
        }
        Write-Host ""
        $continue = Read-Host "Press ENTER to return to menu or type 'exit' to quit"
    } while ($continue -ne "exit")
} else {
    Show-Banner
    python run_hospital_system.py $Mode
}
