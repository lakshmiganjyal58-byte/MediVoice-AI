from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from appointment_service import (
    check_doctor_availability,
    book_appointment,
    cancel_appointment,
    load_appointments
)

app = FastAPI(title="MediVoice AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class BookingRequest(BaseModel):
    patient_name: str
    phone_number: str
    doctor_name: str
    date: str
    time: str

class CancellationRequest(BaseModel):
    phone_number: str

@app.get("/")
def home():
    return {"message": "MediVoice AI Backend is running!"}

@app.get("/doctors")
def get_doctors():
    return check_doctor_availability()

@app.get("/appointments")
def get_appointments():
    return load_appointments()

@app.post("/book")
def create_booking(data: BookingRequest):
    return book_appointment(
        data.patient_name,
        data.phone_number,
        data.doctor_name,
        data.date,
        data.time
    )

@app.post("/cancel")
def cancel_booking(data: CancellationRequest):
    return cancel_appointment(data.phone_number)