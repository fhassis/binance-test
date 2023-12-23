
class BinanceSpotWsKline : BinanceBaseWsClient
{
    public BinanceSpotWsKline(bool isTestnet) :
        base(isTestnet ? "wss://testnet.binance.vision" : "wss://stream.binance.com:9443")
    { }


    public async IAsyncEnumerable<BinanceCandleStream> KlineStream(List<(string symbol, string timeframe)> items)
    {
        var subscriptions = from item in items select $"{item.symbol.ToLower()}@kline_{item.timeframe}";
        await foreach (var kline in base.Stream<BinanceCandleStream>(String.Join(",", subscriptions)))
        {
            yield return kline;
        }
    }
}