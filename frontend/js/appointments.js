/**
 * Appointments Page Controller
 */

let patientsData = [];
let doctorsData = [];

document.addEventListener("DOMContentLoaded", async () => {
  if (!checkAuth()) return;

  await Promise.all([loadPatientsDropdown(), loadDoctorsDropdown()]);
  loadAppointments();

  // Filter Listeners
  document.getElementById("applyFiltersBtn").addEventListener("click", () => {
    const d = document.getElementById("filterDateInput").value;
    const s = document.getElementById("filterStatusSelect").value;
    loadAppointments(d, s);
  });

  document.getElementById("resetFiltersBtn").addEventListener("click", () => {
    document.getElementById("filterDateInput").value = "";
    document.getElementById("filterStatusSelect").value = "";
    loadAppointments();
  });

  // Modal Listeners
  const modal = document.getElementById("appointmentModal");
  const openBtn = document.getElementById("openBookApptBtn");
  const closeBtn = document.getElementById("closeApptModal");
  const cancelBtn = document.getElementById("cancelApptBtn");
  const form = document.getElementById("appointmentForm");

  openBtn.addEventListener("click", () => openApptModal());
  closeBtn.addEventListener("click", () => closeModal(modal));
  cancelBtn.addEventListener("click", () => closeModal(modal));

  form.addEventListener("submit", handleSaveAppointment);
});

async function loadPatientsDropdown() {
  try {
    patientsData = await apiFetch("/api/patients");
    const pSelect = document.getElementById("formApptPatient");
    pSelect.innerHTML = '<option value="">Choose Patient</option>' +
      patientsData.map(p => `<option value="${p.patient_id}">${escapeHtml(p.patient_name)} (#${p.patient_id})</option>`).join("");
  } catch (err) {
    console.error("Failed to load patients for dropdown:", err);
  }
}

async function loadDoctorsDropdown() {
  try {
    doctorsData = await apiFetch("/api/doctors");
    const dSelect = document.getElementById("formApptDoctor");
    dSelect.innerHTML = '<option value="">Choose Doctor</option>' +
      doctorsData.map(d => `<option value="${d.doctor_id}">${escapeHtml(d.doctor_name)} — ${escapeHtml(d.specialization)}</option>`).join("");
  } catch (err) {
    console.error("Failed to load doctors for dropdown:", err);
  }
}

async function loadAppointments(date = "", status = "") {
  const tableBody = document.getElementById("appointmentsTableBody");
  const countLabel = document.getElementById("apptCountLabel");

  try {
    let queryParams = [];
    if (date) queryParams.push(`date=${encodeURIComponent(date)}`);
    if (status) queryParams.push(`status=${encodeURIComponent(status)}`);
    const qs = queryParams.length ? `?${queryParams.join("&")}` : "";

    const appts = await apiFetch(`/api/appointments${qs}`);
    countLabel.textContent = `Showing ${appts.length} appointment${appts.length === 1 ? '' : 's'}`;

    if (appts.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 24px;">No appointments match the selected criteria.</td></tr>';
      return;
    }

    tableBody.innerHTML = appts.map(a => {
      let actionButtons = `
        <button class="btn btn-outline btn-sm" onclick="editAppointment(${a.appointment_id})">Edit</button>
      `;

      if (a.status === 'SCHEDULED') {
        actionButtons += `
          <button class="btn btn-outline btn-sm" style="color: var(--success-text);" onclick="updateStatus(${a.appointment_id}, 'COMPLETED')">Complete</button>
          <button class="btn btn-danger btn-sm" onclick="updateStatus(${a.appointment_id}, 'CANCELLED')">Cancel</button>
        `;
      }

      return `
        <tr>
          <td><strong>#${a.appointment_id}</strong></td>
          <td><strong>${escapeHtml(a.patient_name)}</strong></td>
          <td>${escapeHtml(a.doctor_name)} <span style="font-size: 11px; color: var(--text-muted);">(${escapeHtml(a.specialization)})</span></td>
          <td>${a.appointment_date}</td>
          <td>${a.appointment_time}</td>
          <td>${escapeHtml(a.reason)}</td>
          <td><span class="badge badge-${a.status.toLowerCase()}">${a.status}</span></td>
          <td style="text-align: right;">
            <div class="btn-group">${actionButtons}</div>
          </td>
        </tr>
      `;
    }).join("");
  } catch (err) {
    tableBody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--danger-text); padding: 24px;">Failed to load appointments.</td></tr>';
  }
}

