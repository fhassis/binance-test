import 'package:binance_dart/account_monitor.dart';
import 'package:binance_dart/api_client.dart';
import 'dart:io' show Platform;

import 'package:binance_dart/typings.dart';

void main() async {
  // get api key and secret from environment variables
  Map<String, String> envVars = Platform.environment;

  // create the binance spot client
  var binance = BinanceClient(
    apiKey: envVars['BINANCE_API_KEY'] as String,
    apiSecret: envVars['BINANCE_API_SECRET'] as String,
    testnet: envVars['BINANCE_TESTNET'] == '1',
  );

  // print(await binance.fetchServerTime());
  // print(await binance.fetchAccountInfo());
  // print(await binance.fetchListenKey());
  // print(await binance.fetchExchangeInfo());
  // print(await binance.fetchCandles('BTCUSDT', Timeframe.d1));
  // print(await binance.fetchMyTrades('BTCUSDT'));
  // print(await binance.fetchDepositHistory());
  // print(await binance.fetchWithdrawHistory());

  // // close the binance client
  binance.close();

  // var accountMonitor = AccountMonitor(binance);
  // accountMonitor.start();
}
