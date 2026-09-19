/**
 * Login Page Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  // If already logged in, redirect to dashboard
  if (getUser()) {
    window.location.href = "/dashboard";
    return;
  }

  const loginForm = document.getElementById("loginForm");
  const loginBtn = document.getElementById("loginBtn");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
      showToast("Please enter both email and password.", true);
      return;
    }

    loginBtn.disabled = true;
    loginBtn.textContent = "Authenticating...";

    try {
      const response = await apiFetch("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      if (response && response.user) {
        localStorage.setItem("hprs_user", JSON.stringify(response.user));
        showToast("Login successful! Redirecting...");
        setTimeout(() => {
          window.location.href = "/dashboard";
        }, 500);
      }
    } catch (err) {
      // Error toast is handled in apiFetch
      loginBtn.disabled = false;
      loginBtn.textContent = "Sign In";
    }
  });
});
