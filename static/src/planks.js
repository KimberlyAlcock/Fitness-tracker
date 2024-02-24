document.getElementById("submitBtn").addEventListener("click", function() {
    // Get user input values
    let date = document.getElementById("tracker-date").date;
    let planks = document.getElementById("planks-input").checked;
    let pullups = document.getElementById("pullups-input").checked;
    let doubleUnders = document.getElementById("double-unders-input").checked;

    // Create a new table row
    let newRow = document.createElement("tr");

    // Insert data into the new row
    newRow.innerHTML = `
        <td>${date}</td>
        <td>${planks ? 'true' : 'false'}</td>
        <td>${pullups ? 'true' : 'false'}</td>
        <td>${doubleUnders ? 'true' : 'false'}</td>
    `;

    // Append the new row to the table body
    document.getElementById("data-body").appendChild(newRow);
});

document.getElementById("resetBtn").addEventListener("click", function() {
    // Clear the form inputs
    document.getElementById("dateInput").value = "";
    document.getElementById("planksCheckbox").checked = false;
    document.getElementById("pullupsCheckbox").checked = false;
    document.getElementById("doubleUndersCheckbox").checked = false;
});