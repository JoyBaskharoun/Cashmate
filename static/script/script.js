// to insert partial html without reload
async function loadHTML(url, elementId) {
  const response = await fetch(url);
  const html = await response.text();
  document.getElementById(elementId).innerHTML = html;
}

// load navbar & modal 
async function loadComponents() {
  await loadHTML("/static/navbar.html", "navbar-placeholder");
  await loadHTML("/static/logout-modal.html", "modal-placeholder");
}

// Initialize navbar
function initNavbar() {
  const logoutBtn = document.getElementById("logout");
  const modal = document.getElementById("logout-modal");
  const confirmBtn = document.getElementById("confirm-logout");
  const cancelBtn = document.getElementById("cancel-logout");

  if (!logoutBtn || !modal || !confirmBtn || !cancelBtn) return;

  logoutBtn.addEventListener("click", function (event) {
    event.preventDefault();
    modal.style.display = "flex";
  });

  confirmBtn.addEventListener("click", function () {
    localStorage.clear();
    window.location.href = "/logout";
  });

  cancelBtn.addEventListener("click", function () {
    modal.style.display = "none";
  });

  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
}

function toggleTheme() {
  const root = document.documentElement;
  root.classList.toggle("dark-theme");

  // save theme localStorage
  if (root.classList.contains("dark-theme")) {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
}

// check for theme, apply on html
document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.documentElement.classList.add("dark-theme");
  } else {
    document.documentElement.classList.remove("dark-theme");
  }
});


document.addEventListener("DOMContentLoaded", async function () {
    await loadComponents();
    initNavbar();
});
