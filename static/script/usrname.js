document.addEventListener("DOMContentLoaded", function () {
  const logoutBtn = document.getElementById("logout");
  const modal = document.getElementById("logout-modal");
  const confirmBtn = document.getElementById("confirm-logout");
  const cancelBtn = document.getElementById("cancel-logout");

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

  // Close modal if clicking outside modal content
  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });

  // Set username display (your existing code)
  const username = localStorage.getItem("username");
  if (username) {
    document.getElementById("user-display").textContent =
      username.charAt(0).toUpperCase() + username.slice(1);
  }
});