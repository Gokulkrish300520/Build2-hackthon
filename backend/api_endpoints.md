# API Endpoints Reference

## Intelligence

- **GET /intelligence/trends**
  - Response: `trends[]` (id, generated_at, trend_data)
- **GET /intelligence/recommendations**
  - Response: `recommendations[]` (id, generated_at, recommendations)
- **POST /intelligence/report**
  - Fields: summary, recommendations, trend_data
  - Response: success

## Network

- **GET /network/**
  - Response: `network_status[]` (id, camera_id, patrol_id, status, last_checked, issues)

## Patrols

- **GET /patrols/**
  - Response: `patrols[]` (id, team_name, route, status, start_time, end_time)
- **POST /patrols/report**
  - Fields: patrol_id, description, sightings
  - Response: success

## Cameras

- **GET /cameras/**
  - Response: `cameras[]` (id, name, location, status)
- **GET /cameras/{camera_id}/feeds**
  - Response: `feeds[]` (id, filename, upload_time, status)
- **GET /cameras/{camera_id}/detections**
  - Response: `detections[]` (frame_number, timestamp, type, bbox, species, confidence, is_poacher, risk_score)

## Alerts

- **GET /alerts/**
  - Query: severity, status, search
  - Response: `alerts[]` (id, title, location, camera_id, severity, status, timestamp, description)
- **POST /alerts/acknowledge**
  - Fields: alert_id
  - Response: success
- **POST /alerts/resolve**
  - Fields: alert_id
  - Response: success
- **POST /alerts/export**
  - Response: success, message
- **GET /alerts/high_risk/**
  - Response: `high_risk_alerts[]` (frame_id, bbox, risk_score, is_poacher)

## Videos

- **GET /videos/{video_id}/detections/**
  - Response: `detections[]` (frame_number, timestamp, type, bbox, species, confidence, is_poacher, risk_score)

## Poaching Events

- **GET /poaching_events/**
  - Response: `poaching_events[]` (id, human_id, start_time, end_time, location, species_affected, description)

## Stats

- **GET /stats/species/**
  - Response: `species_stats[]` (species, count)
- **GET /stats/poaching_trends/**
  - Response: `poaching_trends` (hour: count)
