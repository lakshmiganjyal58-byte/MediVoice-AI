from appointment_service import (
    check_doctor_availability,
    book_appointment,
    cancel_appointment
)

# Test 1: Check doctor availability
print("TEST 1: Doctor Availability")
print(check_doctor_availability())

# Test 2: Book an appointment
print("\nTEST 2: Book Appointment")
result = book_appointment(
    "Test Patient",
    "9876543210",
    "Dr. Ananya Sharma",
    "2026-11-25",
    "10:00 AM"
)
print(result)

# Test 3: Cancel the appointment
print("\nTEST 3: Cancel Appointment")
print(cancel_appointment("9876543210"))