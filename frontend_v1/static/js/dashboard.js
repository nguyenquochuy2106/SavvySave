document.addEventListener("DOMContentLoaded", async () => {
    const userName = document.getElementById("user-name");
    const totalSavings = document.getElementById("total-savings");
    const totalSpent = document.getElementById("total-spent");
    const categoryBreakdown = document.getElementById("category-breakdown");
    const logoutButton = document.getElementById("logout");

    // Fetch user data
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/index.html";
        return;
    }

    const headers = { "Authorization": `Bearer ${token}` };

    try {
        // Get user profile
        const userRes = await fetch("/api/users/me", { headers });
        const userData = await userRes.json();
        userName.textContent = userData.name;

        // Get transaction stats
        const statsRes = await fetch("/api/transactions/stats", { headers });
        const statsData = await statsRes.json();
        totalSavings.textContent = `$${statsData.total_savings.toFixed(2)}`;
        totalSpent.textContent = `$${statsData.total_spent.toFixed(2)}`;

        // Render category breakdown
        categoryBreakdown.innerHTML = "";
        statsData.categories.forEach(category => {
            const li = document.createElement("li");
            li.textContent = `${category.name}: $${category.amount.toFixed(2)}`;
            categoryBreakdown.appendChild(li);
        });
    } catch (error) {
        console.error("Error loading dashboard:", error);
    }

    // Logout handler
    logoutButton.addEventListener("click", () => {
        localStorage.removeItem("token");
        window.location.href = "/index.html";
    });
});