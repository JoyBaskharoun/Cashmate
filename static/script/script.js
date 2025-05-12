// toggle drop down
const arrow = document.getElementById("drop-down-arrow");
const menu = document.getElementById("drop-down-menu");

arrow.addEventListener("click", function () {
  menu.classList.toggle("show");
});
