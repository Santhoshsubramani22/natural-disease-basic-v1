document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/dashboard")
        .then(res => res.json())
        .then(data => {
            document.getElementById("statTotalPredictions").innerText = data.metrics.total_predictions;
            document.getElementById("statHighRisk").innerText = data.metrics.high_risk_predictions;
            document.getElementById("statActiveAlerts").innerText = data.metrics.active_alerts;
            document.getElementById("statAvgScore").innerText = data.metrics.average_risk_score;

            // Render Recent Predictions Table
            const tbody = document.getElementById("recentPredictionsBody");
            tbody.innerHTML = "";
            data.recent_predictions.forEach(p => {
                const badge = p.alert_level === 'RED' ? 'badge-red' : p.alert_level === 'ORANGE' ? 'badge-orange' : 'badge-yellow';
                tbody.innerHTML += `
                    <tr>
                        <td>${p.timestamp}</td>
                        <td>${p.disaster_type}</td>
                        <td>${p.location_name || 'N/A'}</td>
                        <td>${p.risk_score}/100</td>
                        <td><span class="badge ${badge}">${p.alert_level}</span></td>
                    </tr>`;
            });

            // Risk Level Distribution Chart
            const ctx = document.getElementById("riskDistChart").getContext("2d");
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(data.risk_distribution),
                    datasets: [{
                        data: Object.values(data.risk_distribution),
                        backgroundColor: ['#198754', '#ffc107', '#fd7e14', '#dc3545', '#6c757d']
                    }]
                }
            });
        });
});