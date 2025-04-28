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
<<<<<<< HEAD
}

function validatePassword() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm_password").value;
    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }
    return true;
}

// Animate form appearance
document.addEventListener("DOMContentLoaded", function () {
    const formContainer = document.getElementById("form-container");
    formContainer.classList.remove("opacity-0", "translate-y-4");
    formContainer.classList.add("opacity-100", "translate-y-0");
});

// Validate before submitting
function validateResetForm(event) {
    const user_id = document.getElementById("user_id").value.trim();
    const answer = document.getElementById("security_answer").value.trim();
    
    if (!user_id || !answer) {
        alert("Please fill in both fields correctly.");
        event.preventDefault();
        return false;
    }
    return true;
}

// Animate form appearance
document.addEventListener("DOMContentLoaded", function () {
    const formContainer = document.getElementById("form-container");
    formContainer.classList.remove("opacity-0", "translate-y-4");
    formContainer.classList.add("opacity-100", "translate-y-0");
});

// Validate password match before submitting
function validateNewPassword(event) {
    const password = document.getElementById("new_password").value.trim();
    const confirmPassword = document.getElementById("confirm_password").value.trim();

    if (password !== confirmPassword) {
        alert("Passwords do not match! Please re-enter.");
        event.preventDefault();
        return false;
    }
    return true;
=======
>>>>>>> c3b9562fa8eaf72805e0954486ad23eee93fe450
}