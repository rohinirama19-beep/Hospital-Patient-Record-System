/**
 * Medical Records Page Controller
 */

let patientsData = [];
let doctorsData = [];
let appointmentsData = [];

document.addEventListener("DOMContentLoaded", async () => {
  if (!checkAuth()) return;

  await Promise.all([loadPatients(), loadDoctors(), loadAppointments()]);
  loadMedicalRecords();

  // Search
  document.getElementById("recordSearchBtn").addEventListener("click", () => {
    const q = document.getElementById("recordSearchInput").value.trim();
    loadMedicalRecords(q);
  });

  document.getElementById("recordSearchInput").addEventListener("keyup", (e) => {
    if (e.key === "Enter") {
      loadMedicalRecords(e.target.value.trim());
    }
  });

  document.getElementById("recordResetBtn").addEventListener("click", () => {
    document.getElementById("recordSearchInput").value = "";
    loadMedicalRecords();
  });

  // Modal Listeners
  const modal = document.getElementById("recordModal");
  const openBtn = document.getElementById("openAddRecordBtn");
  const closeBtn = document.getElementById("closeRecordModal");
  const cancelBtn = document.getElementById("cancelRecordBtn");
  const form = document.getElementById("recordForm");

  openBtn.addEventListener("click", () => openRecordModal());
  closeBtn.addEventListener("click", () => closeModal(modal));
  cancelBtn.addEventListener("click", () => closeModal(modal));

  form.addEventListener("submit", handleSaveRecord);

  // View modal
  const viewModal = document.getElementById("viewRecordModal");
  document.getElementById("closeViewRecordModal").addEventListener("click", () => closeModal(viewModal));
  document.getElementById("closeViewRecordBtn").addEventListener("click", () => closeModal(viewModal));
});

async function loadPatients() {
  try {
    patientsData = await apiFetch("/api/patients");
    const pSelect = document.getElementById("formRecordPatient");
    pSelect.innerHTML = '<option value="">Select Patient</option>' +
      patientsData.map(p => `<option value="${p.patient_id}">${escapeHtml(p.patient_name)} (#${p.patient_id})</option>`).join("");
  } catch (err) {
    console.error("Failed to load patients:", err);
  }
}

async function loadDoctors() {
  try {
    doctorsData = await apiFetch("/api/doctors");
    const dSelect = document.getElementById("formRecordDoctor");
    dSelect.innerHTML = '<option value="">Select Doctor</option>' +
      doctorsData.map(d => `<option value="${d.doctor_id}">${escapeHtml(d.doctor_name)} — ${escapeHtml(d.specialization)}</option>`).join("");
  } catch (err) {
    console.error("Failed to load doctors:", err);
  }
}

async function loadAppointments() {
  try {
    appointmentsData = await apiFetch("/api/appointments");
    const aSelect = document.getElementById("formRecordAppt");
    aSelect.innerHTML = '<option value="">None / Walk-in Consultation</option>' +
      appointmentsData.map(a => `<option value="${a.appointment_id}">Appt #${a.appointment_id} — ${escapeHtml(a.patient_name)} with ${escapeHtml(a.doctor_name)} (${a.appointment_date})</option>`).join("");
  } catch (err) {
    console.error("Failed to load appointments:", err);
  }
}

