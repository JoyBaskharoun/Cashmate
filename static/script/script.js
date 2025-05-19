function loadNavbar() {
  return fetch('/static/navbar.html')
    .then(res => {
      if (!res.ok) throw new Error('Failed to load navbar');
      return res.text();
    })
    .then(html => {
      document.getElementById('navbar-placeholder').innerHTML = html;
    });
}

function loadModal() {
  return fetch('/static/logout-modal.html')
    .then(res => {
      if (!res.ok) throw new Error('Failed to load modal');
      return res.text();
    })
    .then(html => {
      document.getElementById('modal-placeholder').innerHTML = html;
    });
}

function initNavbar() {
  const logoutBtn = document.getElementById("logout");
  const modal = document.getElementById("logout-modal");
  const confirmBtn = document.getElementById("confirm-logout");
  const cancelBtn = document.getElementById("cancel-logout");

  if (logoutBtn && modal && confirmBtn && cancelBtn) {
    logoutBtn.addEventListener("click", (event) => {
      event.preventDefault();
      modal.style.display = "flex";
    });

    confirmBtn.addEventListener("click", () => {
      localStorage.clear();
      window.location.href = "/logout";
    });

    cancelBtn.addEventListener("click", () => {
      modal.style.display = "none";
    });

    window.addEventListener("click", (event) => {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    });
  }
}

function toggleTheme() {
  document.documentElement.classList.toggle('dark-theme');
}

document.addEventListener('DOMContentLoaded', () => {
  Promise.all([loadNavbar(), loadModal()])
    .then(() => {
      initNavbar();
    })
    .catch(err => console.error(err));
});




