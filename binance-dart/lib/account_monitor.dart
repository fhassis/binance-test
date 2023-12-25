import 'package:binance_dart/api_client.dart';
import 'package:binance_dart/typings.dart';
import 'package:binance_dart/websocket_handler.dart';

/// Monitors binance user account changes.
class AccountMonitor {
  final BinanceClient _client;
  late WebsocketHandler _wsHandler;

  AccountMonitor(this._client);

  /// Initializes the AccountMonitor object.
  start() async {
    // gets url from binance client
    var listenKey = await _client.fetchListenKey();

    // creates the websocket handler
    _wsHandler =
        WebsocketHandler('AccountMonitor', _handleWsData, useTestnet: true)
          ..subscribeToUserData(listenKey)
          ..start();

    // var topics = ['btcusdt@kline_1m', 'btcusdt@miniTicker'];
    var topics = ['btcusdt@kline_1m', 'btcusdt@kline_1d'];

    // subscribes to the topics
    Future.delayed(Duration(seconds: 5), () {
      print('Subscribing to topics: ${topics.toString()}');
      _wsHandler.sendSubscription(topics, true);
    });

    // unsubscribes to the topics
    Future.delayed(Duration(seconds: 15), () {
      print('Unsubscribing to topics: ${topics.toString()}');
      _wsHandler.sendSubscription(topics, false);
    });
  }

  /// Disposes inner resources.
  dispose() {
    _wsHandler.dispose();
  }

  // Handles incomming data over the websocket.
  _handleWsData(Json json) {
    print(json);
  }
}
