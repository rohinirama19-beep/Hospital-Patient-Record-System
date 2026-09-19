/**
 * Patients Page Controller
 */

let patientsList = [];

document.addEventListener("DOMContentLoaded", () => {
  if (!checkAuth()) return;

  loadPatients();

  // Search Listeners
  document.getElementById("patientSearchBtn").addEventListener("click", () => {
    const q = document.getElementById("patientSearchInput").value.trim();
    loadPatients(q);
  });

  document.getElementById("patientSearchInput").addEventListener("keyup", (e) => {
    if (e.key === "Enter") {
      loadPatients(e.target.value.trim());
    }
  });

  document.getElementById("patientResetBtn").addEventListener("click", () => {
    document.getElementById("patientSearchInput").value = "";
    loadPatients();
  });

  // Modal Listeners
  const modal = document.getElementById("patientModal");
  const openAddBtn = document.getElementById("openAddPatientBtn");
  const closeBtn = document.getElementById("closePatientModal");
  const cancelBtn = document.getElementById("cancelPatientBtn");
  const form = document.getElementById("patientForm");

  openAddBtn.addEventListener("click", () => {
    openPatientModal();
  });

  closeBtn.addEventListener("click", () => closeModal(modal));
  cancelBtn.addEventListener("click", () => closeModal(modal));

  form.addEventListener("submit", handleSavePatient);

  // Details Modal Listeners
  const detailsModal = document.getElementById("patientDetailsModal");
  document.getElementById("closeDetailsModal").addEventListener("click", () => closeModal(detailsModal));
  document.getElementById("closeDetailsBtn").addEventListener("click", () => closeModal(detailsModal));
});

