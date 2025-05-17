function initNavbar() {
  const arrow = document.getElementById("drop-down-arrow");
  const menu = document.getElementById("drop-down-menu");

  if (arrow && menu) {
    arrow.addEventListener("click", function () {
      menu.classList.toggle("show");
    });
  }

  const logoutBtn = document.getElementById("logout");
  const modal = document.getElementById("logout-modal");
  const confirmBtn = document.getElementById("confirm-logout");
  const cancelBtn = document.getElementById("cancel-logout");

  if (logoutBtn && modal && confirmBtn && cancelBtn) {
    logoutBtn.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
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
}


function loadNavbar() {
  fetch('/static/navbar.html') 
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.text();
    })
    .then(data => {
      document.getElementById('navbar-placeholder').innerHTML = data;
      initNavbar(); 
    })
    .catch(error => {
      console.error('Error loading navbar:', error);
    });
}

document.addEventListener('DOMContentLoaded', loadNavbar);

function toggleTheme() {
  document.documentElement.classList.toggle('dark-theme');
}