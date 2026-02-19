import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

class SocketService {
  WebSocketChannel? _channel;

  final String serverIp;
  final String nodeId;

  SocketService({required this.serverIp, required this.nodeId});

  void connect() {
    final uri = Uri.parse("ws://$serverIp:8000/ws/$nodeId");
    _channel = WebSocketChannel.connect(uri);
  }

  void sendHeartbeat(int battery) {
    final message = {
      "type": "heartbeat",
      "node_id": nodeId,
      "battery": battery
    };
    _channel?.sink.add(jsonEncode(message));
  }

  void sendEvent(Map<String, dynamic> event) {
  print("EVENT TYPE: ${event.runtimeType}");
  print(event);

  event["type"] = "event";
  _channel?.sink.add(jsonEncode(event));
}

  Stream<Map<String, dynamic>> get messages {
    return _channel!.stream.map((data) {
      return jsonDecode(data);
    });
  }

  void dispose() {
    _channel?.sink.close();
  }
}