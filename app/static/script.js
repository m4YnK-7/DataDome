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
    // Fetch dataset when "Retrieve" button is clicked
    // fetchDataset.addEventListener("click", function () {
    //     const url = datasetUrl.value.trim();
    //     if (url) {
    //         datasetInfo.textContent = `Retrieving dataset from: ${url}`;
    //         console.log("Fetching dataset from:", url);

    //         fetch(url)
    //             .then(response => {
    //                 if (!response.ok) {
    //                     throw new Error("Network response was not ok");
    //                 }
    //                 return response.blob(); // Convert response to a file blob
    //             })
    //             .then(blob => {
    //                 datasetInfo.textContent = "Dataset retrieved successfully!";
    //                 console.log("Dataset blob:", blob);
    //                 // You can now process the dataset (e.g., download, preview, etc.)
    //             })
    //             .catch(error => {
    //                 datasetInfo.textContent = "Failed to retrieve dataset.";
    //                 console.error("Error fetching dataset:", error);
    //             });
    //     } else {
    //         alert("Please enter a valid dataset URL.");
    //     }
    // });
    // __________________________________________________________________-
    document.getElementById("fetchDataset").addEventListener("click", function () {
        const url = document.getElementById("datasetUrl").value.trim();
        const datasetInfo = document.getElementById("datasetInfo");
    
        if (!url) {
            alert("Please enter a valid dataset URL.");
            return;
        }
    
        datasetInfo.textContent = `Retrieving dataset from: ${url}`;
        console.log("Fetching dataset from:", url);
    
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok. Status: ${response.status}`);
                }
                return response.blob(); // Convert response to blob
            })
            .then(blob => {
                const filename = "user_data.csv";
                if (!filename) {
                    datasetInfo.textContent = "Download canceled.";
                    return;
                }
    
                const a = document.createElement("a");
                const objectURL = URL.createObjectURL(blob);
                a.href = objectURL;
                a.download = filename; // Set desired filename
                document.body.appendChild(a);
                a.click(); 
                document.body.removeChild(a);
                URL.revokeObjectURL(objectURL); // Clean up memory
    
                datasetInfo.textContent = `Dataset downloaded as: ${filename}`;
                console.log("Dataset downloaded successfully.");
            })
            .catch(error => {
                datasetInfo.textContent = "Failed to retrieve dataset.";
                console.error("Error fetching dataset:", error);
            });
    });
    
    // __________________________________________________________________-


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

    generateButton.addEventListener("click", function () {
        window.location.href = "/columns";
    });

