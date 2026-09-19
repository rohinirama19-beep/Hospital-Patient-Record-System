/**
 * Bills Page Controller
 */

let appointmentsList = [];

document.addEventListener("DOMContentLoaded", async () => {
  if (!checkAuth()) return;

  await loadAppointmentsDropdown();
  loadBills();

  // Filter Listeners
  document.getElementById("applyBillFilterBtn").addEventListener("click", () => {
    const s = document.getElementById("billStatusFilter").value;
    loadBills(s);
  });

  document.getElementById("resetBillFilterBtn").addEventListener("click", () => {
    document.getElementById("billStatusFilter").value = "";
    loadBills();
  });

  // Modal Listeners
  const modal = document.getElementById("generateBillModal");
  const openBtn = document.getElementById("openGenerateBillBtn");
  const closeBtn = document.getElementById("closeBillModal");
  const cancelBtn = document.getElementById("cancelBillBtn");
  const form = document.getElementById("billForm");

  openBtn.addEventListener("click", () => {
    form.reset();
    document.getElementById("formConsultFee").value = "500.00";
    document.getElementById("formMedicineFee").value = "250.00";
    modal.classList.add("active");
  });

  closeBtn.addEventListener("click", () => modal.classList.remove("active"));
  cancelBtn.addEventListener("click", () => modal.classList.remove("active"));

  form.addEventListener("submit", handleGenerateBill);

  // View Modal
  const viewModal = document.getElementById("viewBillModal");
  document.getElementById("closeViewBillModal").addEventListener("click", () => viewModal.classList.remove("active"));
  document.getElementById("closeViewBillBtn").addEventListener("click", () => viewModal.classList.remove("active"));
});

async function loadAppointmentsDropdown() {
  try {
    appointmentsList = await apiFetch("/api/appointments");
    const select = document.getElementById("formBillAppt");
    select.innerHTML = '<option value="">Choose Appointment</option>' +
      appointmentsList.map(a => `<option value="${a.appointment_id}">Appt #${a.appointment_id} — ${escapeHtml(a.patient_name)} with ${escapeHtml(a.doctor_name)} (${a.appointment_date})</option>`).join("");
  } catch (err) {
    console.error("Failed to load appointments for bill generation:", err);
  }
}

async function loadBills(paymentStatus = "") {
  const tableBody = document.getElementById("billsTableBody");
  const countLabel = document.getElementById("billCountLabel");

  try {
    const url = paymentStatus ? `/api/bills?payment_status=${encodeURIComponent(paymentStatus)}` : "/api/bills";
    const bills = await apiFetch(url);

    countLabel.textContent = `Showing ${bills.length} invoice${bills.length === 1 ? '' : 's'}`;

    if (bills.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: var(--text-muted); padding: 24px;">No billing entries found.</td></tr>';
      return;
    }

    tableBody.innerHTML = bills.map(b => {
      const isPaid = b.payment_status === 'PAID';
      const toggleAction = isPaid ? 'PENDING' : 'PAID';
      const toggleBtnLabel = isPaid ? 'Mark Pending' : 'Mark Paid';
      const toggleBtnClass = isPaid ? 'btn-outline' : 'btn-outline';

      return `
        <tr>
          <td><strong>#${b.bill_id}</strong></td>
          <td><strong>${escapeHtml(b.patient_name)}</strong></td>
          <td>${b.appointment_id ? '#' + b.appointment_id : '—'}</td>
          <td>${b.bill_date}</td>
          <td>INR ${parseFloat(b.consultation_fee).toFixed(2)}</td>
          <td>INR ${parseFloat(b.medicine_fee).toFixed(2)}</td>
          <td><strong style="color: var(--primary);">INR ${parseFloat(b.total_amount).toFixed(2)}</strong></td>
          <td><span class="badge badge-${b.payment_status.toLowerCase()}">${b.payment_status}</span></td>
          <td style="text-align: right;">
            <div class="btn-group">
              <button class="btn btn-outline btn-sm" onclick="viewBill(${b.bill_id})">View</button>
              <button class="btn ${toggleBtnClass} btn-sm" onclick="togglePaymentStatus(${b.bill_id}, '${toggleAction}')">${toggleBtnLabel}</button>
            </div>
          </td>
        </tr>
      `;
    }).join("");
  } catch (err) {
    tableBody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: var(--danger-text); padding: 24px;">Failed to load billing ledger.</td></tr>';
  }
}

