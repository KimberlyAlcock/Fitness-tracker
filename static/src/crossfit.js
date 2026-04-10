let crossfitData = [];

function renderSummary(data) {
  const summaryElement = document.getElementById("crossfit-summary");
  if (!summaryElement) return;
  const skills = [...new Set(data.map((item) => item.Skill).filter(Boolean))];
  summaryElement.innerHTML = `
    <p>Loaded ${data.length} CrossFit entries.</p>
    <p>Tracked skills: ${skills.join(", ") || "none"}</p>
  `;
}

function renderTable(data) {
  const tableBody = document.getElementById("data-body-crossfit");
  tableBody.innerHTML = "";

  if (!data || data.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="3">No CrossFit stats available.</td></tr>';
    return;
  }

  data.forEach((item) => {
    const row = document.createElement("tr");
    ["Skill", "Stat", "Date"].forEach((key) => {
      const cell = document.createElement("td");
      cell.textContent = item[key] || "";
      row.appendChild(cell);
    });
    tableBody.appendChild(row);
  });
}

function getColumnIndex(column) {
  const headings = document.querySelectorAll("#data-table-crossfit th");
  for (let i = 0; i < headings.length; i += 1) {
    const headingText = headings[i].textContent.replace(/Sort/i, "").trim();
    if (headingText.toLowerCase() === column.toLowerCase()) {
      return i;
    }
  }
  return -1;
}

function sortTable(column) {
  if (!crossfitData.length) return;
  const sorted = [...crossfitData].sort((a, b) => {
    const aValue = (a[column] || "").toString();
    const bValue = (b[column] || "").toString();
    if (column === "Date") {
      return new Date(aValue) - new Date(bValue);
    }
    return aValue.localeCompare(bValue, undefined, { numeric: true, sensitivity: "base" });
  });

  renderTable(sorted);
}

function addSortingButtonListeners() {
  const sortingButtons = document.querySelectorAll("#data-table-crossfit th button");
  sortingButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const column = button.parentNode.textContent.replace(/Sort/i, "").trim();
      sortTable(column);
    });
  });
}

fetch("/api/crossfit")
  .then((response) => response.json())
  .then((data) => {
    crossfitData = data;
    renderTable(crossfitData);
    renderSummary(crossfitData);
    addSortingButtonListeners();
  })
  .catch((error) => {
    console.error("Error:", error);
    const tableBody = document.getElementById("data-body-crossfit");
    if (tableBody) {
      tableBody.innerHTML = '<tr><td colspan="3">Unable to load CrossFit data.</td></tr>';
    }
  });
