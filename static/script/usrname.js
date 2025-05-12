const username = localStorage.getItem("username");
if (username) {
  document.getElementById("user-display").textContent =
    username.charAt(0).toUpperCase() + username.slice(1);
} else {
  // redirect to login if not logged in
  window.location.href = "/login";
}

document.getElementById("logout").addEventListener("click", function () {
  localStorage.clear();
  window.location.href = "/";
});
