"""
Pydantic Schemas for Request and Response Validation
"""

from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=1)

class PatientCreate(BaseModel):
    patient_name: str = Field(..., min_length=2, max_length=100)
    date_of_birth: str
    gender: str = Field(..., pattern="^(MALE|FEMALE|OTHER)$")
    phone: str = Field(..., min_length=7, max_length=15)
    email: str = Field(..., min_length=5, max_length=100)
    address: str = Field(..., min_length=3, max_length=255)
    blood_group: str = Field(..., pattern="^(A\+|A-|B\+|B-|AB\+|AB-|O\+|O-)$")

class PatientUpdate(PatientCreate):
    pass

class DoctorCreate(BaseModel):
    doctor_name: str = Field(..., min_length=2, max_length=100)
    specialization: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=7, max_length=15)
    email: str = Field(..., min_length=5, max_length=100)
    department_id: int

class DoctorUpdate(DoctorCreate):
    pass

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str
    appointment_time: str
    reason: str = Field(..., min_length=2, max_length=255)
    status: Optional[str] = "SCHEDULED"

class AppointmentUpdate(BaseModel):
    appointment_date: str
    appointment_time: str
    reason: str
    status: str = Field(..., pattern="^(SCHEDULED|COMPLETED|CANCELLED)$")

class AppointmentStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(SCHEDULED|COMPLETED|CANCELLED)$")

class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    diagnosis: str = Field(..., min_length=2, max_length=255)
    treatment: str = Field(..., min_length=2, max_length=255)
    notes: Optional[str] = ""

class MedicalRecordUpdate(BaseModel):
    diagnosis: str
    treatment: str
    notes: Optional[str] = ""

class PrescriptionCreate(BaseModel):
    record_id: int
    medicine_name: str = Field(..., min_length=2, max_length=100)
    dosage: str = Field(..., min_length=1, max_length=50)
    frequency: str = Field(..., min_length=1, max_length=50)
    duration_days: int = Field(..., gt=0)

class BillGenerateRequest(BaseModel):
    appointment_id: int
    consultation_fee: float = Field(..., ge=0.0)
    medicine_fee: float = Field(default=0.0, ge=0.0)

class BillStatusUpdate(BaseModel):
    payment_status: str = Field(..., pattern="^(PAID|PENDING)$")
