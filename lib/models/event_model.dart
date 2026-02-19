class EventModel {
  final int eventId;
  final int eventType;
  final int riskLevel;
  final double lat;
  final double lon;
  final int radiusM;
  final int confidence;
  final int timestamp;
  final int ttl;

  EventModel({
    required this.eventId,
    required this.eventType,
    required this.riskLevel,
    required this.lat,
    required this.lon,
    required this.radiusM,
    required this.confidence,
    required this.timestamp,
    required this.ttl,
  });

  factory EventModel.fromJson(Map<String, dynamic> json) {
  double parseDouble(dynamic v) =>
      v is num ? v.toDouble() : double.tryParse(v.toString()) ?? 0.0;

  int parseInt(dynamic v) =>
      v is num ? v.toInt() : int.tryParse(v.toString()) ?? 0;

  return EventModel(
    eventId: parseInt(json['event_id']),
    eventType: parseInt(json['event_type']),
    riskLevel: parseInt(json['risk_level']),
    lat: parseDouble(json['lat']),
    lon: parseDouble(json['lon']),
    radiusM: parseInt(json['radius_m']),
    confidence: parseInt(json['confidence']),
    timestamp: parseInt(json['timestamp']),
    ttl: parseInt(json['ttl']),
  );
}
}