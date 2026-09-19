/**
 * Prescriptions Page Controller
 */

let medicalRecordsData = [];

document.addEventListener("DOMContentLoaded", async () => {
  if (!checkAuth()) return;

  await loadRecordsDropdown();
  loadPrescriptions();

  // Modal Listeners
  const modal = document.getElementById("prescriptionModal");
  const openBtn = document.getElementById("openAddPrescriptionBtn");
  const closeBtn = document.getElementById("closePrescriptionModal");
  const cancelBtn = document.getElementById("cancelPrescBtn");
  const form = document.getElementById("prescriptionForm");

  openBtn.addEventListener("click", () => {
    form.reset();
    modal.classList.add("active");
  });

  closeBtn.addEventListener("click", () => modal.classList.remove("active"));
  cancelBtn.addEventListener("click", () => modal.classList.remove("active"));

  form.addEventListener("submit", handleSavePrescription);
});

async function loadRecordsDropdown() {
  try {
    medicalRecordsData = await apiFetch("/api/medical-records");
    const recSelect = document.getElementById("formPrescRecord");
    recSelect.innerHTML = '<option value="">Select Medical Record</option>' +
      medicalRecordsData.map(r => `<option value="${r.record_id}">Record #${r.record_id} — ${escapeHtml(r.patient_name)} (${escapeHtml(r.diagnosis)})</option>`).join("");
  } catch (err) {
    console.error("Failed to load medical records for dropdown:", err);
  }
}

async function loadPrescriptions() {
  const tableBody = document.getElementById("prescriptionsTableBody");
  const countLabel = document.getElementById("prescCountLabel");

  try {
    const prescriptions = await apiFetch("/api/prescriptions");
    countLabel.textContent = `Total ${prescriptions.length} medication${prescriptions.length === 1 ? '' : 's'} prescribed`;

    if (prescriptions.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 24px;">No prescriptions on file.</td></tr>';
      return;
    }

    tableBody.innerHTML = prescriptions.map(p => `
      <tr>
        <td><strong>#${p.prescription_id}</strong></td>
        <td><strong>${escapeHtml(p.patient_name)}</strong></td>
        <td><strong>${escapeHtml(p.medicine_name)}</strong></td>
        <td>${escapeHtml(p.dosage)}</td>
        <td>${escapeHtml(p.frequency)}</td>
        <td>${p.duration_days} days</td>
        <td>${escapeHtml(p.doctor_name)}</td>
        <td><span style="color: var(--text-secondary);">${escapeHtml(p.diagnosis)}</span></td>
      </tr>
    `).join("");
  } catch (err) {
    tableBody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--danger-text); padding: 24px;">Failed to load prescriptions.</td></tr>';
  }
}

async function handleSavePrescription(e) {
  e.preventDefault();
  const saveBtn = document.getElementById("savePrescBtn");
  saveBtn.disabled = true;
  saveBtn.textContent = "Issuing...";

  const payload = {
    record_id: parseInt(document.getElementById("formPrescRecord").value),
    medicine_name: document.getElementById("formPrescMedicine").value.trim(),
    dosage: document.getElementById("formPrescDosage").value.trim(),
    duration_days: parseInt(document.getElementById("formPrescDuration").value),
    frequency: document.getElementById("formPrescFrequency").value.trim()
  };

  try {
    await apiFetch("/api/prescriptions", {
      method: "POST",
      body: JSON.stringify(payload)
    });
    showToast("Prescription issued successfully.");
    document.getElementById("prescriptionModal").classList.remove("active");
    loadPrescriptions();
  } catch (err) {
    // Handled in apiFetch
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = "Issue Prescription";
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
