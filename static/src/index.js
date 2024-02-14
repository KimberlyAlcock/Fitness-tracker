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

// Function to fetch data from backend and render it on the webpage
async function fetchDataAndRender() {
    try {
        const response = await fetch('/get_data');
        const data = await response.json();
        const table = document.getElementById('data-table');
        table.innerHTML = ''; // Clear existing data
        // Create table header
        const headerRow = document.createElement('tr');
        for (const key of Object.keys(data[0])) {
            const th = document.createElement('th');
            th.textContent = key;
            headerRow.appendChild(th);
        }
        table.appendChild(headerRow);
        // Create table rows
        for (const row of data) {
            const tr = document.createElement('tr');
            for (const key of Object.keys(row)) {
                const td = document.createElement('td');
                td.textContent = row[key];
                tr.appendChild(td);
            }
            table.appendChild(tr);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Call fetchDataAndRender on page load
fetchDataAndRender();

