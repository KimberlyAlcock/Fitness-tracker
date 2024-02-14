function openTab(tabName) {
    let i, tabs;
    tabs = document.getElementsByClassName("tab");
    for (i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove("active");
    }
    document.getElementById(tabName).classList.add("active");
}


// This JavaScript is for the buttons on the form submission for practice-tracker.html
document.addEventListener("DOMContentLoaded", function() {
    // Get the form element
    let form = document.getElementById("practiceTrackerForm");

    // Add event listener for form submission
    form.addEventListener("submit", function(event) {
        // Prevent the default form submission
        event.preventDefault();

        // Get the form data
        let formData = new FormData(form);

        // Process the form data (you can send it to the server, perform validation, etc.)
        // For demonstration purposes, let's log the form data to the console
        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }

        // Optionally, you can perform additional actions after form submission

        // Reset the form
        form.reset();
    });

    // Add event listener for reset button click
    let resetButton = document.querySelector('input[type="reset"]');
    resetButton.addEventListener("click", function() {
        // Optionally, you can prompt the user for confirmation before resetting the form
        let confirmation = confirm("Are you sure you want to reset the form?");
        if (confirmation) {
            form.reset();
        }});
});

// Function to fetch data from backend 
async function fetchData() {
    try {
        const response = await fetch('/get_data');
        const data = await response.json();
        // Handle retrieved data here (e.g., display it in the HTML)
        document.getElementById('data-container').innerText = JSON.stringify(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Call fetchData when the page loads
window.onload = fetchData;
