/* ============================================
   SentinelAI - Main Application JavaScript
   ============================================ */

// ---- Clock ----
function updateClock() {
    const el = document.getElementById('current-time');
    if (!el) return;
    const now = new Date();
    el.textContent = now.toLocaleString('en-US', {
        month: 'short', day: 'numeric', year: 'numeric',
        hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
}
updateClock();
setInterval(updateClock, 1000);

// ---- Tab Switching (Cameras page) ----
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-trigger').forEach(t => t.classList.remove('active'));
    const tab = document.getElementById('tab-' + tabName);
    if (tab) tab.classList.add('active');
    event.currentTarget.classList.add('active');
    // Re-init icons for dynamic content
    if (window.lucide) lucide.createIcons();
}

// ---- Patrol Expand/Collapse ----
function togglePatrol(card) {
    const expanded = card.querySelector('.patrol-expanded');
    if (!expanded) return;
    const isVisible = expanded.classList.contains('visible');
    // Collapse all
    document.querySelectorAll('.patrol-expanded').forEach(e => e.classList.remove('visible'));
    document.querySelectorAll('.patrol-card').forEach(c => c.classList.remove('selected'));
    if (!isVisible) {
        expanded.classList.add('visible');
        card.classList.add('selected');
    }
    if (window.lucide) lucide.createIcons();
}

// ---- Network Node Expand/Collapse ----
function toggleNode(card) {
    const expanded = card.querySelector('.node-expanded');
    if (!expanded) return;
    const isVisible = expanded.classList.contains('visible');
    // Collapse all
    document.querySelectorAll('.node-expanded').forEach(e => e.classList.remove('visible'));
    document.querySelectorAll('.node-card').forEach(c => c.classList.remove('selected'));
    if (!isVisible) {
        expanded.classList.add('visible');
        card.classList.add('selected');
    }
}

// ---- Alerts Page ----
const alertsData = [
    { id: 1, title: 'Unauthorized Movement Detected', description: 'Potential poacher activity near water source', severity: 'critical', status: 'active', time: '2 minutes ago', location: 'Northern Corridor', camera: 'CAM-NC-01' },
    { id: 2, title: 'Wildlife Aggregation', description: 'Unusual elephant herd gathering detected', severity: 'warning', status: 'acknowledged', time: '15 minutes ago', location: 'Eastern Reserve', camera: 'CAM-ER-03' },
    { id: 3, title: 'Network Connectivity Issue', description: 'Node connection degradation detected', severity: 'info', status: 'resolved', time: '28 minutes ago', location: 'Central Area', camera: 'CAM-CA-02' },
    { id: 4, title: 'Suspicious Vehicle Detected', description: 'Unregistered vehicle near reserve boundary', severity: 'critical', status: 'active', time: '35 minutes ago', location: 'Southern Basin', camera: 'CAM-SB-01' },
    { id: 5, title: 'Camera Offline', description: 'Camera SB-01 not responding to heartbeat', severity: 'warning', status: 'acknowledged', time: '1 hour ago', location: 'Southern Basin', camera: 'CAM-SB-01' },
    { id: 6, title: 'Fence Line Breach', description: 'Perimeter sensor triggered near gate 4', severity: 'warning', status: 'acknowledged', time: '1 hour ago', location: 'Western Plains', camera: 'CAM-WP-05' },
    { id: 7, title: 'Patrol Communication Lost', description: 'Lost contact with Delta team for 3 minutes', severity: 'info', status: 'resolved', time: '2 hours ago', location: 'Central Area', camera: 'CAM-CA-01' },
    { id: 8, title: 'Scheduled Maintenance Reminder', description: 'Camera NC-02 due for quarterly service', severity: 'info', status: 'resolved', time: '3 hours ago', location: 'Northern Corridor', camera: 'CAM-NC-02' },
];

let currentSeverityFilter = 'all';
let currentStatusFilter = 'all';

function renderAlerts() {
    const container = document.getElementById('alertsList');
    const countEl = document.getElementById('alertCount');
    const noMsg = document.getElementById('noAlertsMsg');
    if (!container) return;

    const searchTerm = (document.getElementById('alertSearch')?.value || '').toLowerCase();
    const filtered = alertsData.filter(a => {
        const matchSeverity = currentSeverityFilter === 'all' || a.severity === currentSeverityFilter;
        const matchStatus = currentStatusFilter === 'all' || a.status === currentStatusFilter;
        const matchSearch = !searchTerm || a.title.toLowerCase().includes(searchTerm) || a.location.toLowerCase().includes(searchTerm) || a.camera.toLowerCase().includes(searchTerm);
        return matchSeverity && matchStatus && matchSearch;
    });

    if (countEl) countEl.textContent = `Showing ${filtered.length} of ${alertsData.length} alerts`;

    const clearBtn = document.getElementById('clearFilters');
    if (clearBtn) clearBtn.style.display = (currentSeverityFilter !== 'all' || currentStatusFilter !== 'all' || searchTerm) ? '' : 'none';

    if (filtered.length === 0) {
        container.innerHTML = '';
        if (noMsg) noMsg.style.display = '';
        return;
    }
    if (noMsg) noMsg.style.display = 'none';

    const iconMap = { critical: 'alert-triangle', warning: 'alert-circle', info: 'alert-circle' };
    container.innerHTML = filtered.map(a => `
    <div class="alert-card ${a.severity}">
      <div class="alert-card-header">
        <div class="alert-card-left">
          <div class="alert-icon-wrap ${a.severity}"><i data-lucide="${iconMap[a.severity]}" style="width:20px;height:20px"></i></div>
          <div class="flex-1">
            <div class="alert-title-row">
              <h4>${a.title}</h4>
              <span class="badge badge-${a.severity}">${a.severity.toUpperCase()}</span>
            </div>
            <p class="alert-desc">${a.description}</p>
          </div>
        </div>
        <span class="alert-status-badge ${a.status}">${a.status.charAt(0).toUpperCase() + a.status.slice(1)}</span>
      </div>
      <div class="alert-details">
        <div class="alert-detail-item"><i data-lucide="clock" style="width:16px;height:16px"></i><span>${a.time}</span></div>
        <div class="alert-detail-item"><i data-lucide="map-pin" style="width:16px;height:16px"></i><span>${a.location}</span></div>
        <div class="alert-detail-item"><i data-lucide="camera" style="width:16px;height:16px"></i><span>${a.camera}</span></div>
      </div>
      ${a.status !== 'resolved' ? `<div class="alert-actions">
        ${a.status === 'active' ? '<button class="btn btn-outline btn-sm" onclick="ackAlert(' + a.id + ')">Acknowledge</button>' : ''}
        <button class="btn btn-outline btn-sm">View Details</button>
        <button class="btn btn-outline btn-sm ml-auto" onclick="resolveAlert(${a.id})"><i data-lucide="check-circle-2" style="width:12px;height:12px;margin-right:4px"></i>Resolve</button>
      </div>` : ''}
    </div>
  `).join('');

    if (window.lucide) lucide.createIcons();
}

function filterAlerts() {
    // Update severity filter
    const sevBtn = event.currentTarget;
    if (sevBtn.dataset.severity !== undefined) {
        sevBtn.closest('.btn-group').querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
        sevBtn.classList.add('active');
        currentSeverityFilter = sevBtn.dataset.severity;
    }
    // Update status filter
    if (sevBtn.dataset.status !== undefined) {
        sevBtn.closest('.btn-group').querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
        sevBtn.classList.add('active');
        currentStatusFilter = sevBtn.dataset.status;
    }
    renderAlerts();
}

function clearAlertFilters() {
    currentSeverityFilter = 'all';
    currentStatusFilter = 'all';
    const search = document.getElementById('alertSearch');
    if (search) search.value = '';
    document.querySelectorAll('[data-severity]').forEach(b => b.classList.toggle('active', b.dataset.severity === 'all'));
    document.querySelectorAll('[data-status]').forEach(b => b.classList.toggle('active', b.dataset.status === 'all'));
    renderAlerts();
}

function ackAlert(id) {
    const a = alertsData.find(x => x.id === id);
    if (a) { a.status = 'acknowledged'; renderAlerts(); }
}

function resolveAlert(id) {
    const a = alertsData.find(x => x.id === id);
    if (a) { a.status = 'resolved'; renderAlerts(); }
}

// ---- Camera Feed ----
const cameras = [
    { id: 'CAM-MM-01', name: 'Northern Entry', status: 'online' },
    { id: 'CAM-MM-02', name: 'Central Grassland', status: 'online' },
    { id: 'CAM-MM-03', name: 'Eastern Ridge', status: 'online' },
    { id: 'CAM-MM-04', name: 'Southern Waterhole', status: 'degraded' },
    { id: 'CAM-MM-05', name: 'Western Boundary', status: 'online' },
    { id: 'CAM-MM-06', name: 'Central Valley', status: 'online' },
    { id: 'CAM-MM-07', name: 'Eastern Forest', status: 'offline' },
    { id: 'CAM-MM-08', name: 'Northern Ridge', status: 'online' },
];

let selectedCamera = 0;
let cameraViewMode = 'single';

function initCameraSelector() {
    const sel = document.getElementById('cameraSelector');
    if (!sel) return;
    sel.innerHTML = cameras.map((c, i) => `
    <button class="camera-btn ${i === selectedCamera ? 'selected' : ''}" onclick="selectCamera(${i})">
      <p class="cam-id">${c.id}</p>
      <p class="cam-name">${c.name}</p>
      <div class="cam-dot ${c.status}"></div>
    </button>
  `).join('');
    renderFeed();
}

function selectCamera(idx) {
    selectedCamera = idx;
    document.querySelectorAll('.camera-btn').forEach((b, i) => b.classList.toggle('selected', i === idx));
    renderFeed();
}

function setCameraView(mode) {
    cameraViewMode = mode;
    document.getElementById('viewSingle')?.classList.toggle('active', mode === 'single');
    document.getElementById('viewGrid')?.classList.toggle('active', mode === 'grid');
    renderFeed();
}

function renderFeed() {
    const display = document.getElementById('feedDisplay');
    if (!display) return;

    if (cameraViewMode === 'single') {
        const cam = cameras[selectedCamera];
        display.innerHTML = renderCCTVFeed(cam, 'height:400px');
    } else {
        display.innerHTML = `<div class="grid grid-cols-2" style="gap:0.5rem">${cameras.filter(c => c.status !== 'offline').slice(0, 4).map(c => renderCCTVFeed(c, 'height:240px')).join('')}</div>`;
    }
    if (window.lucide) lucide.createIcons();
}

function renderCCTVFeed(cam, style) {
    const bboxes = cam.status === 'online' ? `
    <div class="yolo-bbox" style="left:25%;top:35%;width:120px;height:80px;border-color:var(--success)"><span class="yolo-bbox-label" style="background:var(--success)">Elephant 98%</span></div>
    <div class="yolo-bbox" style="left:60%;top:50%;width:80px;height:55px;border-color:var(--warning)"><span class="yolo-bbox-label" style="background:var(--warning)">Deer 87%</span></div>
  ` : '';

    return `
    <div class="cctv-feed" style="${style}">
      <div class="cctv-scan-line"></div>
      <div style="position:absolute;inset:0;background:linear-gradient(135deg,rgba(20,184,166,0.02) 0%,rgba(0,0,0,0.3) 100%)"></div>
      ${bboxes}
      <div class="cctv-feed-overlay">
        <div class="cctv-top-bar">
          <span class="live-indicator"><span class="pulse"></span> LIVE</span>
          <span class="rec-indicator">● REC</span>
        </div>
        <div class="cctv-bottom-bar">
          <span>${cam.id} — ${cam.name}</span>
          <span>1080p • 30fps</span>
        </div>
      </div>
    </div>`;
}

// ---- Heatmap ----
function initHeatmap() {
    const grid = document.getElementById('riskHeatmap');
    if (!grid) return;
    const zones = ['NC', 'ER', 'CA', 'SB', 'WP', 'NE', 'SE'];
    const hours = ['00', '04', '08', '12', '16', '20', '24'];

    // Header row
    grid.innerHTML = '<div></div>' + hours.map(h => `<div style="text-align:center;font-size:0.625rem;color:var(--muted-foreground)">${h}h</div>`).join('');

    zones.forEach(zone => {
        grid.innerHTML += `<div style="font-size:0.625rem;color:var(--muted-foreground);display:flex;align-items:center">${zone}</div>`;
        for (let i = 0; i < 7; i++) {
            const risk = Math.random();
            const level = risk > 0.8 ? 'critical' : risk > 0.6 ? 'high' : risk > 0.3 ? 'medium' : 'low';
            grid.innerHTML += `<div class="heatmap-cell ${level}">${Math.floor(risk * 10)}</div>`;
        }
    });
    grid.style.gridTemplateColumns = `40px repeat(7, 1fr)`;
}

// ---- Init ----
document.addEventListener('DOMContentLoaded', function () {
    renderAlerts();
    initCameraSelector();
    initHeatmap();

    // Search listener
    const search = document.getElementById('alertSearch');
    if (search) search.addEventListener('input', renderAlerts);
});
