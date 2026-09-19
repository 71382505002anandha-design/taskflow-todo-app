function editTask(id, title, priority, dueDate) {
    const modal = document.getElementById("editModal");
    const form = document.getElementById("editForm");

    document.getElementById("editTitle").value = title;
    document.getElementById("editPriority").value = priority;
    document.getElementById("editDueDate").value = dueDate;

    form.action = "/edit/" + id;

    modal.style.display = "flex";
}

function closeModal() {
    document.getElementById("editModal").style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById("editModal");

    if (event.target === modal) {
        closeModal();
    }
};
