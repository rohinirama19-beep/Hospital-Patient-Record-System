/**
 * Dashboard Controller
 */

document.addEventListener("DOMContentLoaded", async () => {
  if (!checkAuth()) return;

  try {
    const data = await apiFetch("/api/dashboard");
    
    // Update Stats
    document.getElementById("statPatients").textContent = data.stats.total_patients;
    document.getElementById("statDoctors").textContent = data.stats.total_doctors;
    document.getElementById("statTodayAppts").textContent = data.stats.today_appointments;
    document.getElementById("statRecords").textContent = data.stats.total_records;
    document.getElementById("statPendingBills").textContent = data.stats.pending_bills;

    // Render Recent Appointments
    const apptBody = document.getElementById("recentAppointmentsBody");
    if (!data.recent_appointments || data.recent_appointments.length === 0) {
      apptBody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">No appointments recorded.</td></tr>';
    } else {
      apptBody.innerHTML = data.recent_appointments.map(a => `
        <tr>
          <td><strong>${escapeHtml(a.patient_name)}</strong></td>
          <td>${escapeHtml(a.doctor_name)}</td>
          <td>${a.appointment_date} <span style="font-size: 11px; color: var(--text-muted);">${a.appointment_time}</span></td>
          <td><span class="badge badge-${a.status.toLowerCase()}">${a.status}</span></td>
        </tr>
      `).join("");
    }

    // Render Recent Medical Records
    const recBody = document.getElementById("recentRecordsBody");
    if (!data.recent_records || data.recent_records.length === 0) {
      recBody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">No medical records found.</td></tr>';
    } else {
      recBody.innerHTML = data.recent_records.map(r => `
        <tr>
          <td><strong>${escapeHtml(r.patient_name)}</strong></td>
          <td>${escapeHtml(r.doctor_name)}</td>
          <td>${escapeHtml(r.diagnosis)}</td>
          <td>${r.record_date}</td>
        </tr>
      `).join("");
    }
  } catch (err) {
    console.error("Dashboard error:", err);
  }
});

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
