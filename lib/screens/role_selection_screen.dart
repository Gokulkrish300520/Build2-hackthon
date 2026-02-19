import 'package:flutter/material.dart';
import 'camera_node_screen.dart';
import 'ranger_dashboard_screen.dart';
import 'mesh_visualization_screen.dart';

class RoleSelectionScreen extends StatelessWidget {
  const RoleSelectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Select Role")),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          _button(context, "Camera Node", const CameraNodeScreen()),
          _button(context, "Ranger Device", const RangerDashboardScreen()),
          _button(context, "Mesh Monitor", const MeshVisualizationScreen()),
        ],
      ),
    );
  }

  Widget _button(BuildContext context, String text, Widget screen) {
    return Padding(
      padding: const EdgeInsets.all(12),
      child: ElevatedButton(
        onPressed: () {
          Navigator.push(
              context, MaterialPageRoute(builder: (_) => screen));
        },
        child: Text(text),
      ),
    );
  }
}