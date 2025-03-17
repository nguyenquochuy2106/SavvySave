const video = document.getElementById("video");
const captureButton = document.getElementById("capture");
const message = document.getElementById("message");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");

// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error("Error accessing webcam:", error);
        message.textContent = "Camera access is required for registration.";
    });

// Capture and send face data for registration
captureButton.addEventListener("click", async () => {
    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    
    if (!name || !email) {
        message.textContent = "Please enter your name and email.";
        return;
    }
    
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const imageData = canvas.toDataURL("image/jpeg");
    
    const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, image: imageData })
    });
    
    const result = await response.json();
    if (response.ok) {
        message.textContent = "Registration successful! Redirecting...";
        setTimeout(() => window.location.href = "/index.html", 1500);
    } else {
        message.textContent = "Registration failed: " + result.detail;
    }
});
