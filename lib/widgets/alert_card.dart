import 'package:flutter/material.dart';
import '../models/event_model.dart';

class AlertCard extends StatelessWidget {
  final EventModel event;

  const AlertCard({super.key, required this.event});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: event.riskLevel == 4
          ? Colors.red
          : Colors.orange,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text("Event ID: ${event.eventId}"),
            Text("Risk Level: ${event.riskLevel}"),
            Text("Radius: ${event.radiusM} m"),
          ],
        ),
      ),
    );
  }
}