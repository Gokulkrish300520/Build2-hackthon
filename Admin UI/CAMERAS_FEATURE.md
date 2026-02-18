# CCTV & YOLO Detection System - Feature Documentation

## Overview
Added comprehensive CCTV camera management with real-time YOLO detection integration for the SentinelAI Wildlife Protection Dashboard.

## New Components

### 1. **Mudumalai Map** (`components/dashboard/mudumalai-map.tsx`)
Interactive map visualization of the Mudumalai Tiger Reserve with:
- **Camera Deployment Scatter**: 8 camera locations plotted on the reserve map
- **Status Indicators**: Color-coded dots (green=online, yellow=degraded, red=offline)
- **Live Pulsing Animation**: Online cameras have animated pulse effect
- **Camera Statistics**: Signal strength, battery level, recent detections for each camera
- **Interactive Selection**: Click cameras to view detailed information
- **Legend**: Color legend for status indicators
- **Satellite Background**: Forest reserve topographical map background image

**Key Features:**
- Real-time status monitoring
- Hover tooltips with camera names
- Scrollable camera list with detailed metrics
- Stats summary (online count, total detections)

### 2. **CCTV Feed Viewer** (`components/dashboard/cctv-feed.tsx`)
Live camera feed display with YOLO detection overlay:
- **Live Feed UI**: Realistic camera feed interface with recording indicator
- **YOLO Bounding Boxes**: 
  - Color-coded detection boxes (red=elephant, orange=tiger, darkred=person, green=vehicle)
  - Confidence scores displayed on each detection
  - Interactive selection of detections
  - Corner markers for better visibility
  - Animated scanning line effect
- **Detection Controls**:
  - Play/Pause button
  - Mute audio
  - Fullscreen mode
  - Detection list sidebar
- **Status Indicators**:
  - LIVE indicator (green pulsing)
  - REC indicator (red pulsing)
  - Camera info bar with FPS and resolution
- **Detection History**: Scrollable list of detected objects with timestamps and confidence scores

**Mock Data Included:**
- Sample detections: elephants (98%), tigers (94%), persons (89%)
- Dynamic detection highlighting on bounding boxes

### 3. **YOLO Detection Statistics** (`components/dashboard/yolo-detection-stats.tsx`)
Comprehensive analytics dashboard for model detections:
- **Detection Timeline Chart**: 24-hour detection history line chart
  - Multiple detection classes tracked over time
  - Hover tooltips for detailed values
- **Detection Distribution Pie Chart**: Breakdown of detection types
- **Model Confidence Bar Chart**: Average confidence scores by detection class
- **Recent Detections Table**:
  - Detection ID, class, confidence level
  - Camera source
  - Threat level indicators
  - Timestamp
  - Visual confidence progress bars

**Analytics Included:**
- 24-hour detection trends
- Class-wise confidence metrics
- Threat level classifications
- Detailed detection history

### 4. **Cameras Page** (`app/cameras/page.tsx`)
Main hub for all camera and YOLO detection features:
- **Three-Tab Interface**:
  1. **Deployment Map Tab**: Full Mudumalai map with camera scatter
  2. **Live Feeds Tab**: CCTV feed viewing with camera selector
  3. **Detection Analytics Tab**: YOLO statistics and analytics

- **Camera Selector**:
  - 8 active cameras with status indicators
  - Single/Grid view toggle
  - Quick camera switching
  
- **Statistics Summary**:
  - Total cameras online
  - Today's detections count
  - Model accuracy percentage
  - Active alerts count

## Navigation Integration

Updated sidebar (`components/dashboard/sidebar.tsx`):
- Added "Cameras" menu item (with video icon)
- Positioned between "Alerts" and "Patrols"
- Full navigation integration

## Dashboard Updates

Updated Overview page (`app/page.tsx`):
- Added "YOLO Detections" metric card
- Shows 24-hour detection count
- Displays trend indicator

## Assets

Generated background image (`public/mudumalai-reserve.jpg`):
- Satellite/aerial view of Mudumalai Tiger Reserve
- Topographical styling
- Forest zones and terrain visualization
- Professional GIS map aesthetic

## Key Technical Features

### Color Coding System
- **Elephants**: Red (#ef4444)
- **Tigers**: Orange (#f97316)
- **Persons**: Dark Red (#dc2626)
- **Vehicles**: Green (#22c55e)

### Detection Classes
- Elephant (wildlife protection focus)
- Tiger (endangered species)
- Person (unauthorized entry detection)
- Vehicle (poaching activity indicator)

### Status Indicators
- **Online**: Green + pulsing animation
- **Degraded**: Yellow (warning)
- **Offline**: Red (critical)

## Mock Data Structure

### Camera Nodes
```typescript
interface CameraLocation {
  id: string;
  name: string;
  lat: number;
  lng: number;
  status: 'online' | 'offline' | 'degraded';
  signalStrength: number;
  battery: number;
  recentDetections: number;
}
```

### YOLO Detections
```typescript
interface YOLODetection {
  id: string;
  class: string;
  confidence: number;
  x: number;
  y: number;
  width: number;
  height: number;
  timestamp: string;
}
```

## API Integration Points

Ready for real data integration:
1. **Camera Status API**: Replace mock camera data with real node status
2. **YOLO Detection Stream**: Connect WebSocket for real-time detections
3. **Camera Feed URLs**: Integrate actual RTSP/MJPEG streams
4. **Detection History API**: Replace mock detection history with database

## Performance Considerations

- Bounding boxes rendered via SVG for performance
- Camera list scrollable with max-height constraints
- Chart data limited to reasonable samples
- Fullscreen mode for detailed inspection
- Lazy loading ready for multiple feeds

## Future Enhancements

1. Real RTSP/MJPEG stream integration
2. WebSocket support for real-time detections
3. Video recording and playback
4. Advanced filtering (confidence thresholds, detection type filters)
5. Threat level calculation algorithms
6. Integration with ranger dispatch system
7. Detection heatmaps over time
8. Model performance metrics
9. Custom YOLO model upload support
10. Historical detection analysis and patterns
