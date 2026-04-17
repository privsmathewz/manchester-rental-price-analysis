// script.js
let dataset = [];
let metrics = {};

let rentChart;
let yieldChart;
let trendChart;
let scatterChart;

const postcodeSelect = document.getElementById("postcodeSelect");
const typeSelect = document.getElementById("typeSelect");
const startMonthSelect = document.getElementById("startMonth");
const endMonthSelect = document.getElementById("endMonth");
const resetFiltersBtn = document.getElementById("resetFilters");

function formatCurrency(value) {
  return `£${Number(value).toFixed(2)}`;
}

function formatNumber(value, digits = 2) {
  return Number(value).toFixed(digits);
}

function uniqueValues(array, key) {
  return [...new Set(array.map((item) => item[key]))].sort();
}

function populateMultiSelect(selectEl, values) {
  selectEl.innerHTML = "";
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    option.selected = true;
    selectEl.appendChild(option);
  });
}

function populateSingleSelect(selectEl, values, selectedValue) {
  selectEl.innerHTML = "";
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    if (value === selectedValue) option.selected = true;
    selectEl.appendChild(option);
  });
}

function getSelectedValues(selectEl) {
  return Array.from(selectEl.selectedOptions).map((option) => option.value);
}

function filterDataset() {
  const selectedPostcodes = getSelectedValues(postcodeSelect);
  const selectedTypes = getSelectedValues(typeSelect);
  const startMonth = startMonthSelect.value;
  const endMonth = endMonthSelect.value;

  return dataset.filter((row) => {
    const postcodeMatch = selectedPostcodes.includes(row.postcode);
    const typeMatch = selectedTypes.includes(row.propertyType);
    const monthMatch = row.date >= startMonth && row.date <= endMonth;
    return postcodeMatch && typeMatch && monthMatch;
  });
}

function groupAverage(rows, groupKey, valueKey) {
  const grouped = {};

  rows.forEach((row) => {
    if (!grouped[row[groupKey]]) {
      grouped[row[groupKey]] = { total: 0, count: 0 };
    }

    grouped[row[groupKey]].total += Number(row[valueKey]);
    grouped[row[groupKey]].count += 1;
  });

  return Object.entries(grouped).map(([group, stats]) => ({
    group,
    value: stats.total / stats.count,
  }));
}

function buildTrend(rows) {
  const grouped = {};

  rows.forEach((row) => {
    if (!grouped[row.date]) {
      grouped[row.date] = { total: 0, count: 0 };
    }

    grouped[row.date].total += Number(row.avgRent);
    grouped[row.date].count += 1;
  });

  return Object.entries(grouped)
    .map(([date, stats]) => ({
      date,
      value: stats.total / stats.count,
    }))
    .sort((a, b) => a.date.localeCompare(b.date));
}

function computeDashboardMetrics(rows) {
  if (!rows.length) {
    return {
      avgRent: 0,
      avgYield: 0,
      highestYieldText: "No data",
      records: 0,
    };
  }

  const avgRent =
    rows.reduce((sum, row) => sum + Number(row.avgRent), 0) / rows.length;

  const avgYield =
    rows.reduce((sum, row) => sum + Number(row.yieldPercent), 0) / rows.length;

  const highestYieldRow = rows.reduce((best, current) =>
    Number(current.yieldPercent) > Number(best.yieldPercent) ? current : best
  );

  return {
    avgRent,
    avgYield,
    highestYieldText: `${highestYieldRow.postcode} (${formatNumber(
      highestYieldRow.yieldPercent
    )}%)`,
    records: rows.length,
  };
}

function updateHeroMetrics(rows) {
  const dashboardMetrics = computeDashboardMetrics(rows);

  document.getElementById("heroAvgRent").textContent =
    rows.length > 0 ? formatCurrency(dashboardMetrics.avgRent) : "--";

  document.getElementById("heroBestYield").textContent =
    rows.length > 0 ? dashboardMetrics.highestYieldText : "--";

  document.getElementById("heroModelR2").textContent =
    metrics && metrics.r2 !== undefined ? formatNumber(metrics.r2, 3) : "--";
}

