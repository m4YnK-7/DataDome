document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileInput");
    const fileName = document.getElementById("fileName");
    const addButton = document.getElementById("addButton");
    const browseButton = document.getElementById("browseButton");
    const continueButton = document.getElementById("continue");
    const generateButton = document.getElementById("generate");
    const urlInputContainer = document.getElementById("urlInputContainer");
    const datasetUrl = document.getElementById("datasetUrl");
    const fetchDataset = document.getElementById("fetchDataset");
    const datasetInfo = document.getElementById("datasetInfo");
    const uploadForm = document.getElementById("uploadForm");
    const loadingScreen = document.getElementById("loadingScreen");
    const buttons = document.getElementById("buts");
    const text = document.getElementById("flexy");

    // Handle file input change
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            fileName.textContent = `Selected file: ${fileInput.files[0].name}`;
        } else {
            fileName.textContent = "No file selected";
        }
    });
    
    // Show input field when "Add Dataset" is clicked & Hide "Add" button
    addButton.addEventListener("click", function () {
        urlInputContainer.classList.remove("hidden");
        browseButton.classList.add("hidden");
        addButton.style.display = "none"; // Hide "Add" button
    });


    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            continueButton.classList.remove("hidden"); // Show the button when a file is selected
            generateButton.classList.remove("hidden"); // Show the button when a file is selected
            addButton.classList.add("hidden"); // Hide the "Add" button
            browseButton.classList.add("hidden"); // Hide the "Browse" button
        } else {
            continueButton.classList.add("hidden"); // Hide if no file is selected
            generateButton.classList.add("hidden"); // Hide if no file is selected
        }
    });


    // Fetch dataset from URL
    document.getElementById("fetchDataset").addEventListener("click", function () {
        const url = document.getElementById("datasetUrl").value.trim();
        const datasetInfo = document.getElementById("datasetInfo");
    
        if (!url) {
            alert("Please enter a valid dataset URL.");
            return;
        }
    
        datasetInfo.textContent = `Retrieving dataset from: ${url}`;
        console.log("Sending request to backend to fetch dataset...");
    
        fetch("/fetch-dataset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                datasetInfo.textContent = `Dataset saved as: ${data.filename}`;
                continueButton.classList.remove("hidden"); // Show the button when a file is selected
                console.log("Dataset saved successfully.");
            } else {
                datasetInfo.textContent = "Failed to retrieve dataset.";
                console.error("Error:", data.error);
            }
        })
        .catch(error => {
            datasetInfo.textContent = "Failed to connect to backend.";
            console.error("Fetch error:", error);
        });
    });

    // Continue Button
    continueButton.addEventListener("click", function () {
        window.location.href = "/attribute_cleaning";
    });

    // Browse Button
    fileInput.addEventListener("change", function() {
        if (this.files.length > 0) {
            document.getElementById("uploadForm").submit();
        }
    });

    // Show loading screen when form is submitted
    uploadForm.addEventListener("submit", function (event) {
        if (!fileInput.files.length) {
            alert("Please select a file before uploading.");
            event.preventDefault(); // Prevent form submission if no file is chosen
            return;
        }
        
        buttons.classList.add("hidden"); // Hide buttons
        text.classList.add("hidden"); // Hide text
        loadingScreen.classList.remove("hidden"); // Show loading screen

    });
});

    

