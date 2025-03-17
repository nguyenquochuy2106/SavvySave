document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form submission

        // Get user input (for now, just checking if filled)
        const username = document.getElementById("username").value;

        if (username.trim() === "") {
            alert("Please enter a valid username!");
            return;
        }

        // Simulate authentication (later replace with API call)
        localStorage.setItem("loggedInUser", username);

        // Redirect to dashboard
        window.location.href = "dashboard.html";
    });
});