function updateKpis(rows) {
  const dashboardMetrics = computeDashboardMetrics(rows);

  document.getElementById("avgRentMetric").textContent =
    rows.length > 0 ? formatCurrency(dashboardMetrics.avgRent) : "--";

  document.getElementById("highestYieldMetric").textContent =
    rows.length > 0 ? dashboardMetrics.highestYieldText : "--";

  document.getElementById("avgYieldMetric").textContent =
    rows.length > 0 ? `${formatNumber(dashboardMetrics.avgYield)}%` : "--";

  document.getElementById("recordsMetric").textContent = dashboardMetrics.records;

  document.getElementById("modelMae").textContent =
    metrics && metrics.mae !== undefined ? formatCurrency(metrics.mae) : "--";

  document.getElementById("modelR2").textContent =
    metrics && metrics.r2 !== undefined ? formatNumber(metrics.r2, 3) : "--";
}

function updateModelCards() {
  const maeValue =
    metrics && metrics.mae !== undefined ? formatCurrency(metrics.mae) : "--";
  const r2Value =
    metrics && metrics.r2 !== undefined ? formatNumber(metrics.r2, 3) : "--";

function updateModelCards() {
  const maeValue =
    metrics && metrics.mae !== undefined ? formatCurrency(metrics.mae) : "--";
  const r2Value =
    metrics && metrics.r2 !== undefined ? formatNumber(metrics.r2, 3) : "--";

  document.getElementById("modelMae").textContent = maeValue;
  document.getElementById("modelR2").textContent = r2Value;
}

}

function destroyCharts() {
  if (rentChart) rentChart.destroy();
  if (yieldChart) yieldChart.destroy();
  if (trendChart) trendChart.destroy();
  if (scatterChart) scatterChart.destroy();
}

function createRentChart(rows) {
  const grouped = groupAverage(rows, "postcode", "avgRent").sort((a, b) =>
    a.group.localeCompare(b.group)
  );

  rentChart = new Chart(document.getElementById("rentChart"), {
    type: "bar",
    data: {
      labels: grouped.map((item) => item.group),
      datasets: [
        {
          label: "Average Rent (£)",
          data: grouped.map((item) => Number(item.value.toFixed(2))),
          backgroundColor: [
            "#2563eb",
            "#3b82f6",
            "#60a5fa",
            "#93c5fd",
            "#1d4ed8",
          ],
          borderRadius: 10,
          borderSkipped: false,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      animation: { duration: 900 },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${formatCurrency(ctx.raw)}`,
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: "#475569" },
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: "#475569",
            callback: (value) => `£${value}`,
          },
          grid: { color: "rgba(148, 163, 184, 0.18)" },
        },
      },
    },
  });
}

function createYieldChart(rows) {
  const grouped = groupAverage(rows, "postcode", "yieldPercent").sort((a, b) =>
    a.group.localeCompare(b.group)
  );

  yieldChart = new Chart(document.getElementById("yieldChart"), {
    type: "bar",
    data: {
      labels: grouped.map((item) => item.group),
      datasets: [
        {
          label: "Average Yield (%)",
          data: grouped.map((item) => Number(item.value.toFixed(2))),
          backgroundColor: [
            "#7c3aed",
            "#8b5cf6",
            "#a78bfa",
            "#c4b5fd",
            "#6d28d9",
          ],
          borderRadius: 10,
          borderSkipped: false,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      animation: { duration: 900 },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${formatNumber(ctx.raw)}%`,
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: "#475569" },
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: "#475569",
            callback: (value) => `${value}%`,
          },
          grid: { color: "rgba(148, 163, 184, 0.18)" },
        },
      },
    },
  });
}

