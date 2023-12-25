import 'package:binance_dart/typings.dart';

int parseServerTime(Json json) {
  return json['serverTime'];
}

String parseListenKey(Json json) {
  return json['listenKey'];
}
