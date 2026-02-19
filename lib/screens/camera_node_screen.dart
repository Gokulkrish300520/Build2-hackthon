import 'dart:async';
import 'package:flutter/material.dart';
import '../services/socket_service.dart';

class CameraNodeScreen extends StatefulWidget {
  const CameraNodeScreen({super.key});

  @override
  State<CameraNodeScreen> createState() => _CameraNodeScreenState();
}

class _CameraNodeScreenState extends State<CameraNodeScreen> {
  late SocketService socket;

  @override
  void initState() {
    super.initState();
    socket = SocketService(
      serverIp: "127.0.0.1", // CHANGE THIS
      nodeId: "CAM_01",
    );
    socket.connect();

    Timer.periodic(const Duration(seconds: 30), (_) {
      socket.sendHeartbeat(80);
    });
  }

  void triggerEvent() {
    final Map<String, dynamic> event = {
      "event_id": DateTime.now().millisecondsSinceEpoch,
      "event_type": 4,
      "risk_level": 4,
      "lat": 11.5432,
      "lon": 76.6352,
      "radius_m": 500,
      "confidence": 90,
      "timestamp":
          DateTime.now().millisecondsSinceEpoch ~/ 1000,
      "ttl": 4
    };

    socket.sendEvent(event);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Camera Node")),
      body: Center(
        child: ElevatedButton(
          onPressed: triggerEvent,
          child: const Text("Trigger Critical Event"),
        ),
      ),
    );
  }
}