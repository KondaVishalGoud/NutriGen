document.addEventListener("DOMContentLoaded", function () {
    const generateBtn = document.getElementById("generate-btn");

    if (!generateBtn) {
        console.error("❌ Button with ID 'generate-btn' not found!");
        return;
    }

    generateBtn.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent form submission

        console.log("✅ Button Clicked");

        let userData = {
            age: document.getElementById("age")?.value || "",
            gender: document.getElementById("gender")?.value || "",
            weight: document.getElementById("weight")?.value || "",
            height: document.getElementById("height")?.value || "",
            activity: document.getElementById("activity")?.value || "",
            diet_restrictions: [...document.querySelectorAll('input[name="diet_restrictions"]:checked')].map(e => e.value),
            custom_diet: document.getElementById("customDiet")?.value || "",
            allergies: document.getElementById("allergies")?.value || "",
            health: document.getElementById("health")?.value || "",
            goal: document.getElementById("goal")?.value || "",
            cuisine: document.getElementById("cuisine")?.value || "",
            meals: document.getElementById("meals")?.value || "",
            include_foods: document.getElementById("include_foods")?.value || "",
            avoid_foods: document.getElementById("avoid_foods")?.value || ""
        };

        fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userData),
        })
        .then(response => response.json())
        .then(data => {
            console.log("📩 Response from backend:", data);

            const outputElement = document.getElementById("mealPlanContent");
            if (!outputElement) {
                console.error("❌ Output element not found!");
                return;
            }

            if (data.meal_plan) {
                outputElement.innerHTML = `<pre style="white-space: pre-wrap; font-size: 16px; color: #333;">${data.meal_plan}</pre>`;
            } else {
                outputElement.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            }
        })
        .catch(error => {
            console.error("❌ Fetch error:", error);
            document.getElementById("mealPlanContent").innerHTML = `<p style="color: red;">An error occurred while generating the meal plan.</p>`;
        });
    });
});
