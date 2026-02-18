/* ============================================
   SentinelAI - Chart.js Configurations
   ============================================ */

// Chart.js Global Defaults
Chart.defaults.color = '#999999';
Chart.defaults.borderColor = '#2e2e2e';
Chart.defaults.font.family = "'Inter', system-ui, sans-serif";

document.addEventListener('DOMContentLoaded', function () {
    initDashboardCharts();
    initIntelligenceCharts();
    initNetworkCharts();
    initCameraCharts();
});

// ---- DASHBOARD CHARTS ----
function initDashboardCharts() {
    // Alert Trends
    const alertCtx = document.getElementById('alertTrendsChart');
    if (alertCtx) {
        new Chart(alertCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [
                    { label: 'Critical', data: [3, 2, 4, 1, 3, 2, 2], borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.1)', fill: true, tension: 0.4 },
                    { label: 'Warning', data: [5, 4, 6, 3, 5, 4, 3], borderColor: '#eab308', backgroundColor: 'rgba(234,179,8,0.1)', fill: true, tension: 0.4 },
                    { label: 'Info', data: [8, 6, 9, 7, 8, 5, 4], borderColor: '#14b8a6', backgroundColor: 'rgba(20,184,166,0.1)', fill: true, tension: 0.4 },
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'top', labels: { boxWidth: 12, padding: 16 } } },
                scales: { y: { beginAtZero: true, grid: { color: '#2e2e2e' } }, x: { grid: { display: false } } }
            }
        });
    }

    // Detection Distribution
    const detCtx = document.getElementById('detectionChart');
    if (detCtx) {
        new Chart(detCtx, {
            type: 'doughnut',
            data: {
                labels: ['Elephant', 'Tiger', 'Deer', 'Person', 'Vehicle', 'Other'],
                datasets: [{
                    data: [12, 5, 8, 6, 4, 3],
                    backgroundColor: ['#14b8a6', '#eab308', '#22c55e', '#ef4444', '#8b5cf6', '#6b7280'],
                    borderWidth: 0,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'right', labels: { boxWidth: 12, padding: 12 } } },
                cutout: '65%'
            }
        });
    }

    // Network Health
    const netCtx = document.getElementById('networkHealthChart');
    if (netCtx) {
        new Chart(netCtx, {
            type: 'line',
            data: {
                labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
                datasets: [{
                    label: 'Network Health %',
                    data: [95.2, 94.8, 95.1, 94.5, 93.2, 94.0, 95.5, 96.1, 95.8, 94.9, 95.3, 94.7, 93.8, 94.2, 95.0, 95.4, 94.6, 93.9, 94.3, 95.1, 94.8, 95.2, 94.5, 94.9],
                    borderColor: '#14b8a6',
                    backgroundColor: 'rgba(20,184,166,0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0,
                    pointHoverRadius: 4
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { min: 90, max: 100, grid: { color: '#2e2e2e' }, ticks: { callback: v => v + '%' } },
                    x: { grid: { display: false }, ticks: { maxTicksLimit: 8 } }
                }
            }
        });
    }
}

// ---- INTELLIGENCE CHARTS ----
function initIntelligenceCharts() {
    // 6-Month Trend
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx) {
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
                datasets: [
                    { label: 'Poaching Attempts', data: [12, 18, 22, 15, 28, 24], borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.1)', fill: true, tension: 0.4 },
                    { label: 'Wildlife Incidents', data: [8, 12, 15, 10, 14, 11], borderColor: '#eab308', backgroundColor: 'rgba(234,179,8,0.1)', fill: true, tension: 0.4 },
                    { label: 'Patrols Completed', data: [45, 52, 48, 55, 60, 58], borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,0.1)', fill: true, tension: 0.4 },
                    { label: 'Detections', data: [120, 145, 168, 132, 195, 178], borderColor: '#14b8a6', backgroundColor: 'rgba(20,184,166,0.1)', fill: true, tension: 0.4 },
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: { legend: { position: 'top', labels: { boxWidth: 12, padding: 16 } } },
                scales: { y: { beginAtZero: true, grid: { color: '#2e2e2e' } }, x: { grid: { display: false } } }
            }
        });
    }

    // Seasonal Risk
    const seasonCtx = document.getElementById('seasonalChart');
    if (seasonCtx) {
        new Chart(seasonCtx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Risk Level',
                    data: [45, 38, 42, 55, 48, 72, 85, 92, 88, 78, 52, 40],
                    backgroundColor: function (context) {
                        const v = context.raw;
                        if (v >= 80) return 'rgba(239,68,68,0.8)';
                        if (v >= 60) return 'rgba(234,179,8,0.8)';
                        return 'rgba(20,184,166,0.8)';
                    },
                    borderRadius: 4,
                    barPercentage: 0.7
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, max: 100, grid: { color: '#2e2e2e' }, ticks: { callback: v => v + '%' } }, x: { grid: { display: false } } }
            }
        });
    }

    // Zone Risk Timeline
    const zoneCtx = document.getElementById('zoneRiskChart');
    if (zoneCtx) {
        new Chart(zoneCtx, {
            type: 'line',
            data: {
                labels: ['2021', '2022', '2023', '2024', '2025'],
                datasets: [
                    { label: 'Northern Corridor', data: [65, 72, 80, 85, 90], borderColor: '#ef4444', tension: 0.3, pointRadius: 3 },
                    { label: 'Eastern Reserve', data: [45, 52, 58, 62, 68], borderColor: '#eab308', tension: 0.3, pointRadius: 3 },
                    { label: 'Central Area', data: [30, 28, 35, 32, 38], borderColor: '#22c55e', tension: 0.3, pointRadius: 3 },
                    { label: 'Southern Basin', data: [55, 60, 65, 70, 75], borderColor: '#8b5cf6', tension: 0.3, pointRadius: 3 },
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'top', labels: { boxWidth: 12, padding: 16 } } },
                scales: { y: { beginAtZero: true, grid: { color: '#2e2e2e' } }, x: { grid: { display: false } } }
            }
        });
    }
}

