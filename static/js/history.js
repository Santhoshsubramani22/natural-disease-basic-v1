document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/history")
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById("historyTableBody");
            tbody.innerHTML = "";
            data.history.forEach(h => {
                tbody.innerHTML += `
                    <tr>
                        <td>${h.timestamp}</td>
                        <td>${h.disaster_type}</td>
                        <td>${h.location_name || 'N/A'}</td>
                        <td>${h.probability}%</td>
                        <td>${h.risk_score}/100</td>
                        <td>${h.risk_level}</td>
                        <td>${h.model_used}</td>
                    </tr>`;
            });
        });
});