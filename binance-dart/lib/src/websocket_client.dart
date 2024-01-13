import 'dart:io';
import 'dart:convert';

// TODO: replace print statements by dart logging

class BinanceWebsocketClient {
  final Set<String> _subscriptions = {};
  late final String _baseUrl;
  WebSocket? _ws;

  BinanceWebsocketClient({required String baseUrl}) {
    _baseUrl = baseUrl;
  }

  String _getSubscriptionMessage({
    required List<String> topics,
    required bool isSubscribe,
  }) {
    return jsonEncode({
      "method": isSubscribe ? 'SUBSCRIBE' : 'UNSUBSCRIBE',
      "params": topics,
      "id": DateTime.now().toUtc().millisecondsSinceEpoch,
    });
  }

  /// Sends a subscribe / unsubscribe message over websocket.
  _sendSubscription(String payload) {
    if (_ws?.readyState == WebSocket.open) {
      _ws!.add(payload);
    } else {
      print('WARNING: Message not sent due to disconnection: $payload');
    }
  }

  /// Stream of data from the websocket.
  Stream<Map<String, dynamic>> stream() async* {
    try {
      print('INFO: connecting to $_baseUrl');
      _ws = await WebSocket.connect(_baseUrl);

      // subscribes to the topics topics
      if (_subscriptions.isNotEmpty) {
        _sendSubscription(_getSubscriptionMessage(
          topics: _subscriptions.toList(),
          isSubscribe: true,
        ));
      }

      // receives messages
      print('DEBUG: waiting for messages');
      await for (var message in _ws!) {
        try {
          yield jsonDecode(message) as Map<String, dynamic>;
        } on FormatException catch (e) {
          print('ERROR: invalid json message: $message - $e');
        }
      }
      // if here, websocket was disconnected
      print('INFO: websocket disconnected.');
      _ws = null;
    } on SocketException catch (e) {
      // log an error message
      print(
          'ERROR: ${e.osError?.errorCode} | ${e.osError?.message.trimRight()}');

      // removes reference
      _ws = null;
    } catch (e) {
      print('ERROR: error in websocket: $e');
    }
  }

  /// Subscribes to User Data stream.
  void subscribeToUserData(String listenKey) {
    // add item to the subscription list
    _subscriptions.add(listenKey);

    // form the payload message
    final message = _getSubscriptionMessage(
      topics: [listenKey],
      isSubscribe: true,
    );

    // send message over websocket
    _sendSubscription(message);
  }

  /// Subscribes to User Data stream.
  void unsubscribeFromUserData(String listenKey) {
    // remove item from the subscription list
    _subscriptions.remove(listenKey);

    // form the payload message
    final message = _getSubscriptionMessage(
      topics: [listenKey],
      isSubscribe: false,
    );

    // send message over websocket
    _sendSubscription(message);
  }
}
