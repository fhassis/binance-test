import 'dart:convert';
import 'dart:io';
import 'package:binance_dart/parsers.dart';
import 'package:crypto/crypto.dart';

import 'typings.dart';

class BinanceClient {
  late final Hmac _hmac;
  late final String _apiKey;
  late final String _baseUrl;
  final _client = HttpClient();

  BinanceClient(
      {required String apiKey,
      required String apiSecret,
      bool testnet = false}) {
    _baseUrl = testnet ? 'testnet.binance.vision' : 'api.binance.com';
    _hmac = Hmac(sha256, utf8.encode(apiSecret));
    _apiKey = apiKey;
  }

  /// Closes the inner http client.
  void close() {
    _client.close();
  }

  /// Adds the signature parameter to a given map of parameters
  Map<String, String> _addSignature(Map<String, String>? params) {
    // initializes params map if null
    params ??= <String, String>{};

    // adds timestamp information required for signed endpoints
    params['timestamp'] =
        DateTime.now().toUtc().millisecondsSinceEpoch.toString();

    // // generate the query string based on the original query params
    final queryString = utf8.encode(Uri(queryParameters: params).query);

    // add signature to the query parameters
    params['signature'] = _hmac.convert(queryString).toString();

    return params;
  }

  /// Sends the HTTP request to Binance server and handles the response.
  Future<dynamic> _sendRequest(String method, String path,
      {Map<String, String>? params, bool signed = false}) async {
    // adds signature if required
    if (signed) {
      params = _addSignature(params);
    }

    // creates the http request
    final request =
        await _client.openUrl(method, Uri.https(_baseUrl, path, params));
    request.headers.set('X-MBX-APIKEY', _apiKey);

    // sends the http request
    final response = await request.close();

    // handles the http response
    if (response.statusCode == 200) {
      final data = await response.transform(utf8.decoder).join();
      return jsonDecode(data);
    } else {
      throw HttpException(
          "HTTP status ${response.statusCode}: ${response.reasonPhrase}");
    }
  }

  /// Fetches the server time data.
  Future<int> fetchServerTime() async {
    var json = await _sendRequest('GET', '/api/v3/time');
    return parseServerTime(json);
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
