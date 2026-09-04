let map = null;
let markersArray = [];

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 20.5937, lng: 78.9629 }, // Center over India / Global default
        zoom: 5
    });
    updateMapData();
}

function updateMapData() {
    if (!map) return;
    const dFilter = document.getElementById("mapDisasterFilter").value;
    const rFilter = document.getElementById("mapRiskFilter").value;

    fetch(`/api/map-data?disaster=${dFilter}&risk=${rFilter}`)
        .then(res => res.json())
        .then(data => {
            // Clear existing markers
            markersArray.forEach(m => m.setMap(null));
            markersArray = [];

            data.markers.forEach(item => {
                const color = item.alert_level === 'RED' ? '#dc3545' : item.alert_level === 'ORANGE' ? '#fd7e14' : item.alert_level === 'YELLOW' ? '#ffc107' : '#198754';
                
                const marker = new google.maps.Marker({
                    position: { lat: item.lat, lng: item.lng },
                    map: map,
                    title: `${item.disaster_type} Risk: ${item.risk_score}`,
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 8,
                        fillColor: color,
                        fillOpacity: 0.8,
                        strokeWeight: 1,
                        strokeColor: '#ffffff'
                    }
                });

                const info = new google.maps.InfoWindow({
                    content: `
                        <div>
                            <h4>${item.disaster_type} - ${item.location_name}</h4>
                            <p><strong>Location:</strong> ${item.state}, ${item.country}</p>
                            <p><strong>Risk Score:</strong> ${item.risk_score}/100 (${item.risk_level})</p>
                            <p><strong>Severity:</strong> ${item.severity}/10</p>
                        </div>`
                });

                marker.addListener("click", () => info.open(map, marker));
                markersArray.push(marker);
            });
        });
}