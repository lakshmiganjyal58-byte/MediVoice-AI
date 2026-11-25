const API = "http://127.0.0.1:8000";

// Load doctors
async function loadDoctors() {
    const response = await fetch(API + "/doctors");
    const doctors = await response.json();

    const container = document.getElementById("doctors");
    container.innerHTML = "";

    doctors.forEach(doctor => {
        const div = document.createElement("div");
        div.innerHTML = `
            <h3>${doctor.doctor_name}</h3>
            <p>Speciality: ${doctor.speciality}</p>
            <p>Available Slots: ${doctor.available_slots.join(", ")}</p>
        `;
        container.appendChild(div);
    });
}

// Load appointments
async function loadAppointments() {
    const response = await fetch(API +"/appointments");
    const appointments = await response.json();

    const container = document.getElementById("appointments");
    container.innerHTML = "";

    if (appointments.length === 0) {
        container.textContent = "No appointments yet.";
        return;
    }

    appointments.forEach(appointment => {
        const div = document.createElement("div");
        div.innerHTML = `
            <p><strong>${appointment.patient_name}</strong></p>
            <p>${appointment.doctor_name} | ${appointment.date} | ${appointment.time}</p>
            <p>Status: ${appointment.status}</p>
        `;
        container.appendChild(div);
    });
}

// Book appointment
document.getElementById("bookingForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const booking = {
        patient_name: document.getElementById("patientName").value,
        phone_number: document.getElementById("phoneNumber").value,
        doctor_name: document.getElementById("doctorName").value,
        date: document.getElementById("date").value,
        time: document.getElementById("time").value
    };

    const response = await fetch(API +"/book", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(booking)
    });

    const result = await response.json();
    document.getElementById("message").textContent = result.message;

    if (result.success) {
        document.getElementById("bookingForm").reset();
        loadDoctors();
        loadAppointments();
    }
});

// Start dashboard
loadDoctors();
loadAppointments();
async function cancelAppointment() {
    const phoneNumber = document.getElementById("cancelPhone").value;

    if (!phoneNumber) {
        alert("Please enter your phone number.");
        return;
    }

    const response = await fetch(API + "/cancel", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            phone_number: phoneNumber
        })
    });

    const result = await response.json();

    alert(result.message);

    if (result.success) {
        loadAppointments();
        loadDoctors();
        document.getElementById("cancelPhone").value = "";
    }
}