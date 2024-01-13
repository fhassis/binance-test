import 'dart:convert';
import 'dart:io';
import 'package:crypto/crypto.dart';

class BinanceHttpClient {
  late final Hmac _hmac;
  late final String _apiKey;
  late final String _baseUrl;
  final _http = HttpClient();

  BinanceHttpClient(
      {required String apiKey,
      required String apiSecret,
      required String baseUrl}) {
    _baseUrl = baseUrl;
    _hmac = Hmac(sha256, utf8.encode(apiSecret));
    _apiKey = apiKey;
  }

  /// Closes the inner http client.
  void close() {
    _http.close();
  }

  /// Sends the HTTP request to Binance server and handles the response.
  Future<dynamic> sendRequest(
      {required String method,
      required String path,
      Map<String, String>? params,
      bool isSigned = false}) async {
    // adds signature if it is a signed request
    if (isSigned) {
      params ??= <String, String>{};

      // adds timestamp information required for signed endpoints
      params['timestamp'] =
          DateTime.now().toUtc().millisecondsSinceEpoch.toString();

      // generate the query string based on the original query params
      final queryString = utf8.encode(Uri(queryParameters: params).query);

      // add signature to the query parameters
      params['signature'] = _hmac.convert(queryString).toString();
    }

    // creates the http request
    final request =
        await _http.openUrl(method, Uri.https(_baseUrl, path, params));
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
}