// ---- NETWORK CHARTS ----
function initNetworkCharts() {
    const sigCtx = document.getElementById('signalChart');
    if (sigCtx) {
        new Chart(sigCtx, {
            type: 'line',
            data: {
                labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
                datasets: [
                    { label: 'CAM-NC-01', data: [85, 86, 84, 83, 85, 87, 88, 85, 84, 82, 83, 85, 86, 84, 83, 85, 87, 88, 85, 84, 82, 83, 85, 85], borderColor: '#14b8a6', tension: 0.3, pointRadius: 0 },
                    { label: 'CAM-ER-02', data: [55, 52, 48, 45, 42, 40, 38, 35, 32, 30, 35, 40, 45, 42, 38, 35, 32, 30, 35, 40, 45, 42, 45, 45], borderColor: '#eab308', tension: 0.3, pointRadius: 0 },
                    { label: 'CAM-SB-01', data: [60, 58, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], borderColor: '#ef4444', tension: 0.3, pointRadius: 0 },
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'top', labels: { boxWidth: 12, padding: 16 } } },
                scales: {
                    y: { beginAtZero: true, max: 100, grid: { color: '#2e2e2e' }, ticks: { callback: v => v + '%' } },
                    x: { grid: { display: false }, ticks: { maxTicksLimit: 8 } }
                }
            }
        });
    }
}

// ---- CAMERA CHARTS ----
function initCameraCharts() {
    // Detection Timeline
    const dtCtx = document.getElementById('detectionTimelineChart');
    if (dtCtx) {
        new Chart(dtCtx, {
            type: 'bar',
            data: {
                labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
                datasets: [
                    { label: 'Wildlife', data: [2, 1, 0, 0, 1, 3, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 2, 1], backgroundColor: 'rgba(20,184,166,0.7)', borderRadius: 4, barPercentage: 0.6 },
                    { label: 'Person', data: [0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, 0, 1, 2, 1, 0, 0, 0], backgroundColor: 'rgba(239,68,68,0.7)', borderRadius: 4, barPercentage: 0.6 },
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'top', labels: { boxWidth: 12, padding: 16 } } },
                scales: {
                    y: { beginAtZero: true, stacked: true, grid: { color: '#2e2e2e' } },
                    x: { stacked: true, grid: { display: false }, ticks: { maxTicksLimit: 8 } }
                }
            }
        });
    }

    // Detection Distribution (cameras page)
    const ddCtx = document.getElementById('detectionDistChart');
    if (ddCtx) {
        new Chart(ddCtx, {
            type: 'polarArea',
            data: {
                labels: ['Elephant', 'Tiger', 'Deer', 'Person', 'Vehicle'],
                datasets: [{
                    data: [12, 5, 8, 6, 4],
                    backgroundColor: ['rgba(20,184,166,0.7)', 'rgba(234,179,8,0.7)', 'rgba(34,197,94,0.7)', 'rgba(239,68,68,0.7)', 'rgba(139,92,246,0.7)'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'right', labels: { boxWidth: 12, padding: 12 } } },
                scales: { r: { grid: { color: '#2e2e2e' }, ticks: { display: false } } }
            }
        });
    }

    // Confidence chart
    const confCtx = document.getElementById('confidenceChart');
    if (confCtx) {
        new Chart(confCtx, {
            type: 'bar',
            data: {
                labels: ['Elephant', 'Tiger', 'Deer', 'Person', 'Vehicle'],
                datasets: [{
                    label: 'Avg Confidence',
                    data: [96, 92, 88, 85, 78],
                    backgroundColor: ['rgba(20,184,166,0.8)', 'rgba(234,179,8,0.8)', 'rgba(34,197,94,0.8)', 'rgba(239,68,68,0.8)', 'rgba(139,92,246,0.8)'],
                    borderRadius: 4,
                    barPercentage: 0.5
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: { legend: { display: false } },
                scales: {
                    x: { beginAtZero: true, max: 100, grid: { color: '#2e2e2e' }, ticks: { callback: v => v + '%' } },
                    y: { grid: { display: false } }
                }
            }
        });
    }
}
