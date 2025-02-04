async function fetchPastData() {
    let response = await fetch("/api/past");
    let data = await response.json();

    let labels = data.map(d => new Date(d.created_at).toLocaleTimeString());
    let mq7 = data.map(d => parseFloat(d.mq7));
    let mq135 = data.map(d => parseFloat(d.mq135));
    let dust = data.map(d => parseFloat(d.dust));

    let ctx = document.getElementById('airQualityChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                { 
                    label: 'MQ-7 (ppm)', 
                    data: mq7, 
                    borderColor: '#36a2eb', 
                    backgroundColor: 'rgba(54,162,235,0.2)', 
                    fill: true 
                },
                { 
                    label: 'MQ-135 (ppm)', 
                    data: mq135, 
                    borderColor: '#4bc0c0', 
                    backgroundColor: 'rgba(75,192,192,0.2)', 
                    fill: true 
                },
                { 
                    label: 'Dust (µg/m³)', 
                    data: dust, 
                    borderColor: '#9966ff', 
                    backgroundColor: 'rgba(153,102,255,0.2)', 
                    fill: true 
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true, // Makes sure the Y-axis starts from zero
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(2); // Format numbers
                        }
                    }
                }
            }
        }
    });
}

// Call the function to load the past data when the page loads
fetchPastData();
