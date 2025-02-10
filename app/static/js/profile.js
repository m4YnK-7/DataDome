document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("uploadForm");
    const generateButton = document.getElementById("generate");
    const continueButton = document.getElementById("continue");
    const loadingScreen = document.getElementById("loadingScreen");
    const buttons = document.getElementById("buts");

    // Show loading screen when "Generate Report" is clicked
    generateButton.addEventListener("click", function () {
        buttons.classList.add("hidden");  // Hide buttons
        loadingScreen.classList.remove("hidden");  // Show loading screen
    });

    // Redirect to columns page when "Continue" is clicked
    continueButton.addEventListener("click", function () {
        window.location.href = "/attribute_cleaning";
    });
});
