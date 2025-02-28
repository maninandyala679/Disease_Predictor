document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("parkinsons-form");
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

        // Collect user input and ensure decimal values are handled correctly
        const formData = new FormData(form);
        const inputData = {};

        formData.forEach((value, key) => {
            inputData[key] = parseFloat(value); // Convert input to a floating-point number
        });

        // Send data to Flask backend
        fetch("/predict_parkinsons", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(inputData)
        })
        .then(response => response.json())
        .then(data => {
            const prediction = data.result; // "Yes" or "No"
            predictionResult.textContent = `Parkinson's Prediction: ${prediction}`;

            // Set emoji and AI response
            if (prediction === "No") {
                emojiIndicator.textContent = "😊 Low Risk";
                aiMessage.textContent = "Great! Keep maintaining a healthy lifestyle!";
            } else {
                emojiIndicator.textContent = "😟 High Risk";
                aiMessage.textContent = "Consult a neurologist for further evaluation.";
            }

            resultSection.style.display = "block";
        })
        .catch(error => console.error("Prediction error:", error));
    });

    // Dark mode toggle
    darkModeToggle.addEventListener("change", function() {
        document.body.classList.toggle("dark-mode");
    });
});
