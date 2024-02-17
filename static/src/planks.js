/*

const fs = require('fs');

document.addEventListener("DOMContentLoaded", function() {
    // Add event listener for form submission
    document.getElementById("practiceTrackerForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission behavior
        console.log("Form submitted");

        // Send form data to data.json
        fs.writeFile('data.json', data, (err) => {
            if (err) {
                throw err;
            }
            console.log("JSON data is saved");
        });

        // Reset form after submission 
        form.reset();
        // document.getElementById("practiceTrackerForm").reset();
    });

    // Add event listener for form reset
    document.getElementById("practiceTrackerForm").addEventListener("reset", function(event) {
        // Handle form reset here (e.g., clear input fields)
        console.log("Form reset");
    });
});

/*
document.getElementById("myForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission behavior

    // Get the value of the checkbox
    const checkboxValue = document.getElementById("myCheckbox").checked;

    // Display the value
    alert("Checkbox value: " + checkboxValue);
});
*/