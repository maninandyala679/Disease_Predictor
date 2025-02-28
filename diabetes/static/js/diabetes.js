document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("diabetes-form");
    const inputs = document.querySelectorAll("input[type='number']");
    const resultSection = document.getElementById("result-section");
    const predictionResult = document.getElementById("prediction-result");
    const emojiIndicator = document.getElementById("emoji-indicator");
    const aiMessage = document.getElementById("ai-message");
    const darkModeToggle = document.getElementById("dark-mode-toggle");

    // Move to next input field on pressing Enter
    inputs.forEach((input, index) => {
        input.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                const nextInput = inputs[index + 1];
                if (nextInput) {
                    nextInput.focus();
                } else {
                    form.querySelector("button").focus();
                }
            }
        });
    });

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        // Collect user input
        const formData = new FormData(form);
        const inputData = {};
        formData.forEach((value, key) => {
            inputData[key] = value;
        });

        // Send data to Flask backend
        fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(inputData)
        })
        .then(response => response.json())
        .then(data => {
            const prediction = data.result; // "Yes" or "No"
            predictionResult.textContent = `Diabetes Prediction: ${prediction}`;
            emojiIndicator.textContent = prediction === "No" ? "😊 Low Risk" : "😟 High Risk";
            aiMessage.textContent = prediction === "No" ? "Great! Maintain a balanced diet and exercise!" : "Consult a doctor for further guidance.";
            resultSection.style.display = "block";
        })
        .catch(error => console.error("Prediction error:", error));
    });

    // Dark mode toggle
    darkModeToggle.addEventListener("change", function() {
        document.body.classList.toggle("dark-mode");
    });
});
