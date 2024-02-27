// Sets event listener to get info from user
document.getElementById("submitBtn").addEventListener("click", function() {
    // Get user input values
    let date = document.getElementById("tracker-date").querySelector("input").value;
    let planks = document.getElementById("planks-input").querySelector("input").checked;
    let pullups = document.getElementById("pullups-input").querySelector("input").checked;
    let doubleUnders = document.getElementById("double-unders-input").querySelector("input").checked;

    // Create a new table row
    let newRow = document.createElement("tr");

    let userInput = {
        Date: date,
        Planks: planks,
        Pullups: pullups,
        "Double-unders": doubleUnders
    };
    
    console.log(userInput)

    // Insert data into the new row
    newRow.innerHTML = `
        <td>${date}</td>
        <td>${planks ? 'true' : 'false'}</td>
        <td>${pullups ? 'true' : 'false'}</td>
        <td>${doubleUnders ? 'true' : 'false'}</td>
    `;

    // Append the new row to the table body
    document.getElementById("data-body").appendChild(newRow);

    // Clear the form inputs
    document.getElementById("tracker-date").querySelector("input").value = "";
    document.getElementById("planks-input").querySelector("input").checked = false;
    document.getElementById("pullups-input").querySelector("input").checked = false;
    document.getElementById("double-unders-input").querySelector("input").checked = false;
});

// Sets event listener for Reset button
document.getElementById("resetBtn").addEventListener("click", function() {
    // Clear the form inputs
    document.getElementById("tracker-date").querySelector("input").value = "";
    document.getElementById("planks-input").querySelector("input").checked = false;
    document.getElementById("pullups-input").querySelector("input").checked = false;
    document.getElementById("double-unders-input").querySelector("input").checked = false;
});





