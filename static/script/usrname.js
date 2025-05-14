const username = localStorage.getItem("username");
if (username) {
  document.getElementById("user-display").textContent =
    username.charAt(0).toUpperCase() + username.slice(1);
} else {
  if (!username) {
    // Only redirect if not on login page already
    if (!window.location.pathname.endsWith("/login")) {
      window.location.href = "/login";
    }
  }
}

document.getElementById("logout").addEventListener("click", function () {
  localStorage.clear();
  window.location.href = "/";
});