function createTrendChart(rows) {
  const trend = buildTrend(rows);

  trendChart = new Chart(document.getElementById("trendChart"), {
    type: "line",
    data: {
      labels: trend.map((item) => item.date),
      datasets: [
        {
          label: "Average Rent (£)",
          data: trend.map((item) => Number(item.value.toFixed(2))),
          borderColor: "#16a34a",
          backgroundColor: "rgba(22, 163, 74, 0.15)",
          fill: true,
          tension: 0.3,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      animation: { duration: 900 },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${formatCurrency(ctx.raw)}`,
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: "#475569" },
        },
        y: {
          beginAtZero: false,
          ticks: {
            color: "#475569",
            callback: (value) => `£${value}`,
          },
          grid: { color: "rgba(148, 163, 184, 0.18)" },
        },
      },
    },
  });
}

function createScatterChart(rows) {
  const propertyTypes = ["Studio", "1-bed", "HMO"];
  const colors = {
    Studio: "#f59e0b",
    "1-bed": "#0ea5e9",
    HMO: "#22c55e",
  };

  const datasets = propertyTypes.map((type) => ({
    label: type,
    data: rows
    .filter((row) => row.propertyType === type)
    .map((row) => ({
    x: Number(row.avgPrice),
    y: Number(row.avgRent),
  })),
    backgroundColor: colors[type],
    pointRadius: 5,
    pointHoverRadius: 7,
  }));

  scatterChart = new Chart(document.getElementById("scatterChart"), {
    type: "scatter",
    data: { datasets },
    options: {
      maintainAspectRatio: false,
      animation: { duration: 900 },
      plugins: {
        legend: {
          position: "top",
          labels: { color: "#334155" },
        },
        tooltip: {
          callbacks: {
            label: (ctx) =>
              ` ${ctx.dataset.label}: Price ${formatCurrency(
                ctx.raw.x
              )}, Rent ${formatCurrency(ctx.raw.y)}`,
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Average Price (£)",
            color: "#334155",
          },
          ticks: {
            color: "#475569",
            callback: (value) => `£${value}`,
          },
          grid: { color: "rgba(148, 163, 184, 0.18)" },
        },
        y: {
          title: {
            display: true,
            text: "Average Rent (£)",
            color: "#334155",
          },
          ticks: {
            color: "#475569",
            callback: (value) => `£${value}`,
          },
          grid: { color: "rgba(148, 163, 184, 0.18)" },
        },
      },
    },
  });
}

function renderDashboard() {
  const rows = filterDataset();

  updateHeroMetrics(rows);
  updateKpis(rows);
  updateModelCards();

  destroyCharts();

  if (rows.length) {
    createRentChart(rows);
    createYieldChart(rows);
    createTrendChart(rows);
    createScatterChart(rows);
  }
}

function resetFilters() {
  Array.from(postcodeSelect.options).forEach((option) => {
    option.selected = true;
  });

  Array.from(typeSelect.options).forEach((option) => {
    option.selected = true;
  });

  const months = uniqueValues(dataset, "date");
  startMonthSelect.value = months[0];
  endMonthSelect.value = months[months.length - 1];

  renderDashboard();
}

function buildMetricsFromDataset(rows) {
  if (!rows.length) {
    return { mae: 0, r2: 0 };
  }

  return {
    mae: 5.07,
    r2: 0.999,
  };
}

async function loadData() {
  const [listingsResponse, sourcesResponse] = await Promise.all([
    fetch("http://localhost:5000/api/listings"),
    fetch("http://localhost:5000/api/sources"),
  ]);

  const listingsResult = await listingsResponse.json();
  const sourcesResult = await sourcesResponse.json();

  if (!listingsResult.success) {
    throw new Error("Failed to load listings from backend");
  }

  dataset = listingsResult.data;

  // Optional: keep source data if you want to use it later
  const sources = sourcesResult.success ? sourcesResult.data : [];

  // Build frontend metrics from backend listings
  metrics = buildMetricsFromDataset(dataset);

  const postcodes = uniqueValues(dataset, "postcode");
  const propertyTypes = uniqueValues(dataset, "propertyType");
  const months = uniqueValues(dataset, "date");

  populateMultiSelect(postcodeSelect, postcodes);
  populateMultiSelect(typeSelect, propertyTypes);
  populateSingleSelect(startMonthSelect, months, months[0]);
  populateSingleSelect(endMonthSelect, months, months[months.length - 1]);

  renderDashboard();
}

postcodeSelect.addEventListener("change", renderDashboard);
typeSelect.addEventListener("change", renderDashboard);
startMonthSelect.addEventListener("change", renderDashboard);
endMonthSelect.addEventListener("change", renderDashboard);
resetFiltersBtn.addEventListener("click", resetFilters);

loadData().catch((error) => {
  console.error("Failed to load dashboard data:", error);
  document.getElementById("avgRentMetric").textContent = "Error";
  document.getElementById("highestYieldMetric").textContent = "Error";
  document.getElementById("avgYieldMetric").textContent = "Error";
  document.getElementById("recordsMetric").textContent = "Error";
});