function openApptModal(appt = null) {
  const modal = document.getElementById("appointmentModal");
  const title = document.getElementById("apptModalTitle");
  const form = document.getElementById("appointmentForm");
  const statusContainer = document.getElementById("statusFieldContainer");

  form.reset();
  document.getElementById("editApptId").value = "";

  if (appt) {
    title.textContent = `Edit Appointment #${appt.appointment_id}`;
    document.getElementById("editApptId").value = appt.appointment_id;
    document.getElementById("formApptPatient").value = appt.patient_id;
    document.getElementById("formApptPatient").disabled = true;
    document.getElementById("formApptDoctor").value = appt.doctor_id;
    document.getElementById("formApptDoctor").disabled = true;
    document.getElementById("formApptDate").value = appt.appointment_date;
    document.getElementById("formApptTime").value = appt.appointment_time;
    document.getElementById("formApptReason").value = appt.reason;
    document.getElementById("formApptStatus").value = appt.status;
    statusContainer.style.display = "block";
  } else {
    title.textContent = "Schedule Consultation Appointment";
    document.getElementById("formApptPatient").disabled = false;
    document.getElementById("formApptDoctor").disabled = false;
    statusContainer.style.display = "none";
    // Default date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.getElementById("formApptDate").value = tomorrow.toISOString().split("T")[0];
    document.getElementById("formApptTime").value = "10:00 AM";
  }

  modal.classList.add("active");
}

function closeModal(modalEl) {
  modalEl.classList.remove("active");
}

async function handleSaveAppointment(e) {
  e.preventDefault();
  const id = document.getElementById("editApptId").value;
  const isEdit = Boolean(id);

  const saveBtn = document.getElementById("saveApptBtn");
  saveBtn.disabled = true;
  saveBtn.textContent = "Saving...";

  try {
    if (isEdit) {
      const payload = {
        appointment_date: document.getElementById("formApptDate").value,
        appointment_time: document.getElementById("formApptTime").value.trim(),
        reason: document.getElementById("formApptReason").value.trim(),
        status: document.getElementById("formApptStatus").value
      };
      await apiFetch(`/api/appointments/${id}`, {
        method: "PUT",
        body: JSON.stringify(payload)
      });
      showToast("Appointment updated successfully.");
    } else {
      const payload = {
        patient_id: parseInt(document.getElementById("formApptPatient").value),
        doctor_id: parseInt(document.getElementById("formApptDoctor").value),
        appointment_date: document.getElementById("formApptDate").value,
        appointment_time: document.getElementById("formApptTime").value.trim(),
        reason: document.getElementById("formApptReason").value.trim(),
        status: "SCHEDULED" // Explicitly start as SCHEDULED
      };
      await apiFetch("/api/appointments", {
        method: "POST",
        body: JSON.stringify(payload)
      });
      showToast("Appointment scheduled successfully.");
    }

    closeModal(document.getElementById("appointmentModal"));
    loadAppointments();
  } catch (err) {
    // Handled in apiFetch
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = "Confirm Appointment";
  }
}

async function editAppointment(apptId) {
  try {
    const appt = await apiFetch(`/api/appointments/${apptId}`);
    openApptModal(appt);
  } catch (err) {
    showToast("Could not retrieve appointment details.", true);
  }
}

async function updateStatus(apptId, newStatus) {
  const actionText = newStatus === 'COMPLETED' ? "mark as completed" : "cancel";
  if (!confirm(`Are you sure you want to ${actionText} appointment #${apptId}?`)) {
    return;
  }

  try {
    await apiFetch(`/api/appointments/${apptId}/status`, {
      method: "PUT",
      body: JSON.stringify({ status: newStatus })
    });
    showToast(`Appointment #${apptId} marked as ${newStatus}.`);
    loadAppointments();
  } catch (err) {
    // Handled in apiFetch
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
