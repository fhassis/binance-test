import 'package:binance_dart/binance_dart.dart';
import 'dart:io' show Platform;

void main() async {
  // access the system environment variables
  var environ = Platform.environment;

  // create the binance spot client
  var binanceSpotClient = BinanceSpotClient(
    apiKey: environ['BINANCE_API_KEY']!,
    apiSecret: environ['BINANCE_API_SECRET']!,
    isTestnet: bool.parse(environ['BINANCE_TESTNET']!),
  );

  // use some rest endpoints
  print(await binanceSpotClient.fetchServerTime());
  print(await binanceSpotClient.fetchAccountInfo());

  // processes user data stream
  await for (var data in binanceSpotClient.userDataStream()) {
    print(data);
  }
}
