const form = document.getElementById("running-form");
const planSection = document.getElementById("running-plan");

function renderPlan(plan, goalDistance) {
  if (!plan || plan.length === 0) {
    planSection.innerHTML = "<p>No plan was generated.</p>";
    return;
  }

  // Get all unique run types from the plan
  const runTypes = new Set();
  plan.forEach(week => {
    Object.keys(week).forEach(key => {
      if (key !== "Week" && key !== "Goal") {
        runTypes.add(key);
      }
    });
  });
  const runTypeArray = Array.from(runTypes);

  const headerRow = runTypeArray.map(type => `<th>${type}</th>`).join("");
  const rows = plan
    .map(
      (item) => {
        const cells = runTypeArray.map(type => `<td>${item[type] || "-"}</td>`).join("");
        return `<tr><td>${item["Week"]}</td>${cells}</tr>`;
      }
    )
    .join("");

  planSection.innerHTML = `
    <h3>${goalDistance} Training Plan (${plan.length} weeks)</h3>
    <table>
      <thead>
        <tr>
          <th>Week</th>
          ${headerRow}
        </tr>
      </thead>
      <tbody>
        ${rows}
      </tbody>
    </table>
  `;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const currentMileage = parseFloat(document.getElementById("current-mileage").value || 0);
  const goalDistance = document.getElementById("goal-distance").value;
  const raceDate = document.getElementById("race-date").value;
  const runsPerWeek = parseInt(document.getElementById("runs-per-week").value || 3);

  planSection.innerHTML = "<p>Generating your plan...</p>";

  try {
    const response = await fetch("/api/running-plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ currentMileage, goalDistance, raceDate, runsPerWeek }),
    });

    if (!response.ok) {
      throw new Error("Server error while generating plan.");
    }

    const data = await response.json();
    renderPlan(data.plan, data.goalDistance);
  } catch (error) {
    console.error(error);
    planSection.innerHTML = "<p>Unable to generate the running program right now.</p>";
  }
});
