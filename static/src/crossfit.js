fetch('../static/src/crossfitData.json')
.then(response => response.json())
.then(data => {
    const tableBody = document.getElementById('data-body-crossfit');

    // Iterate over the data and create table rows
    data.forEach(item => {
        const row = document.createElement('tr');
        Object.keys(item).forEach(key => {
            const cell = document.createElement('td');
            cell.textContent = item[key];
            row.appendChild(cell);
        });
        tableBody.appendChild(row);
    });
})
.catch(error => console.error('Error:', error));