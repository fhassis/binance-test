class BinanceSpotClient : BinanceBaseClient
{
    public BinanceSpotClient(string apiKey, string apiSecret, bool isTestnet = false) :
        base(apiKey, apiSecret, isTestnet ? "https://testnet.binance.vision" : "https://api.binance.com")
    { }

    public async Task<BinanceServerTime> FetchServerTime()
    {
        return await SendRequest<BinanceServerTime>(HttpMethod.Get, "/api/v3/time", null);
    }

    public async Task<BinanceAccountInfo> FetchAccountInfo()
    {
        return await SendRequest<BinanceAccountInfo>(HttpMethod.Get, "/api/v3/account", null, true);
    }

    public async Task<List<BinanceTrade>> FetchTrades(string symbol, long? startTime, long? endTime, long? fromId)
    {
        var data = new Dictionary<string, string>() { { "symbol", symbol } };
        if (startTime is not null)
        {
            data.Add("startTime", startTime.ToString()!);
        }
        if (endTime is not null)
        {
            data.Add("endTime", endTime.ToString()!);
        }
        if (fromId is not null)
        {
            data.Add("fromId", fromId.ToString()!);
        }
        return await SendRequest<List<BinanceTrade>>(HttpMethod.Get, "/api/v3/myTrades", data, true);
    }
}