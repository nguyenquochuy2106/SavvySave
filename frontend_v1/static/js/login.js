async function loginWithFaceID() {
    let fileInput = document.getElementById("faceImage").files[0];
    let formData = new FormData();
    formData.append("file", fileInput);

    let response = await fetch("/auth/faceid-login", {
        method: "POST",
        body: formData
    });

    let data = await response.json();
    if (response.ok) {
        localStorage.setItem("token", data.token);
        window.location.href = "dashboard.html";
    } else {
        alert("FaceID not recognized!");
    }
}
