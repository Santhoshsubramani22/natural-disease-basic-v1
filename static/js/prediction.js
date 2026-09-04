const disasterSchema = {
    Flood: [
        { id: "rainfall_24h_mm", label: "24h Rainfall (mm)", val: 180 },
        { id: "rainfall_7d_mm", label: "7-Day Rainfall (mm)", val: 450 },
        { id: "river_level_m", label: "River Level (m)", val: 6.5 },
        { id: "soil_moisture_percent", label: "Soil Moisture (%)", val: 85 },
        { id: "elevation_m", label: "Elevation (m)", val: 12 }
    ],
    Earthquake: [
        { id: "earthquake_magnitude", label: "Magnitude (Richter)", val: 6.8 },
        { id: "earthquake_depth_km", label: "Depth (km)", val: 15 },
        { id: "distance_to_fault_km", label: "Distance to Fault (km)", val: 8 },
        { id: "ground_acceleration_g", label: "Ground Acceleration (g)", val: 0.45 }
    ],
    Cyclone: [
        { id: "cyclone_wind_speed_kmh", label: "Wind Speed (km/h)", val: 165 },
        { id: "cyclone_pressure_hpa", label: "Central Pressure (hPa)", val: 940 },
        { id: "storm_surge_m", label: "Storm Surge (m)", val: 3.8 }
    ],
    Wildfire: [
        { id: "temperature_c", label: "Temperature (°C)", val: 41 },
        { id: "vegetation_dryness_index", label: "Vegetation Dryness", val: 0.88 },
        { id: "fire_weather_index", label: "Fire Weather Index", val: 38 },
        { id: "wind_speed_kmh", label: "Wind Speed (km/h)", val: 32 }
    ],
    Landslide: [
        { id: "slope_degree", label: "Slope Degree (°)", val: 38 },
        { id: "soil_saturation_percent", label: "Soil Saturation (%)", val: 92 },
        { id: "rainfall_24h_mm", label: "24h Rainfall (mm)", val: 140 }
    ],
    Drought: [
        { id: "drought_index", label: "Drought Index", val: -3.8 },
        { id: "precipitation_anomaly_percent", label: "Precipitation Anomaly (%)", val: -60 },
        { id: "soil_moisture_percent", label: "Soil Moisture (%)", val: 12 }
    ],
    Tsunami: [
        { id: "earthquake_magnitude", label: "Undersea Eq Magnitude", val: 7.9 },
        { id: "sea_level_anomaly_m", label: "Sea Level Anomaly (m)", val: 2.4 },
        { id: "distance_to_coast_km", label: "Distance to Coast (km)", val: 4 }
    ]
};

let factorChart = null;

function renderDynamicInputs() {
    const type = document.getElementById("disasterType").value;
    const container = document.getElementById("dynamicInputs");
    container.innerHTML = "";

    const fields = disasterSchema[type] || [];
    fields.forEach(f => {
        container.innerHTML += `
            <div class="form-group">
                <label>${f.label}</label>
                <input type="number" step="any" id="${f.id}" name="${f.id}" value="${f.val}" required>
            </div>`;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    renderDynamicInputs();
    const form = document.getElementById("predictionForm");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const payload = {
                disaster_type: document.getElementById("disasterType").value,
                algorithm: document.getElementById("algorithm").value,
                location_name: document.getElementById("location_name").value,
                latitude: parseFloat(document.getElementById("latitude").value),
                longitude: parseFloat(document.getElementById("longitude").value)
            };

            const inputs = document.querySelectorAll("#dynamicInputs input");
            inputs.forEach(inp => payload[inp.id] = parseFloat(inp.value));

            const res = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            displayResults(data);
        });
    }
});

function getUserLocation() {
    const status = document.getElementById("locationStatus");
    if (!navigator.geolocation) {
        status.innerText = "Geolocation not supported.";
        return;
    }
    status.innerText = "Locating...";
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            document.getElementById("latitude").value = pos.coords.latitude.toFixed(4);
            document.getElementById("longitude").value = pos.coords.longitude.toFixed(4);
            status.innerText = "Location updated!";
        },
        () => { status.innerText = "Unable to retrieve location."; }
    );
}

function displayResults(data) {
    const out = document.getElementById("predictionOutput");
    const badgeClass = data.alert_level === 'RED' ? 'badge-red' : data.alert_level === 'ORANGE' ? 'badge-orange' : data.alert_level === 'YELLOW' ? 'badge-yellow' : 'badge-green';

    out.innerHTML = `
        <div class="res-box">
            <h4>Prediction: <strong>${data.prediction}</strong></h4>
            <p>Probability: <strong>${data.probability}%</strong></p>
            <p>Risk Score: <strong>${data.risk_score}/100</strong> (<span class="badge ${badgeClass}">${data.risk_level}</span>)</p>
            <p>Severity Scale: <strong>${data.severity}/10</strong> | Alert Level: <strong>${data.alert_level}</strong></p>
            <hr>
            <p><strong>Explanation:</strong> ${data.explanation}</p>
            <p><strong>Warning Message:</strong> <em>${data.alert_message}</em></p>
        </div>
    `;

    renderFactorChart(data.top_factors || []);
}

function renderFactorChart(factors) {
    const ctx = document.getElementById("factorChart").getContext("2d");
    if (factorChart) factorChart.destroy();

    factorChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: factors.map(f => f.feature),
            datasets: [{
                label: 'Relative Impact Factor',
                data: factors.map(f => f.score || f.importance),
                backgroundColor: '#0d6efd'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { title: { display: true, text: 'Top Contributing Parameters' } }
        }
    });
}