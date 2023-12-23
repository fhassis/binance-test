import 'dart:convert';
import 'package:binance_dart/parsers.dart';
import 'package:dio/dio.dart';
import 'package:crypto/crypto.dart';

import 'typings.dart';

class BinanceClient {
  late Dio _dio;
  late Hmac _hmac;

  BinanceClient(
      {required String apiKey,
      required String apiSecret,
      bool testnet = false}) {
    _dio = Dio(BaseOptions(
      baseUrl: testnet
          ? 'https://testnet.binance.vision'
          : 'https://api.binance.com',
      headers: {'X-MBX-APIKEY': apiKey},
    ));
    _hmac = Hmac(sha256, utf8.encode(apiSecret));
  }

  /// Closes the inner http client.
  void close() {
    _dio.close();
  }

  /// Adds the signature parameter to a given map of parameters
  Map<String, String> _addSignature(Map<String, String>? params) {
    // initializes params map if null
    params ??= <String, String>{};

    // adds timestamp information required for signed endpoints
    params['timestamp'] =
        DateTime.now().toUtc().millisecondsSinceEpoch.toString();

    // generate the query string based on the original query params
    var list = [];
    params.forEach((key, value) => list.add('$key=$value'));
    var queryBytes = utf8.encode(list.join('&'));

    // add signature to the query parameters
    params['signature'] = _hmac.convert(queryBytes).toString();

    return params;
  }

  /// Sends the HTTP request to Binance server and handles the response.
  Future<dynamic> _sendRequest(String method, String path,
      {Map<String, String>? params, bool signed = false}) async {
    // adds signature if required
    if (signed) {
      params = _addSignature(params);
    }

    // performs http request
    try {
      var response = await _dio.request(
        path,
        options: Options(method: method),
        queryParameters: params,
      );
      return response.data;
    } on DioError catch (e) {
      if (e.response?.data == "") {
        throw Exception(e.error);
      } else {
        throw Exception(
            'Error ${e.response?.data["code"]}: ${e.response?.data["msg"]}');
      }
    }
  }

  /// Fetches the server time data.
  Future<Json> fetchServerTime() async {
    return await _sendRequest('GET', '/api/v3/time');
  }

  /// Fetches the account info data.
  Future<Json> fetchAccountInfo() async {
    return await _sendRequest('GET', '/api/v3/account', signed: true);
  }

  /// Fetches the exchange info data.
  Future<Json> fetchExchangeInfo() async {
    return await _sendRequest('GET', '/api/v3/exchangeInfo');
  }

  /// Fetches a listenKey for account info websockets.
  Future<String> fetchListenKey() async {
    var json = await _sendRequest('POST', '/api/v3/userDataStream');
    return parseListenKey(json);
  }

  /// Fetches a candles list.
  Future<List<dynamic>> fetchCandles(String symbol, Timeframe tf,
      {DateTime? startTime, DateTime? endTime, int? limit}) async {
    var params = {'symbol': symbol, 'interval': tf.toBinanceString()};
    if (startTime != null) {
      params['startTime'] = startTime.millisecondsSinceEpoch.toString();
    }
    if (endTime != null) {
      params['endTime'] = endTime.millisecondsSinceEpoch.toString();
    }
    if (limit != null) {
      params['limit'] = limit.toString();
    }
    return await _sendRequest('GET', '/api/v3/klines', params: params);
  }

  /// Fetches user trades.
  Future<dynamic> fetchTrades(String symbol,
      {int? orderId,
      DateTime? startTime,
      DateTime? endTime,
      int? fromId,
      int? limit}) async {
    var params = {'symbol': symbol};
    if (orderId != null) {
      params['orderId'] = orderId.toString();
    }
    if (startTime != null) {
      params['startTime'] = startTime.millisecondsSinceEpoch.toString();
    }
    if (endTime != null) {
      params['endTime'] = endTime.millisecondsSinceEpoch.toString();
    }
    if (fromId != null) {
      params['fromId'] = fromId.toString();
    }
    if (limit != null) {
      params['limit'] = limit.toString();
    }
    return await _sendRequest('GET', '/api/v3/myTrades',
        params: params, signed: true);
  }

  /// Fetches deposits history.
  Future<dynamic> fetchDepositHistory(
      {String? asset,
      DateTime? startTime,
      DateTime? endTime,
      int? offset,
      int? limit}) async {
    Map<String, String> params = {};
    if (asset != null) {
      params['coin'] = asset;
    }
    if (startTime != null) {
      params['startTime'] = startTime.millisecondsSinceEpoch.toString();
    }
    if (endTime != null) {
      params['endTime'] = endTime.millisecondsSinceEpoch.toString();
    }
    if (offset != null) {
      params['offset'] = offset.toString();
    }
    if (limit != null) {
      params['limit'] = limit.toString();
    }
    return await _sendRequest('GET', '/sapi/v1/capital/deposit/hisrec',
        params: params, signed: true);
  }

  /// Fetches withdrawals history.
  Future<dynamic> fetchWithdrawHistory(
      {String? asset,
      DateTime? startTime,
      DateTime? endTime,
      int? offset,
      int? limit}) async {
    Map<String, String> params = {};
    if (asset != null) {
      params['coin'] = asset;
    }
    if (startTime != null) {
      params['startTime'] = startTime.millisecondsSinceEpoch.toString();
    }
    if (endTime != null) {
      params['endTime'] = endTime.millisecondsSinceEpoch.toString();
    }
    if (offset != null) {
      params['offset'] = offset.toString();
    }
    if (limit != null) {
      params['limit'] = limit.toString();
    }
    return await _sendRequest('GET', '/sapi/v1/capital/withdraw/history',
        params: params, signed: true);
  }
}
