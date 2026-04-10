const dateInput = document.querySelector("#tracker-date input");
const planksInput = document.querySelector("#planks-input input");
const pullupsInput = document.querySelector("#pullups-input input");
const doubleUndersInput = document.querySelector("#double-unders-input input");
const tableBody = document.getElementById("data-body");
const submitBtn = document.getElementById("submitBtn");
const resetBtn = document.getElementById("resetBtn");

function formatBoolean(value) {
  if (value === true || value === "true") return "✔";
  if (value === false || value === "false") return "✘";
  return value ? "✔" : "✘";
}

function createRow(item) {
  const row = document.createElement("tr");
  const values = [item.Date, formatBoolean(item.Planks), formatBoolean(item.Pullups), formatBoolean(item["Double-unders"])];
  values.forEach((value) => {
    const cell = document.createElement("td");
    cell.textContent = value;
    row.appendChild(cell);
  });
  return row;
}

function renderTable(data) {
  tableBody.innerHTML = "";
  if (!data || data.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="4">No practice history available.</td></tr>';
    return;
  }
  data.forEach((item) => {
    tableBody.appendChild(createRow(item));
  });
}

function clearForm() {
  dateInput.value = "";
  planksInput.checked = false;
  pullupsInput.checked = false;
  doubleUndersInput.checked = false;
}

async function loadPracticeData() {
  try {
    const response = await fetch("/api/practice");
    const data = await response.json();
    renderTable(data);
  } catch (error) {
    console.error("Error loading practice data:", error);
    tableBody.innerHTML = '<tr><td colspan="4">Unable to load practice data.</td></tr>';
  }
}

async function addPracticeEntry(entry) {
  const response = await fetch("/api/practice", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(entry),
  });

  if (!response.ok) {
    throw new Error("Failed to save practice entry");
  }

  const result = await response.json();
  tableBody.appendChild(createRow(result.entry));
}

submitBtn.addEventListener("click", async () => {
  if (!dateInput.value) {
    alert("Please choose a date before submitting.");
    return;
  }

  const userInput = {
    Date: dateInput.value,
    Planks: planksInput.checked,
    Pullups: pullupsInput.checked,
    "Double-unders": doubleUndersInput.checked,
  };

  try {
    await addPracticeEntry(userInput);
    clearForm();
  } catch (error) {
    console.error("Error:", error);
    alert("Unable to save your practice entry. Try again later.");
  }
});

resetBtn.addEventListener("click", clearForm);

loadPracticeData();



