import 'dart:io';
import 'dart:convert';

class WebsocketHandler {
  final String _taskName;
  final void Function(Map<String, dynamic>) _handleData;
  Set<String> _subscriptions = Set<String>();

  final int _reconnectTime = 5;
  WebSocket? _ws;
  bool _keepConnected = true;
  late String _baseUrl;

  WebsocketHandler(this._taskName, this._handleData, {useTestnet = false}) {
    _baseUrl = useTestnet
        ? 'wss://testnet.binance.vision/ws'
        : 'wss://stream.binance.com:9443/ws';
  }

  /// Starts the WebsocketHandler object.
  Future<void> start() async {
    while (_keepConnected) {
      try {
        // connects to websocket server
        print('$_taskName: connecting to $_baseUrl');
        _ws = await WebSocket.connect(_baseUrl);

        // subcribes to the subscriptions topics
        sendSubscription(_subscriptions.toList(), true);

        // receives messages
        print('$_taskName: waiting for messages');
        await for (var message in _ws!) {
          // converts the message to json
          var json = jsonDecode(message);

          // pass the message to the callback handler
          _handleData(json);
        }

        // if here, websocket was disconnected
        print('$_taskName: disconnected');
        _ws = null;
      } on SocketException catch (e) {
        // log an error message
        print(
            '$_taskName: Error ${e.osError?.errorCode} | ${e.osError?.message.trimRight()}');

        // removes reference
        _ws = null;

        // waits some time before retrying
        print('$_taskName: reconnecting in $_reconnectTime s');
        await Future.delayed(Duration(seconds: _reconnectTime));
      }
    }
  }

  // Disposes the WebsocketHandler resources.
  void dispose() {
    print('$_taskName: disposing resources');
    _keepConnected = false;
    _ws?.close();
  }

  /// Sends a subscribe / unsubscribe message over websocket.
  sendSubscription(List<String> streams, bool isSubscribe) {
    if (_ws != null && _ws!.readyState == WebSocket.open) {
      var payload = jsonEncode({
        "method": isSubscribe ? 'SUBSCRIBE' : 'UNSUBSCRIBE',
        "params": streams,
        "id": DateTime.now().toUtc().millisecondsSinceEpoch,
      });
      _ws!.add(payload);
    } else {
      print('$_taskName: ERROR: unable to send message over websocket');
    }
  }

  /// Subscribes to User Data stream.
  subscribeToUserData(String listenKey) {
    // add item to the subscription list
    _subscriptions.add(listenKey);

    // send a live subscription in the websocket if connected
    if (_ws != null && _ws!.readyState == WebSocket.open) {
      sendSubscription([listenKey], true);
    }
  }

  // /// forms the url to connect to a Mini Ticker Stream.
  // void setMiniTickerUrl(List<String> symbols) {
  //   var streams = symbols.map((s) => s.toLowerCase() + '@miniTicker');
  //   var urlBuffer = StringBuffer(_baseUrl)
  //     ..write('/stream?streams=')
  //     ..writeAll(streams, '/');
  //   _url = urlBuffer.toString();
  // }

  // /// forms the url to connect to a all Mini Tickers Stream.
  // void setMiniTickerAllUrl() {
  //   _url = '$_baseUrl/ws/!miniTicker@arr';
  // }

  // /// forms the url to connect to account stream.
  // void setAccountUrl(String listenKey) {
  //   _url = '$_baseUrl/ws';
  //   // _url = '$_baseUrl/stream';
  // }
}
