document.addEventListener("DOMContentLoaded", loadAlerts);

function loadAlerts() {
    fetch("/api/alerts")
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById("alertsTableBody");
            tbody.innerHTML = "";
            data.alerts.forEach(a => {
                const badge = a.alert_level === 'RED' ? 'badge-red' : a.alert_level === 'ORANGE' ? 'badge-orange' : 'badge-yellow';
                tbody.innerHTML += `
                    <tr>
                        <td>${a.timestamp}</td>
                        <td>${a.disaster_type}</td>
                        <td>${a.location}</td>
                        <td><span class="badge ${badge}">${a.alert_level}</span></td>
                        <td>${a.message}</td>
                        <td>${a.status}</td>
                        <td>
                            ${a.status === 'Unread' ? `<button class="btn btn-secondary" onclick="markRead(${a.id})">Mark Read</button>` : 'Resolved'}
                        </td>
                    </tr>`;
            });
        });
}

function markRead(id) {
    fetch("/api/alerts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id, status: "Read" })
    }).then(() => loadAlerts());
}