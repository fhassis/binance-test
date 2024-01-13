import 'package:binance_dart/src/http_client.dart';
import 'package:binance_dart/src/websocket_client.dart';

class BinanceSpotClient {
  late final BinanceHttpClient _httpClient;
  late final BinanceWebsocketClient _wsClient;

  BinanceSpotClient({required apiKey, required apiSecret, isTestnet = false}) {
    _httpClient = BinanceHttpClient(
      apiKey: apiKey,
      apiSecret: apiSecret,
      baseUrl: isTestnet ? 'testnet.binance.vision' : 'api.binance.com',
    );
    _wsClient = BinanceWebsocketClient(
      baseUrl: isTestnet
          ? 'wss://testnet.binance.vision/stream'
          : 'wss://stream.binance.com:9443/stream',
    );
  }

  /// Fetches the server time.
  Future<Map<String, dynamic>> fetchServerTime() async {
    return await _httpClient.sendRequest(
      method: 'GET',
      path: '/api/v3/time',
    ) as Map<String, dynamic>;
  }

  /// Fetches the user account information.
  Future<Map<String, dynamic>> fetchAccountInfo() async {
    return await _httpClient.sendRequest(
      method: 'GET',
      path: '/api/v3/account',
      isSigned: true,
    );
  }

  /// Creates a listen key to be used in user data streams.
  Future<Map<String, dynamic>> createListenKey() async {
    return await _httpClient.sendRequest(
      method: 'POST',
      path: '/api/v3/userDataStream',
    );
  }

  Stream<Map<String, dynamic>> userDataStream() async* {
    // creates the listenKey
    final rawData = await createListenKey();
    final listenKey = rawData['listenKey'];

    // subscribes to user data
    _wsClient.subscribeToUserData(listenKey);

    // keeps receiving user data stream
    await for (var data in _wsClient.stream()) {
      // TODO: parse stream data before yield
      yield data;
    }

    // TODO: create renew task here
  }
}
