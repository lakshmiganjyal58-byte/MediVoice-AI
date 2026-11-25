import json
from pathlib import Path

# Location of our appointment storage file
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "appointments.json"

# Sample doctors and their specialities
DOCTORS = [
    {
        "id": 1,
        "name": "Dr. Ananya Sharma",
        "speciality": "Cardiologist",
        "slots": ["10:00 AM", "11:00 AM", "02:00 PM"]
    },
    {
        "id": 2,
        "name": "Dr. Rahul Mehta",
        "speciality": "Dermatologist",
        "slots": ["09:00 AM", "12:00 PM", "03:00 PM"]
    },
    {
        "id": 3,
        "name": "Dr. Priya Nair",
        "speciality": "General Physician",
        "slots": ["10:00 AM", "01:00 PM", "04:00 PM"]
    }
]


def load_appointments():
    """Load saved appointments from the JSON file."""
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_appointments(appointments):
    """Save appointments to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(appointments, file, indent=4)


def check_doctor_availability(doctor_name=None, date=None):
    """Check available appointment slots."""

    appointments = load_appointments()
    results = []

    for doctor in DOCTORS:
        if doctor_name and doctor_name.lower() not in doctor["name"].lower():
            continue

        available_slots = []

        for slot in doctor["slots"]:
            already_booked = any(
                appointment["doctor_name"] == doctor["name"]
                and appointment["date"] == date
                and appointment["time"] == slot
                and appointment["status"] == "Booked"
                for appointment in appointments
            )

            if not already_booked:
                available_slots.append(slot)

        results.append({
            "doctor_name": doctor["name"],
            "speciality": doctor["speciality"],
            "available_slots": available_slots
        })

    return results


def book_appointment(patient_name, phone_number, doctor_name, date, time):
    """Book an appointment for a patient."""

    if len(phone_number) != 10 or not phone_number.isdigit():
        return {"success": False, "message": "Enter a valid 10-digit phone number."}

    appointments = load_appointments()

    doctor = next(
        (d for d in DOCTORS if d["name"].lower() == doctor_name.lower()),
        None
    )

    if doctor is None:
        return {"success": False, "message": "Doctor not found."}

    if time not in doctor["slots"]:
        return {"success": False, "message": "Invalid appointment time."}

    available = check_doctor_availability(doctor_name, date)

    if not available or time not in available[0]["available_slots"]:
        return {"success": False, "message": "This slot is already booked."}

    appointment = {
        "id": len(appointments) + 1,
        "patient_name": patient_name,
        "phone_number": phone_number,
        "doctor_name": doctor["name"],
        "speciality": doctor["speciality"],
        "date": date,
        "time": time,
        "status": "Booked"
    }

    appointments.append(appointment)
    save_appointments(appointments)

    return {
        "success": True,
        "message": "Appointment booked successfully.",
        "appointment": appointment
    }


def cancel_appointment(phone_number):
    """Cancel an appointment using the patient's phone number."""

    if len(phone_number) != 10 or not phone_number.isdigit():
        return {"success": False, "message": "Enter a valid 10-digit phone number."}

    appointments = load_appointments()

    for appointment in appointments:
        if (
            appointment["phone_number"] == phone_number
            and appointment["status"] == "Booked"
        ):
            appointment["status"] = "Cancelled"
            save_appointments(appointments)

            return {
                "success": True,
                "message": "Appointment cancelled successfully.",
                "appointment": appointment
            }

    return {
        "success": False,
        "message": "No active appointment found for this phone number."
    }