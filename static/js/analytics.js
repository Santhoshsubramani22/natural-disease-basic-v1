document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/analytics")
        .then(res => res.json())
        .then(data => {
            // Disaster Frequency Chart
            const ctx1 = document.getElementById("disasterFreqChart").getContext("2d");
            new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: Object.keys(data.disaster_counts),
                    datasets: [{
                        label: 'Dataset Total Occurrences',
                        data: Object.values(data.disaster_counts),
                        backgroundColor: '#0d6efd'
                    }]
                }
            });

            // Scatter Chart Rainfall vs Flood
            const ctx2 = document.getElementById("rainfallFloodChart").getContext("2d");
            const floodScatter = data.scatter_samples.flood.map(r => ({ x: r.rainfall_24h_mm, y: r.flood_occurrence }));
            new Chart(ctx2, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: '24h Rainfall vs Flood (0/1)',
                        data: floodScatter,
                        backgroundColor: '#dc3545'
                    }]
                },
                options: {
                    scales: {
                        x: { title: { display: true, text: '24h Rainfall (mm)' } },
                        y: { title: { display: true, text: 'Flood Occurrence (0/1)' } }
                    }
                }
            });
        });
});