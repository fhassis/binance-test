import 'package:test/test.dart';
import 'package:binance_dart/src/spot_client.dart';
import 'dart:io' show Platform;

void main() {
  group('BinanceSpotClient', () {
    // access the system environment variables
    var environ = Platform.environment;

    // check if environment variables exist
    assert(environ['BINANCE_API_KEY'] != null);
    assert(environ['BINANCE_API_SECRET'] != null);
    assert(environ['BINANCE_TESTNET'] != null);

    // create the binance spot client
    final client = BinanceSpotClient(
      apiKey: environ['BINANCE_API_KEY']!,
      apiSecret: environ['BINANCE_API_SECRET']!,
      isTestnet: bool.parse(environ['BINANCE_TESTNET']!),
    );

    test('fetchServerTime returns data', () async {
      var data = await client.fetchServerTime();
      expect(data.containsKey("serverTime"), true);
    });

    test('fetchAccountInfo returns data', () async {
      var data = await client.fetchAccountInfo();
      expect(data.containsKey("makerCommission"), true);
    });

    test('createListenKey returns data', () async {
      var data = await client.createListenKey();
      expect(data.containsKey("listenKey"), true);
    });
  });
}
