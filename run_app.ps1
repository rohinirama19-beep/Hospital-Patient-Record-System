# ==============================================================================
# HOSPITAL PATIENT RECORD SYSTEM — FRONTEND & BACKEND LAUNCHER
# Oracle COE Academic Project
# ==============================================================================

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "         HOSPITAL PATIENT RECORD SYSTEM - APPLICATION LAUNCHER                 " -ForegroundColor Yellow -BackgroundColor Black
Write-Host "                       FASTAPI & WEB FRONTEND                                   " -ForegroundColor White
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path $PSScriptRoot

Write-Host "[1/3] Verifying database and dependencies..." -ForegroundColor Green
python -c "import fastapi, uvicorn; print('Dependencies verified.')"

Write-Host "[2/3] Opening browser at http://localhost:8000 ..." -ForegroundColor Green
Start-Process "http://localhost:8000"

Write-Host "[3/3] Launching FastAPI backend server..." -ForegroundColor Green
Write-Host "Press Ctrl+C at any time to stop the server." -ForegroundColor Yellow
Write-Host ""

python start_server.py
