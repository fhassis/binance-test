using System.Net.WebSockets;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

abstract class BinanceBaseClient
{
    private readonly HttpClient _http;
    private readonly HMACSHA256 _hmac;
    private readonly JsonSerializerOptions _serializerOptions;

    public BinanceBaseClient(string apiKey, string apiSecret, string url)
    {
        _http = new HttpClient
        {
            BaseAddress = new Uri(url)
        };
        _http.DefaultRequestHeaders.Add("X-MBX-APIKEY", apiKey);
        _hmac = new HMACSHA256(Encoding.UTF8.GetBytes(apiSecret));
        _serializerOptions = new JsonSerializerOptions
        {
            DictionaryKeyPolicy = JsonNamingPolicy.CamelCase,
            NumberHandling = JsonNumberHandling.AllowReadingFromString
        };
    }

    private string GenerateSignature(string queryString)
    {
        byte[] queryStringBytes = Encoding.UTF8.GetBytes(queryString);
        byte[] bytes = _hmac.ComputeHash(queryStringBytes);
        return BitConverter.ToString(bytes).Replace("-", "").ToLower();
    }

    private static string GetTimestamp()
    {
        return DateTimeOffset.UtcNow.ToUnixTimeMilliseconds().ToString();
    }

    private string? GenerateQueryString(Dictionary<string, string>? data, bool signed)
    {
        if (data is null)
        {
            if (signed is false)
            {
                return null;
            }
            data = new Dictionary<string, string>();
        }
        if (signed)
        {
            data.Add("timestamp", GetTimestamp());
        }
        var paramList = from item in data select $"{item.Key}={item.Value}";
        var queryParams = String.Join("&", paramList);
        if (signed)
        {
            queryParams += $"&signature={GenerateSignature(queryParams)}";
        }
        return queryParams;
    }

    protected async Task<T> SendRequest<T>(HttpMethod method, string endpoint, Dictionary<string, string>? data, bool signed = false)
    {
        var queryStr = GenerateQueryString(data, signed);
        var url = queryStr is null ? endpoint : $"{endpoint}?{queryStr}";
        var request = new HttpRequestMessage(method, url);
        var response = await _http.SendAsync(request);
        var json = await response.Content.ReadAsStringAsync();
        if (response.IsSuccessStatusCode)
        {
            var parsedObject = JsonSerializer.Deserialize<T>(json, _serializerOptions);
            if (parsedObject is null)
            {
                throw new Exception($"Unable to convert the following json:\n{json}");
            }
            else return parsedObject;
        }
        else
        {
            throw new Exception(json);
        }
    }
}