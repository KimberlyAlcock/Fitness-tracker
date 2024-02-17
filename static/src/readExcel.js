/*
const xlsx = require('xlsx');
const fs = require('fs');

// Load Excel file
const workbook = xlsx.readFile('../../data/practice-tracker.xlsx');

// Get the first worksheet
const sheetName = workbook.SheetNames[0];
const worksheet = workbook.Sheets[sheetName];

// Convert worksheet to JSON
const data = xlsx.utils.sheet_to_json(worksheet);

// Output the data
console.log(data);

// Write data to a JSON file (optional)
fs.writeFileSync('data.json', JSON.stringify(data, null, 2));

const express = require('express');
const app = express();

app.get('/data', (req, res) => {
    res.json(data); // Send the data to the client
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
*/