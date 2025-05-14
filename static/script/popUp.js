document.addEventListener("DOMContentLoaded", function () {
  const logoutBtn = document.getElementById("logout");
  const modal = document.getElementById("logout-modal");
  const confirmBtn = document.getElementById("confirm-logout");
  const cancelBtn = document.getElementById("cancel-logout");

  logoutBtn.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent immediate navigation or default action
    event.stopPropagation();
    modal.style.display = "flex"; // Show modal
  });

  confirmBtn.addEventListener("click", function () {
    window.location.href = "/logout"; // Proceed to logout
  });

  cancelBtn.addEventListener("click", function () {
    modal.style.display = "none"; // Hide modal
  });

  // Optional: close modal when clicking outside content
  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
});
