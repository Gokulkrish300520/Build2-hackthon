import pytest
from fastapi.testclient import TestClient
from .app import app

client = TestClient(app)

def test_alerts():
    response = client.get('/alerts/')
    assert response.status_code == 200
    assert 'alerts' in response.json()

def test_cameras():
    response = client.get('/cameras/')
    assert response.status_code == 200
    assert 'cameras' in response.json()

def test_patrols():
    response = client.get('/patrols/')
    assert response.status_code == 200
    assert 'patrols' in response.json()

def test_network():
    response = client.get('/network/')
    assert response.status_code == 200
    assert 'network_status' in response.json()

def test_intelligence_trends():
    response = client.get('/intelligence/trends')
    assert response.status_code == 200
    assert 'trends' in response.json()

def test_intelligence_recommendations():
    response = client.get('/intelligence/recommendations')
    assert response.status_code == 200
    assert 'recommendations' in response.json()
