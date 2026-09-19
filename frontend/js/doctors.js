/**
 * Doctors Page Controller
 */

let departmentsList = [];

document.addEventListener("DOMContentLoaded", async () => {
  if (!checkAuth()) return;

  await loadDepartments();
  loadDoctors();

  // Search Listeners
  document.getElementById("doctorSearchBtn").addEventListener("click", () => {
    const q = document.getElementById("doctorSearchInput").value.trim();
    loadDoctors(q);
  });

  document.getElementById("doctorSearchInput").addEventListener("keyup", (e) => {
    if (e.key === "Enter") {
      loadDoctors(e.target.value.trim());
    }
  });

  document.getElementById("doctorResetBtn").addEventListener("click", () => {
    document.getElementById("doctorSearchInput").value = "";
    loadDoctors();
  });

  // Modal Listeners
  const modal = document.getElementById("doctorModal");
  const openAddBtn = document.getElementById("openAddDoctorBtn");
  const closeBtn = document.getElementById("closeDoctorModal");
  const cancelBtn = document.getElementById("cancelDoctorBtn");
  const form = document.getElementById("doctorForm");

  openAddBtn.addEventListener("click", () => {
    openDoctorModal();
  });

  closeBtn.addEventListener("click", () => closeModal(modal));
  cancelBtn.addEventListener("click", () => closeModal(modal));

  form.addEventListener("submit", handleSaveDoctor);
});

async function loadDepartments() {
  try {
    departmentsList = await apiFetch("/api/departments");
    const deptSelect = document.getElementById("formDoctorDept");
    deptSelect.innerHTML = '<option value="">Select Department</option>' +
      departmentsList.map(d => `<option value="${d.department_id}">${escapeHtml(d.department_name)} (${escapeHtml(d.location)})</option>`).join("");
  } catch (err) {
    console.error("Failed to load departments:", err);
  }
}

async function loadDoctors(searchQuery = "") {
  const tableBody = document.getElementById("doctorsTableBody");
  const countLabel = document.getElementById("doctorCountLabel");

  try {
    const url = searchQuery ? `/api/doctors?search=${encodeURIComponent(searchQuery)}` : "/api/doctors";
    const doctors = await apiFetch(url);

    countLabel.textContent = `Showing ${doctors.length} doctor${doctors.length === 1 ? '' : 's'}`;

    if (doctors.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 24px;">No doctor records found.</td></tr>';
      return;
    }

    tableBody.innerHTML = doctors.map(d => `
      <tr>
        <td><strong>#${d.doctor_id}</strong></td>
        <td><strong>${escapeHtml(d.doctor_name)}</strong></td>
        <td>${escapeHtml(d.specialization)}</td>
        <td><span class="badge" style="background-color: var(--bg-surface); border: 1px solid var(--border-color);">${escapeHtml(d.department_name)}</span></td>
        <td>${escapeHtml(d.phone)}</td>
        <td>${escapeHtml(d.email)}</td>
        <td style="text-align: right;">
          <div class="btn-group">
            <button class="btn btn-outline btn-sm" onclick="editDoctor(${d.doctor_id})">Edit</button>
            <button class="btn btn-danger btn-sm" onclick="deleteDoctor(${d.doctor_id})">Delete</button>
          </div>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    tableBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--danger-text); padding: 24px;">Failed to load doctors list.</td></tr>';
  }
}

function openDoctorModal(doc = null) {
  const modal = document.getElementById("doctorModal");
  const title = document.getElementById("doctorModalTitle");
  const form = document.getElementById("doctorForm");

  form.reset();
  document.getElementById("editDoctorId").value = "";

  if (doc) {
    title.textContent = `Edit Doctor #${doc.doctor_id}`;
    document.getElementById("editDoctorId").value = doc.doctor_id;
    document.getElementById("formDoctorName").value = doc.doctor_name;
    document.getElementById("formDoctorSpec").value = doc.specialization;
    document.getElementById("formDoctorDept").value = doc.department_id;
    document.getElementById("formDoctorPhone").value = doc.phone;
    document.getElementById("formDoctorEmail").value = doc.email;
  } else {
    title.textContent = "Add New Doctor";
  }

  modal.classList.add("active");
}

function closeModal(modalEl) {
  modalEl.classList.remove("active");
}

async function handleSaveDoctor(e) {
  e.preventDefault();
  const id = document.getElementById("editDoctorId").value;
  const isEdit = Boolean(id);

  const payload = {
    doctor_name: document.getElementById("formDoctorName").value.trim(),
    specialization: document.getElementById("formDoctorSpec").value.trim(),
    department_id: parseInt(document.getElementById("formDoctorDept").value),
    phone: document.getElementById("formDoctorPhone").value.trim(),
    email: document.getElementById("formDoctorEmail").value.trim()
  };

  const saveBtn = document.getElementById("saveDoctorBtn");
  saveBtn.disabled = true;
  saveBtn.textContent = "Saving...";

  try {
    if (isEdit) {
      await apiFetch(`/api/doctors/${id}`, {
        method: "PUT",
        body: JSON.stringify(payload)
      });
      showToast("Doctor updated successfully.");
    } else {
      await apiFetch("/api/doctors", {
        method: "POST",
        body: JSON.stringify(payload)
      });
      showToast("Doctor added successfully.");
    }

    closeModal(document.getElementById("doctorModal"));
    loadDoctors();
  } catch (err) {
    // Handled in apiFetch
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = "Save Doctor";
  }
}

async function editDoctor(doctorId) {
  try {
    const doc = await apiFetch(`/api/doctors/${doctorId}`);
    openDoctorModal(doc);
  } catch (err) {
    showToast("Could not retrieve doctor details.", true);
  }
}

async function deleteDoctor(doctorId) {
  if (!confirm(`Are you sure you want to delete doctor #${doctorId}?`)) {
    return;
  }

  try {
    await apiFetch(`/api/doctors/${doctorId}`, { method: "DELETE" });
    showToast("Doctor deleted successfully.");
    loadDoctors();
  } catch (err) {
    // Handled in apiFetch
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