async function loadPatients(searchQuery = "") {
  const tableBody = document.getElementById("patientsTableBody");
  const countLabel = document.getElementById("patientCountLabel");
  
  try {
    const url = searchQuery ? `/api/patients?search=${encodeURIComponent(searchQuery)}` : "/api/patients";
    patientsList = await apiFetch(url);
    
    countLabel.textContent = `Showing ${patientsList.length} patient${patientsList.length === 1 ? '' : 's'}`;

    if (patientsList.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 24px;">No matching patient records found.</td></tr>';
      return;
    }

    tableBody.innerHTML = patientsList.map(p => `
      <tr>
        <td><strong>#${p.patient_id}</strong></td>
        <td><strong>${escapeHtml(p.patient_name)}</strong></td>
        <td>${p.date_of_birth}</td>
        <td>${p.gender}</td>
        <td>${escapeHtml(p.phone)}</td>
        <td><span class="badge" style="background-color: var(--bg-surface); border: 1px solid var(--border-color);">${p.blood_group}</span></td>
        <td style="text-align: right;">
          <div class="btn-group">
            <button class="btn btn-outline btn-sm" onclick="viewPatientDetails(${p.patient_id})">View</button>
            <button class="btn btn-outline btn-sm" onclick="editPatient(${p.patient_id})">Edit</button>
            <button class="btn btn-danger btn-sm" onclick="deletePatient(${p.patient_id})">Delete</button>
          </div>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    tableBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--danger-text); padding: 24px;">Failed to load patient records.</td></tr>';
  }
}

function openPatientModal(patient = null) {
  const modal = document.getElementById("patientModal");
  const title = document.getElementById("patientModalTitle");
  const form = document.getElementById("patientForm");
  
  form.reset();
  document.getElementById("editPatientId").value = "";

  if (patient) {
    title.textContent = `Edit Patient #${patient.patient_id}`;
    document.getElementById("editPatientId").value = patient.patient_id;
    document.getElementById("formPatientName").value = patient.patient_name;
    document.getElementById("formPatientDOB").value = patient.date_of_birth;
    document.getElementById("formPatientGender").value = patient.gender;
    document.getElementById("formPatientPhone").value = patient.phone;
    document.getElementById("formPatientBlood").value = patient.blood_group;
    document.getElementById("formPatientEmail").value = patient.email;
    document.getElementById("formPatientAddress").value = patient.address;
  } else {
    title.textContent = "Register New Patient";
  }

  modal.classList.add("active");
}

function closeModal(modalEl) {
  modalEl.classList.remove("active");
}

async function handleSavePatient(e) {
  e.preventDefault();
  const id = document.getElementById("editPatientId").value;
  const isEdit = Boolean(id);

  const payload = {
    patient_name: document.getElementById("formPatientName").value.trim(),
    date_of_birth: document.getElementById("formPatientDOB").value,
    gender: document.getElementById("formPatientGender").value,
    phone: document.getElementById("formPatientPhone").value.trim(),
    email: document.getElementById("formPatientEmail").value.trim(),
    address: document.getElementById("formPatientAddress").value.trim(),
    blood_group: document.getElementById("formPatientBlood").value
  };

  const saveBtn = document.getElementById("savePatientBtn");
  saveBtn.disabled = true;
  saveBtn.textContent = "Saving...";

  try {
    if (isEdit) {
      await apiFetch(`/api/patients/${id}`, {
        method: "PUT",
        body: JSON.stringify(payload)
      });
      showToast("Patient record updated successfully.");
    } else {
      await apiFetch("/api/patients", {
        method: "POST",
        body: JSON.stringify(payload)
      });
      showToast("New patient registered successfully.");
    }

    closeModal(document.getElementById("patientModal"));
    loadPatients();
  } catch (err) {
    // Toast handled in apiFetch
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = "Save Patient";
  }
}

async function editPatient(patientId) {
  try {
    const patient = await apiFetch(`/api/patients/${patientId}`);
    openPatientModal(patient);
  } catch (err) {
    showToast("Could not retrieve patient details.", true);
  }
}

async function deletePatient(patientId) {
  if (!confirm(`Are you sure you want to delete patient #${patientId}? This cannot be undone.`)) {
    return;
  }

  try {
    await apiFetch(`/api/patients/${patientId}`, { method: "DELETE" });
    showToast("Patient deleted successfully.");
    loadPatients();
  } catch (err) {
    // Handled in apiFetch
  }
}

async function viewPatientDetails(patientId) {
  const modal = document.getElementById("patientDetailsModal");
  const demoBody = document.getElementById("demographicCardBody");
  const apptsBody = document.getElementById("detailApptsBody");
  const medBody = document.getElementById("detailMedHistoryBody");
  const billsBody = document.getElementById("detailBillsBody");

  try {
    const data = await apiFetch(`/api/patients/${patientId}/details`);
    const p = data.patient;

    document.getElementById("detailsModalTitle").textContent = `${p.patient_name} — Medical Profile (#${p.patient_id})`;

    demoBody.innerHTML = `
      <div><span style="color: var(--text-muted);">DOB:</span> <strong>${p.date_of_birth}</strong></div>
      <div><span style="color: var(--text-muted);">Gender:</span> <strong>${p.gender}</strong></div>
      <div><span style="color: var(--text-muted);">Blood Group:</span> <strong>${p.blood_group}</strong></div>
      <div><span style="color: var(--text-muted);">Phone:</span> <strong>${escapeHtml(p.phone)}</strong></div>
      <div><span style="color: var(--text-muted);">Email:</span> <strong>${escapeHtml(p.email)}</strong></div>
      <div><span style="color: var(--text-muted);">Address:</span> <strong>${escapeHtml(p.address)}</strong></div>
    `;

    // Appointments
    if (data.appointments.length === 0) {
      apptsBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No recorded appointments.</td></tr>';
    } else {
      apptsBody.innerHTML = data.appointments.map(a => `
        <tr>
          <td>#${a.appointment_id}</td>
          <td>${escapeHtml(a.doctor_name)}</td>
          <td>${a.appointment_date} ${a.appointment_time}</td>
          <td>${escapeHtml(a.reason)}</td>
          <td><span class="badge badge-${a.status.toLowerCase()}">${a.status}</span></td>
        </tr>
      `).join("");
    }

    // Medical History
    if (data.medical_history.length === 0) {
      medBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No clinical records on file.</td></tr>';
    } else {
      medBody.innerHTML = data.medical_history.map(m => `
        <tr>
          <td>#${m.record_id}</td>
          <td>${escapeHtml(m.doctor_name)}</td>
          <td><strong>${escapeHtml(m.diagnosis)}</strong></td>
          <td>${escapeHtml(m.treatment)}</td>
          <td>${m.record_date}</td>
        </tr>
      `).join("");
    }

    // Bills
    if (data.bills.length === 0) {
      billsBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted);">No billing transactions found.</td></tr>';
    } else {
      billsBody.innerHTML = data.bills.map(b => `
        <tr>
          <td>#${b.bill_id}</td>
          <td>${b.appointment_id ? '#' + b.appointment_id : '—'}</td>
          <td>${b.bill_date}</td>
          <td>INR ${parseFloat(b.consultation_fee).toFixed(2)}</td>
          <td>INR ${parseFloat(b.medicine_fee).toFixed(2)}</td>
          <td><strong>INR ${parseFloat(b.total_amount).toFixed(2)}</strong></td>
          <td><span class="badge badge-${b.payment_status.toLowerCase()}">${b.payment_status}</span></td>
        </tr>
      `).join("");
    }

    modal.classList.add("active");
  } catch (err) {
    showToast("Could not load patient details profile.", true);
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
