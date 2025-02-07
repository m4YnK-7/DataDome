document.addEventListener("DOMContentLoaded", function () {
    const continueButton = document.getElementById("continue");

    continueButton.addEventListener("click", function () {
        window.location.href = "/next";
    });
});