// Initialize charts
const powerCtx = document.getElementById('power-chart').getContext('2d');
const componentCtx = document.getElementById('component-chart').getContext('2d');
const hourlyCtx = document.getElementById('hourly-chart').getContext('2d');

const powerChart = new Chart(powerCtx, {
    type: 'line',
    data: {
        labels: ['14:10', '14:20', '14:30', '14:40', '14:50', '15:00'],
        datasets: [{
            label: 'Power (kW)',
            data: [25, 32, 28, 40, 35, 30],
            borderColor: '#4285F4',
            backgroundColor: 'rgba(66, 133, 244, 0.1)',
            tension: 0.4,
            fill: true
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'kW'
                }
            }
        }
    }
});

const componentChart = new Chart(componentCtx, {
    type: 'doughnut',
    data: {
        labels: ['Drive Motor', 'Climate Control', 'Electronics', 'Lighting', 'Auxiliaries'],
        datasets: [{
            data: [24.5, 61.3, 8.2, 3.8, 2],
            backgroundColor: [
                '#4285F4',
                '#EA4335',
                '#FBBC05',
                '#34A853',
                '#9AA0A6'
            ]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'right'
            }
        }
    }
});

const hourlyChart = new Chart(hourlyCtx, {
    type: 'bar',
    data: {
        labels: ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'],
        datasets: [{
            label: 'Energy (kWh)',
            data: [23, 1.8, 4.2, 6.8, 5.4, 7.2, 8.9, 3.6],
            backgroundColor: '#4285F4'
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'kWh'
                }
            }
        }
    }
});

// Update dashboard with new data
function updateDashboard(data) {
    // Update health overview
    document.getElementById('health-value').textContent = `${data.health}%`;
    document.getElementById('remaining-distance').textContent = `${data.remaining_distance} km`;
    document.getElementById('temperature').textContent = `${data.temperature} °C`;
    document.getElementById('soc').textContent = `${100 - data.dod}%`;
    
    // Update health circle
    const healthCircle = document.querySelector('.health-circle');
    healthCircle.style.setProperty('--health-percent', `${data.health}%`);
    
    // Update energy consumption
    document.getElementById('total-used').textContent = `${data.power_consumption} kWh`;
    document.getElementById('daily-cost').textContent = `$${(data.power_consumption * 0.125 * 24).toFixed(2)}`;
    
    // Update power activity
    document.getElementById('current-power').textContent = `${(data.voltage * data.current / 1000).toFixed(1)} kW`;
    document.getElementById('peak-power').textContent = `${(data.voltage * data.current / 1000 * 2).toFixed(1)} kW`;
    
    // Update sensor readings
    document.getElementById('inclination').textContent = `${data.inclination}°`;
    document.getElementById('load').textContent = `${data.load} kg`;
    document.getElementById('jerk').textContent = `${data.jerk} m/s³`;
    document.getElementById('c-rate').textContent = `${data.c_rate} C`;
    document.getElementById('voltage').textContent = `${data.voltage} V`;
    document.getElementById('current').textContent = `${data.current} A`;
    
    // Update timestamp
    document.getElementById('update-time').textContent = new Date().toLocaleTimeString();
    
    // Update charts with new data
    updateCharts(data);
}

function updateCharts(data) {
    // Simulate updating charts with new data
    // In a real application, you would add the new data point and remove the oldest
    
    // Update power chart
    const newPowerValue = data.voltage * data.current / 1000;
    powerChart.data.datasets[0].data.push(newPowerValue);
    powerChart.data.datasets[0].data.shift();
    
    // Add new time label
    const now = new Date();
    const newTime = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;
    powerChart.data.labels.push(newTime);
    powerChart.data.labels.shift();
    
    powerChart.update();
    
    // Update component usage (simulated)
    componentChart.data.datasets[0].data = [
        data.power_consumption * 0.4,  // Drive Motor
        data.power_consumption * 0.3,  // Climate Control
        data.power_consumption * 0.15, // Electronics
        data.power_consumption * 0.1,  // Lighting
        data.power_consumption * 0.05  // Auxiliaries
    ];
    componentChart.update();
    
    // Update hourly consumption (simulated)
    const currentHour = now.getHours();
    if (currentHour % 3 === 0) {  // Update every 3 hours
        const hourIndex = currentHour / 3;
        hourlyChart.data.datasets[0].data[hourIndex] = data.power_consumption;
        hourlyChart.update();
    }
}

// Fetch data from server every 2 seconds
function fetchData() {
    fetch('/api/battery-data')
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// Initial data fetch
fetchData();

// Set up periodic data fetching
setInterval(fetchData, 2000);