async function loadMedicalRecords(search = "") {
  const tableBody = document.getElementById("recordsTableBody");
  const countLabel = document.getElementById("recordCountLabel");

  try {
    const url = search ? `/api/medical-records?search=${encodeURIComponent(search)}` : "/api/medical-records";
    const records = await apiFetch(url);

    countLabel.textContent = `Showing ${records.length} record${records.length === 1 ? '' : 's'}`;

    if (records.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 24px;">No medical records found.</td></tr>';
      return;
    }

    tableBody.innerHTML = records.map(r => `
      <tr>
        <td><strong>#${r.record_id}</strong></td>
        <td><strong>${escapeHtml(r.patient_name)}</strong></td>
        <td>${escapeHtml(r.doctor_name)}</td>
        <td><strong>${escapeHtml(r.diagnosis)}</strong></td>
        <td>${escapeHtml(r.treatment)}</td>
        <td>${r.record_date}</td>
        <td style="text-align: right;">
          <div class="btn-group">
            <button class="btn btn-outline btn-sm" onclick="viewRecord(${r.record_id})">View</button>
            <button class="btn btn-outline btn-sm" onclick="editRecord(${r.record_id})">Edit</button>
          </div>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    tableBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--danger-text); padding: 24px;">Failed to load clinical records.</td></tr>';
  }
}

function openRecordModal(rec = null) {
  const modal = document.getElementById("recordModal");
  const title = document.getElementById("recordModalTitle");
  const form = document.getElementById("recordForm");

  form.reset();
  document.getElementById("editRecordId").value = "";

  const pGroup = document.getElementById("patientSelectGroup");
  const dGroup = document.getElementById("doctorSelectGroup");
  const aGroup = document.getElementById("apptSelectGroup");

  if (rec) {
    title.textContent = `Edit Medical Record #${rec.record_id}`;
    document.getElementById("editRecordId").value = rec.record_id;
    document.getElementById("formRecordDiagnosis").value = rec.diagnosis;
    document.getElementById("formRecordTreatment").value = rec.treatment;
    document.getElementById("formRecordNotes").value = rec.notes || "";
    // Hide patient/doctor in edit mode (master linkage)
    pGroup.style.display = "none";
    dGroup.style.display = "none";
    aGroup.style.display = "none";
  } else {
    title.textContent = "Create Clinical Medical Record";
    pGroup.style.display = "block";
    dGroup.style.display = "block";
    aGroup.style.display = "block";
  }

  modal.classList.add("active");
}

function closeModal(modalEl) {
  modalEl.classList.remove("active");
}

async function handleSaveRecord(e) {
  e.preventDefault();
  const id = document.getElementById("editRecordId").value;
  const isEdit = Boolean(id);

  const saveBtn = document.getElementById("saveRecordBtn");
  saveBtn.disabled = true;
  saveBtn.textContent = "Saving...";

  try {
    if (isEdit) {
      const payload = {
        diagnosis: document.getElementById("formRecordDiagnosis").value.trim(),
        treatment: document.getElementById("formRecordTreatment").value.trim(),
        notes: document.getElementById("formRecordNotes").value.trim()
      };
      await apiFetch(`/api/medical-records/${id}`, {
        method: "PUT",
        body: JSON.stringify(payload)
      });
      showToast("Medical record updated successfully.");
    } else {
      const apptVal = document.getElementById("formRecordAppt").value;
      const payload = {
        patient_id: parseInt(document.getElementById("formRecordPatient").value),
        doctor_id: parseInt(document.getElementById("formRecordDoctor").value),
        appointment_id: apptVal ? parseInt(apptVal) : null,
        diagnosis: document.getElementById("formRecordDiagnosis").value.trim(),
        treatment: document.getElementById("formRecordTreatment").value.trim(),
        notes: document.getElementById("formRecordNotes").value.trim()
      };
      await apiFetch("/api/medical-records", {
        method: "POST",
        body: JSON.stringify(payload)
      });
      showToast("Medical record saved successfully.");
    }

    closeModal(document.getElementById("recordModal"));
    loadMedicalRecords();
  } catch (err) {
    // Handled in apiFetch
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = "Save Medical Record";
  }
}

async function editRecord(recordId) {
  try {
    const rec = await apiFetch(`/api/medical-records/${recordId}`);
    openRecordModal(rec);
  } catch (err) {
    showToast("Could not retrieve medical record details.", true);
  }
}

async function viewRecord(recordId) {
  const modal = document.getElementById("viewRecordModal");
  const body = document.getElementById("viewRecordBody");

  try {
    const rec = await apiFetch(`/api/medical-records/${recordId}`);
    document.getElementById("viewRecordTitle").textContent = `Clinical Record #${rec.record_id} — ${rec.patient_name}`;

    let prescHtml = '<p style="color: var(--text-muted); font-size: 13px;">No prescriptions attached to this visit.</p>';
    if (rec.prescriptions && rec.prescriptions.length > 0) {
      prescHtml = `
        <table class="data-table" style="margin-top: 8px;">
          <thead>
            <tr>
              <th>Medicine</th>
              <th>Dosage</th>
              <th>Frequency</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody>
            ${rec.prescriptions.map(p => `
              <tr>
                <td><strong>${escapeHtml(p.medicine_name)}</strong></td>
                <td>${escapeHtml(p.dosage)}</td>
                <td>${escapeHtml(p.frequency)}</td>
                <td>${p.duration_days} days</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;
    }

    body.innerHTML = `
      <div style="font-size: 13px; line-height: 1.6;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; background: var(--bg-surface); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-color);">
          <div><span style="color: var(--text-muted);">Patient:</span> <strong>${escapeHtml(rec.patient_name)}</strong> (#${rec.patient_id})</div>
          <div><span style="color: var(--text-muted);">Physician:</span> <strong>${escapeHtml(rec.doctor_name)}</strong></div>
          <div><span style="color: var(--text-muted);">Record Date:</span> <strong>${rec.record_date}</strong></div>
          <div><span style="color: var(--text-muted);">Appointment ID:</span> <strong>${rec.appointment_id ? '#' + rec.appointment_id : 'Walk-in'}</strong></div>
        </div>

        <div style="margin-bottom: 14px;">
          <h4 style="color: var(--text-muted); font-size: 11px; text-transform: uppercase;">Diagnosis</h4>
          <p style="font-size: 15px; font-weight: 600; color: var(--text-primary); margin-top: 2px;">${escapeHtml(rec.diagnosis)}</p>
        </div>

        <div style="margin-bottom: 14px;">
          <h4 style="color: var(--text-muted); font-size: 11px; text-transform: uppercase;">Treatment Protocol</h4>
          <p style="color: var(--text-primary); margin-top: 2px;">${escapeHtml(rec.treatment)}</p>
        </div>

        <div style="margin-bottom: 18px;">
          <h4 style="color: var(--text-muted); font-size: 11px; text-transform: uppercase;">Physician Clinical Notes</h4>
          <p style="color: var(--text-secondary); margin-top: 2px; font-style: italic;">${escapeHtml(rec.notes || 'None recorded.')}</p>
        </div>

        <div>
          <h4 style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; margin-bottom: 4px;">Prescribed Medications</h4>
          ${prescHtml}
        </div>
      </div>
    `;

    modal.classList.add("active");
  } catch (err) {
    showToast("Failed to load medical record details.", true);
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
