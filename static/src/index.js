// this function fetches the data for the practice tracker table from the python file

$(document).ready(function() {
    // Fetch data from Flask endpoint
    $.getJSON('/get_excel_data', function(data) {
        // Generate table rows
        $.each(data, function(index, row) {
            var tr = $('<tr>');
            $.each(row, function(index, cell) {
                tr.append($('<td>').text(cell));
            });
            $('#excel-table').append(tr);
        });
    });
});


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