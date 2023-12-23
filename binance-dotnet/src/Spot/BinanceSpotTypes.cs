using System.Text.Json.Serialization;

public readonly record struct BinanceError(
    [property: JsonPropertyName("msg")] string Message,
    [property: JsonPropertyName("code")] int Code
);

public readonly record struct BinanceServerTime(
    [property: JsonPropertyName("serverTime")] long ServerTime
);

public readonly record struct BinanceBalance(
    [property: JsonPropertyName("asset")] string Asset,
    [property: JsonPropertyName("free")] decimal Free,
    [property: JsonPropertyName("locked")] decimal Locked
);

public readonly record struct BinanceAccountInfo(
    [property: JsonPropertyName("makerCommission")] int MakerCommission,
    [property: JsonPropertyName("takerCommission")] int TakerCommission,
    [property: JsonPropertyName("buyerCommission")] int BuyerCommission,
    [property: JsonPropertyName("sellerCommission")] int SellerCommission,
    [property: JsonPropertyName("canTrade")] bool CanTrade,
    [property: JsonPropertyName("canWithdraw")] bool CanWithdraw,
    [property: JsonPropertyName("canDeposit")] bool CanDeposit,
    [property: JsonPropertyName("updateTime")] long UpdateTime,
    [property: JsonPropertyName("accountType")] string AccountType,
    [property: JsonPropertyName("balances")] List<BinanceBalance> Balances,
    [property: JsonPropertyName("permissions")] List<string> Permissions
);

public readonly record struct BinanceTrade(
    [property: JsonPropertyName("symbol")] string Symbol,
    [property: JsonPropertyName("id")] long Id,
    [property: JsonPropertyName("orderId")] long OrderId,
    [property: JsonPropertyName("orderListId")] long OrderListId,
    [property: JsonPropertyName("price")] decimal Price,
    [property: JsonPropertyName("qty")] decimal Qty,
    [property: JsonPropertyName("quoteQty")] decimal QuoteQty,
    [property: JsonPropertyName("commission")] decimal Commission,
    [property: JsonPropertyName("commissionAsset")] string CommissionAsset,
    [property: JsonPropertyName("time")] long Time,
    [property: JsonPropertyName("isBuyer")] bool IsBuyer,
    [property: JsonPropertyName("isMaker")] bool IsMaker,
    [property: JsonPropertyName("isBestMatch")] bool IsBestMatch
);

public readonly record struct BinanceCandleStreamItem(
    [property: JsonPropertyName("t")] long KlineStartTime,
    [property: JsonPropertyName("T")] long KlineCloseTime,
    [property: JsonPropertyName("s")] string Symbol,
    [property: JsonPropertyName("i")] string Interval,
    [property: JsonPropertyName("f")] long FirstTradeId,
    [property: JsonPropertyName("L")] long LastTradeId,
    [property: JsonPropertyName("o")] decimal OpenPrice,
    [property: JsonPropertyName("c")] decimal ClosePrice,
    [property: JsonPropertyName("h")] decimal HighPrice,
    [property: JsonPropertyName("l")] decimal LowPrice,
    [property: JsonPropertyName("v")] decimal BaseAssetVolume,
    [property: JsonPropertyName("n")] long NumberOfTrades,
    [property: JsonPropertyName("x")] bool IsKlineClosed,
    [property: JsonPropertyName("q")] decimal QuoteAssetVolume,
    [property: JsonPropertyName("V")] decimal TakerBuyBaseAssetVolume,
    [property: JsonPropertyName("Q")] decimal TakerBuyQuoteAssetVolume,
    [property: JsonPropertyName("B")] long Ignore
);

public readonly record struct BinanceCandleStream(
    [property: JsonPropertyName("e")] string EventType,
    [property: JsonPropertyName("E")] long EventTime,
    [property: JsonPropertyName("s")] string Symbol,
    [property: JsonPropertyName("k")] BinanceCandleStreamItem Data
);
