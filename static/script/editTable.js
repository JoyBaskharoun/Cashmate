document.querySelectorAll(".edit-btn").forEach((editBtn) => {
  editBtn.addEventListener("click", () => {
    const row = editBtn.closest("tr");
    const id = row.dataset.id;

    const amountCell = row.querySelector(".amount-cell");
    const dateCell = row.querySelector(".date-cell");
    const noteCell = row.querySelector(".note-cell");

    const originalAmount = amountCell.textContent.replace("$", "");
    const originalDate = dateCell.textContent;
    const originalNote = noteCell.textContent;

    // Replace with inputs
    amountCell.innerHTML = `<input type="number" step="0.01" value="${originalAmount}" />`;
    dateCell.innerHTML = `<input type="datetime-local" value="${formatDateForInput(originalDate)}" />`;
    noteCell.innerHTML = `<input type="text" value="${originalNote === "-" ? "" : originalNote}" />`;

    // Replace icons
    const icons = row.querySelector(".icons-container");
    icons.innerHTML = `
      <img src="/static/images/icons/check.svg" class="action-icon confirm-edit" title="Confirm">
      <img src="/static/images/icons/cancel.svg" class="action-icon cancel-edit" title="Cancel">
    `;

    icons.querySelector(".confirm-edit").addEventListener("click", () => {
      const updatedAmount = row.querySelector("input[type=number]").value;
      const updatedDate = row.querySelector("input[type=datetime-local]").value;
      const updatedNote = row.querySelector("input[type=text]").value;

      fetch("/update-transaction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id: id,
          amount: updatedAmount,
          timestamp: updatedDate,
          note: updatedNote,
        }),
      }).then((res) => {
        if (res.ok) location.reload();
        else alert("Failed to update");
      });
    });

    icons.querySelector(".cancel-edit").addEventListener("click", () => {
      location.reload();
    });
  });
});

function formatDateForInput(formatted) {
  // Assumes formatted like "YYYY-MM-DD HH:mm"
  const [date, time] = formatted.split(" ");
  return `${date}T${time}`;
}


// delete
document.querySelectorAll(".delete-btn").forEach((delBtn) => {
  delBtn.addEventListener("click", (event) => {
    event.preventDefault();

    const row = delBtn.closest("tr");
    const id = row.dataset.id;

    const modal = document.getElementById("confirm-modal");
    const message = document.getElementById("confirm-modal-message");
    const yesBtn = document.getElementById("confirm-modal-yes");
    const noBtn = document.getElementById("confirm-modal-no");

    message.textContent = "Are you sure you want to delete this transaction?";
    modal.style.display = "flex";

    // Remove previous listeners by cloning buttons
    yesBtn.replaceWith(yesBtn.cloneNode(true));
    noBtn.replaceWith(noBtn.cloneNode(true));

    const newYesBtn = document.getElementById("confirm-modal-yes");
    const newNoBtn = document.getElementById("confirm-modal-no");

    newYesBtn.addEventListener("click", () => {
      fetch("/delete-transaction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id }),
      }).then((res) => {
        if (res.ok) location.reload();
        else alert("Failed to delete");
      });
      modal.style.display = "none";
    });

    newNoBtn.addEventListener("click", () => {
      modal.style.display = "none";
    });

    // One-time outside click listener
    function outsideClickListener(e) {
      if (e.target === modal) {
        modal.style.display = "none";
        window.removeEventListener("click", outsideClickListener);
      }
    }
    window.addEventListener("click", outsideClickListener);
  });
});