async function handleGenerateBill(e) {
  e.preventDefault();
  const saveBtn = document.getElementById("saveBillBtn");
  saveBtn.disabled = true;
  saveBtn.textContent = "Calculating & Saving...";

  // Notice: We only send consultation_fee and medicine_fee. The backend performs the calculation.
  const payload = {
    appointment_id: parseInt(document.getElementById("formBillAppt").value),
    consultation_fee: parseFloat(document.getElementById("formConsultFee").value),
    medicine_fee: parseFloat(document.getElementById("formMedicineFee").value)
  };

  try {
    const res = await apiFetch("/api/bills", {
      method: "POST",
      body: JSON.stringify(payload)
    });
    showToast(res.message || `Bill generated. Total: INR ${res.total_amount}`);
    document.getElementById("generateBillModal").classList.remove("active");
    loadBills();
  } catch (err) {
    // Handled in apiFetch
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = "Generate & Save Bill";
  }
}

async function togglePaymentStatus(billId, newStatus) {
  try {
    await apiFetch(`/api/bills/${billId}/status`, {
      method: "PUT",
      body: JSON.stringify({ payment_status: newStatus })
    });
    showToast(`Bill #${billId} updated to ${newStatus}.`);
    loadBills(document.getElementById("billStatusFilter").value);
  } catch (err) {
    // Handled in apiFetch
  }
}

async function viewBill(billId) {
  const modal = document.getElementById("viewBillModal");
  const body = document.getElementById("viewBillBody");

  try {
    const bill = await apiFetch(`/api/bills/${billId}`);
    document.getElementById("viewBillTitle").textContent = `Invoice #${bill.bill_id} — ${bill.patient_name}`;

    body.innerHTML = `
      <div style="font-size: 13px; line-height: 1.6;">
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; margin-bottom: 14px;">
          <div>
            <div style="font-weight: 700; font-size: 15px; color: var(--primary);">Hospital Patient Invoice</div>
            <div style="color: var(--text-muted); font-size: 11px;">Oracle COE Academic Demonstration</div>
          </div>
          <div style="text-align: right;">
            <div>Invoice: <strong>#${bill.bill_id}</strong></div>
            <div>Date: ${bill.bill_date}</div>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; background: var(--bg-surface); padding: 12px; border-radius: var(--radius-sm);">
          <div>
            <span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase;">Billed To</span>
            <div style="font-weight: 600; font-size: 14px;">${escapeHtml(bill.patient_name)} (#${bill.patient_id})</div>
            <div style="color: var(--text-muted);">${escapeHtml(bill.phone)} | ${escapeHtml(bill.email)}</div>
          </div>
          <div style="text-align: right;">
            <span style="color: var(--text-muted); font-size: 11px; text-transform: uppercase;">Payment Status</span>
            <div style="margin-top: 4px;"><span class="badge badge-${bill.payment_status.toLowerCase()}">${bill.payment_status}</span></div>
            <div style="color: var(--text-muted); font-size: 11px; margin-top: 4px;">Appointment: #${bill.appointment_id || 'N/A'}</div>
          </div>
        </div>

        <table class="data-table" style="margin-bottom: 16px;">
          <thead>
            <tr>
              <th>Fee Category</th>
              <th style="text-align: right;">Amount (INR)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Doctor Professional Consultation Fee</td>
              <td style="text-align: right;">INR ${parseFloat(bill.consultation_fee).toFixed(2)}</td>
            </tr>
            <tr>
              <td>Pharmacy & Medicine Charges</td>
              <td style="text-align: right;">INR ${parseFloat(bill.medicine_fee).toFixed(2)}</td>
            </tr>
            <tr style="background: var(--bg-surface); font-weight: 700;">
              <td>Total Amount Due (Database Calculated)</td>
              <td style="text-align: right; color: var(--primary); font-size: 15px;">INR ${parseFloat(bill.total_amount).toFixed(2)}</td>
            </tr>
          </tbody>
        </table>
      </div>
    `;

    modal.classList.add("active");
  } catch (err) {
    showToast("Failed to load invoice details.", true);
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
