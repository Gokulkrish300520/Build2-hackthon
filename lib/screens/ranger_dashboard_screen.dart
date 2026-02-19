import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import '../models/event_model.dart';
import '../services/socket_service.dart';
import 'dart:async';
import 'dart:math';

class RangerDashboardScreen extends StatefulWidget {
  const RangerDashboardScreen({super.key});

  @override
  State<RangerDashboardScreen> createState() =>
      _RangerDashboardScreenState();
}

class _RangerDashboardScreenState
    extends State<RangerDashboardScreen> {

  late SocketService socket;
  EventModel? latestEvent;
  StreamSubscription<Map<String, dynamic>>? _subscription;

  GoogleMapController? _mapController;

  Set<Circle> _circles = {};
  Set<Marker> _markers = {};

  bool _blink = true;
  Timer? _blinkTimer;

  // Simulated ranger base location
  final LatLng _rangerLocation = const LatLng(11.5550, 76.6200);

  double? _etaMinutes;

  @override
  void initState() {
    super.initState();

    socket = SocketService(
      serverIp: "127.0.0.1",
      nodeId: "RANGER_01",
    );

    socket.connect();

    // Blinking animation timer
    _blinkTimer = Timer.periodic(
      const Duration(milliseconds: 600),
      (timer) {
        if (!mounted) return;
        setState(() {
          _blink = !_blink;
        });
      },
    );

    _subscription = socket.messages.listen((event) {
      if (!mounted) return;

      if (event.containsKey("event_id")) {
        final parsedEvent = EventModel.fromJson(event);

        final LatLng alertLocation =
            LatLng(parsedEvent.lat, parsedEvent.lon);

        // Calculate ETA
        double distanceKm =
            _calculateDistance(_rangerLocation, alertLocation);

        double avgSpeedKmPerHour = 40; // patrol jeep avg speed
        double timeHours = distanceKm / avgSpeedKmPerHour;
        double eta = timeHours * 60;

        setState(() {
          latestEvent = parsedEvent;
          _etaMinutes = eta;

          _circles = {
            Circle(
              circleId: const CircleId("alert_zone"),
              center: alertLocation,
              radius: parsedEvent.radiusM.toDouble(),
              fillColor: Colors.red.withOpacity(0.3),
              strokeColor: Colors.red,
              strokeWidth: 2,
            )
          };

          _markers = {
            // Blinking alert marker
            Marker(
              markerId: const MarkerId("alert_marker"),
              position: alertLocation,
              icon: BitmapDescriptor.defaultMarkerWithHue(
                _blink
                    ? BitmapDescriptor.hueRed
                    : BitmapDescriptor.hueOrange,
              ),
            ),

            // Ranger base marker
            Marker(
              markerId: const MarkerId("ranger_marker"),
              position: _rangerLocation,
              icon: BitmapDescriptor.defaultMarkerWithHue(
                  BitmapDescriptor.hueAzure),
            ),
          };
        });

        _mapController?.animateCamera(
          CameraUpdate.newLatLngZoom(alertLocation, 15),
        );
      }
    });
  }

  // Haversine distance formula
  double _calculateDistance(LatLng start, LatLng end) {
    const double earthRadius = 6371; // km

    double dLat =
        (end.latitude - start.latitude) * pi / 180;
    double dLon =
        (end.longitude - start.longitude) * pi / 180;

    double a =
        sin(dLat / 2) * sin(dLat / 2) +
            cos(start.latitude * pi / 180) *
                cos(end.latitude * pi / 180) *
                sin(dLon / 2) *
                sin(dLon / 2);

    double c = 2 * atan2(sqrt(a), sqrt(1 - a));

    return earthRadius * c;
  }

  @override
  void dispose() {
    _blinkTimer?.cancel();
    _subscription?.cancel();
    socket.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Ranger Dashboard")),
      body: Stack(
        children: [
          GoogleMap(
            initialCameraPosition: const CameraPosition(
              target: LatLng(11.5590, 76.6298),
              zoom: 13,
            ),
            mapType: MapType.hybrid, // Better for demo
            circles: _circles,
            markers: _markers,
            onMapCreated: (controller) {
              _mapController = controller;
            },
          ),

          if (latestEvent != null)
            Positioned(
              top: 40,
              left: 20,
              right: 20,
              child: Card(
                color: Colors.red.shade700,
                elevation: 6,
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Column(
                    children: [
                      const Text(
                        "🚨 POACHING ALERT DETECTED",
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 6),
                      Text("Risk Level: ${latestEvent!.riskLevel}"),
                      Text("Confidence: ${latestEvent!.confidence}%"),
                      Text("Alert Radius: ${latestEvent!.radiusM} m"),
                      if (_etaMinutes != null)
                        Text(
                          "Estimated Arrival: ${_etaMinutes!.toStringAsFixed(1)} mins",
                          style: const TextStyle(
                              fontWeight: FontWeight.bold),
                        ),
                    ],
                  ),
                ),
              ),
            ),

          if (latestEvent == null)
            const Center(
              child: Text(
                "No Alerts",
                style: TextStyle(fontSize: 18),
              ),
            ),
        ],
      ),
    );
  }
}