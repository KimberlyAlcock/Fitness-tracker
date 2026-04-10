const form = document.getElementById("running-form");
const planSection = document.getElementById("running-plan");

function renderPlan(plan, goalDistance) {
  if (!plan || plan.length === 0) {
    planSection.innerHTML = "<p>No plan was generated.</p>";
    return;
  }

  const rows = plan
    .map(
      (item) => `
      <tr>
        <td>${item["Week"]}</td>
        <td>${item["Easy Run"]}</td>
        <td>${item["Tempo Run"]}</td>
        <td>${item["Long Run"]}</td>
      </tr>`
    )
    .join("");

  planSection.innerHTML = `
    <h3>${goalDistance} Training Plan</h3>
    <table>
      <thead>
        <tr>
          <th>Week</th>
          <th>Easy Run</th>
          <th>Tempo Run</th>
          <th>Long Run</th>
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

  planSection.innerHTML = "<p>Generating your plan...</p>";

  try {
    const response = await fetch("/api/running-plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ currentMileage, goalDistance }),
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
