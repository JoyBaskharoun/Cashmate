let rows = document.querySelectorAll("tr.collapsible");

rows.forEach(function (row) {
  row.addEventListener("click", function () {
    var id = row.id;
    var contentRow = document.getElementById(id.replace("row", "content-row"));
    if (contentRow.style.display === "none") {
      contentRow.style.display = "table-row";
    } else {
      contentRow.style.display = "none";
    }
  });
});
