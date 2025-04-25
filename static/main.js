function toggleInputs() {
    const method = document.getElementById("method").value;
    document.getElementById("content-fields").style.display = (method === "content" || method === "hybrid" || method === "collaborative") ? "block" : "none";
}

window.onload = function () {
    toggleInputs();
};

document.addEventListener("DOMContentLoaded", function () {
    const formCard = document.getElementById("form-card");
    formCard.classList.remove("opacity-0", "translate-y-4");
    formCard.classList.add("opacity-100", "translate-y-0");
});

// Validate form on submit
function validateLoginForm(event) {
    const userId = document.getElementById("user_id").value;
    const password = document.getElementById("password").value;

    if (!userId || !password) {
        alert("Please fill in both fields.");
        event.preventDefault();
        return false;
    }
    return true;
}

// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById("password");
    const toggleIcon = document.getElementById("toggleIcon");
    const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
    passwordInput.setAttribute("type", type);
    toggleIcon.textContent = type === "password" ? "👁️" : "🙈";
}