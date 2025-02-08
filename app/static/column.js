// document.addEventListener("DOMContentLoaded", function () {
//     document.querySelector("form").addEventListener("submit", function (event) {
//         event.preventDefault(); // Prevent form from refreshing the page

//         let formData = new FormData(event.target);
//         let jsonData = {};

//         formData.forEach((value, key) => {
//             let colName = key.split("_")[0];  // Extract column name before "_floor", "_ceil", etc.

//             // If it's numeric (floor & ceil), store as array [floor, ceil]
//             if (key.endsWith("_floor") || key.endsWith("_ceil")) {
//                 if (!jsonData[colName]) jsonData[colName] = [];
//                 jsonData[colName].push(value);
//             }
//             else if (key.endsWith("_category")) {
//                 if (!jsonData[colName]) jsonData[colName] = [];
//                 jsonData[colName].push(value);
//             }

//             // If it's datetime (start & end date), store as [start_date, end_date]
//             else if (key.endsWith("_start") || key.endsWith("_end")) {
//                 if (!jsonData[colName]) jsonData[colName] = [];
//                 jsonData[colName].push(value);
//             }
//             jsonData[colName].push(value);  // Store as array: [floor, ceil]
//         });

//         console.log("Submitting Data: ", jsonData);

//         let jsonString = JSON.stringify(jsonData, null, 2);
//         let blob = new Blob([jsonString], { type: "application/json" });
//         let link = document.createElement("a");

//         link.href = URL.createObjectURL(blob);
//         link.download = "submitted_data.json";  // Name of the file
//         document.body.appendChild(link);
//         link.click();
//         document.body.removeChild(link);
//     });

//     document.getElementById("continue").addEventListener("click", function () {
//         window.location.href = "/next";
//     });
// });

// Frontend JavaScript
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("form").addEventListener("submit", async function (event) {
        event.preventDefault();

        let formData = new FormData(event.target);
        let jsonData = {};

        formData.forEach((value, key) => {
            let colName = key.split("_")[0];

            if (key.endsWith("_floor") || key.endsWith("_ceil")) {
                if (!jsonData[colName]) jsonData[colName] = [];
                jsonData[colName].push(value);
            }
            else if (key.endsWith("_category")) {
                if (!jsonData[colName]) jsonData[colName] = [];
                jsonData[colName].push(value);
            }
            else if (key.endsWith("_start") || key.endsWith("_end")) {
                if (!jsonData[colName]) jsonData[colName] = [];
                jsonData[colName].push(value);
            }
        });

        console.log("Submitting Data: ", jsonData);

        try {
            const response = await fetch('/save-file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(jsonData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log('File saved successfully:', result);
        } catch (error) {
            console.error('Error saving file:', error);
        }
    });

    document.getElementById("continue").addEventListener("click", function () {
        window.location.href = "/next";
    });
});