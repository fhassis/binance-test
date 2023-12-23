
// reads api keys from environment variables
var apiKey = Environment.GetEnvironmentVariable("BINANCE_API_KEY");
var apiSecret = Environment.GetEnvironmentVariable("BINANCE_API_SECRET");
var isTestnet = Convert.ToBoolean(Environment.GetEnvironmentVariable("BINANCE_TESTNET"));

if (apiKey is null || apiSecret is null)
{
    throw new Exception("Binance API keys not defined");
}

// creates binance client
var client = new BinanceSpotClient(apiKey, apiSecret, isTestnet);

Console.WriteLine(await client.FetchServerTime());

Console.WriteLine(await client.FetchAccountInfo());

var trades = await client.FetchTrades("BTCUSDT", null, null, null);
foreach (var trade in trades)
{
    Console.WriteLine(trade);
}

var wsClient = new BinanceSpotWsKline(true);

var subscriptions = new List<(string symbol, string timeframe)> {
    ("BTCUSDT", "1d")
};
await foreach (var kline in wsClient.KlineStream(subscriptions))
{
    Console.WriteLine(kline);
}
