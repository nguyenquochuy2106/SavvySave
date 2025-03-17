const video = document.getElementById("video");
const captureButton = document.getElementById("capture");
const message = document.getElementById("message");

// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error("Error accessing webcam:", error);
        message.textContent = "Camera access is required for FaceID login.";
    });

// Capture and send face data
captureButton.addEventListener("click", async () => {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const imageData = canvas.toDataURL("image/jpeg");
    
    const response = await fetch("/api/auth/faceid-login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData })
    });
    
    const result = await response.json();
    if (response.ok) {
        message.textContent = "Login successful! Redirecting...";
        localStorage.setItem("token", result.token);
        setTimeout(() => window.location.href = "/dashboard.html", 1500);
    } else {
        message.textContent = "Login failed: " + result.detail;
    }
});