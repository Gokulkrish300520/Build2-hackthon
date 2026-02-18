const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Set EJS as template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.get('/', (req, res) => {
  res.render('layout', { page: 'index', title: 'Dashboard', activePath: '/' });
});

app.get('/alerts', (req, res) => {
  res.render('layout', { page: 'alerts', title: 'Alerts Management', activePath: '/alerts' });
});

app.get('/cameras', (req, res) => {
  res.render('layout', { page: 'cameras', title: 'CCTV & Detection System', activePath: '/cameras' });
});

app.get('/patrols', (req, res) => {
  res.render('layout', { page: 'patrols', title: 'Active Patrols', activePath: '/patrols' });
});

app.get('/network', (req, res) => {
  res.render('layout', { page: 'network', title: 'Network Status', activePath: '/network' });
});

app.get('/intelligence', (req, res) => {
  res.render('layout', { page: 'intelligence', title: 'Predictive Intelligence', activePath: '/intelligence' });
});

app.listen(PORT, () => {
  console.log(`SentinelAI server running at http://localhost:${PORT}`);
});
