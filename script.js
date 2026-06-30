const API_URL = "http://127.0.0.1:8000";

// Get token from browser
const token = localStorage.getItem("token");

// If no token → send back to login
if (!token) {
    window.location.href = "login.html";
}

// ---------------------------
// LOAD TASKS ON PAGE LOAD
// ---------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
});


// ---------------------------
// ADD TASK
// ---------------------------
async function addTask() {
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    if (!title || !description) {
        alert("Please enter both title and description");
        return;
    }

    const res = await fetch(`${API_URL}/tasks/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            title: title,
            description: description
        })
    });

    if (res.ok) {
        document.getElementById("title").value = "";
        document.getElementById("description").value = "";
        loadTasks();
    } else {
        alert("Failed to add task");
    }
}


// ---------------------------
// LOAD TASKS
// ---------------------------
async function loadTasks() {
    const res = await fetch(`${API_URL}/tasks/`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!res.ok) {
        alert("Failed to load tasks");
        return;
    }

    const tasks = await res.json();

    const taskList = document.getElementById("taskList");
    taskList.innerHTML = "";

    tasks.forEach(task => {
        const div = document.createElement("div");
        div.className = "task";

        div.innerHTML = `
            <h3>${task.title}</h3>
            <p>${task.description}</p>
            <p>Status: ${task.completed ? "Completed" : "Pending"}</p>

            <button onclick="deleteTask(${task.id})">Delete</button>
            <button onclick="editTask(${task.id}, '${task.title}', '${task.description}', ${task.completed})">Edit</button>
        `;

        taskList.appendChild(div);
    });
}


// ---------------------------
// DELETE TASK
// ---------------------------
async function deleteTask(id) {
    const confirmDelete = confirm("Are you sure you want to delete this task?");
    if (!confirmDelete) return;

    const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (res.ok) {
        loadTasks();
    } else {
        alert("Failed to delete task");
    }
}


// ---------------------------
// EDIT TASK
// ---------------------------
async function editTask(id, oldTitle, oldDesc, oldCompleted) {

    const newTitle = prompt("Edit Title:", oldTitle);
    if (newTitle === null) return;

    const newDesc = prompt("Edit Description:", oldDesc);
    if (newDesc === null) return;

    const completed = confirm("Mark as completed? OK = Yes");

    const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            title: newTitle || oldTitle,
            description: newDesc || oldDesc,
            completed: completed
        })
    });

    if (res.ok) {
        loadTasks();
    } else {
        alert("Update failed");
    }
}