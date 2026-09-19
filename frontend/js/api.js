/**
 * Shared API Client & Session Utilities
 * Hospital Patient Record System (Oracle COE)
 */

const API_BASE = "";

function getUser() {
  const userStr = localStorage.getItem("hprs_user");
  if (!userStr) return null;
  try {
    return JSON.parse(userStr);
  } catch (e) {
    return null;
  }
}

function checkAuth() {
  const user = getUser();
  if (!user) {
    window.location.href = "/";
    return null;
  }
  
  // Render user info in sidebar if elements exist
  const nameEl = document.getElementById("currentUserName");
  const roleEl = document.getElementById("currentUserRole");
  if (nameEl) nameEl.textContent = user.name;
  if (roleEl) roleEl.textContent = user.role;

  return user;
}

function logout() {
  localStorage.removeItem("hprs_user");
  window.location.href = "/";
}

function showToast(message, isError = false) {
  let toast = document.getElementById("globalToast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "globalToast";
    toast.className = "alert-box";
    document.body.appendChild(toast);
  }

  toast.textContent = message;
  toast.className = `alert-box ${isError ? "alert-error" : "alert-success"}`;
  toast.style.display = "block";

  setTimeout(() => {
    toast.style.display = "none";
  }, 4000);
}

async function apiFetch(endpoint, options = {}) {
  try {
    const config = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(`${API_BASE}${endpoint}`, config);
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      const errorMsg = data.detail || data.message || "An unexpected error occurred while processing the request.";
      showToast(errorMsg, true);
      throw new Error(errorMsg);
    }

    return data;
  } catch (err) {
    console.error(`API Error [${endpoint}]:`, err);
    throw err;
  }
}

function setupMobileNav() {
  const toggleBtn = document.getElementById("mobileToggle");
  const sidebar = document.getElementById("appSidebar");
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("open");
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  setupMobileNav();
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      logout();
    });
  }
});
