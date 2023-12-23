from typing import TypedDict, Any, Union


class ServerTimeResponse(TypedDict):
    serverTime: int


class BalanceResponse(TypedDict):
    asset: str
    free: str
    locked: str


class AccountResponse(TypedDict):
    makerCommission: int
    takerCommission: int
    buyerCommission: int
    sellerCommission: int
    canTrade: bool
    canWithdraw: bool
    canDeposit: bool
    updateTime: int
    accountType: str
    balances: list[BalanceResponse]
    permissions: list[str]


class TradesResponse(TypedDict):
    symbol: str
    id: int
    orderId: int
    orderListId: int
    price: str
    qty: str
    quoteQty: str
    commission: str
    commissionAsset: str
    time: int
    isBuyer: bool
    isMaker: bool
    isBestMatch: bool


class NewOrderResponse(TypedDict):
    symbol: str
    orderId: int
    orderListId: int
    clientOrderId: str
    transactTime: int


class QueryOrderResponse(TypedDict):
    symbol: str
    orderId: int
    orderListId: int
    clientOrderId: str
    price: str
    origQty: str
    executedQty: str
    cummulativeQuoteQty: str
    status: str
    timeInForce: str
    type: str
    side: str
    stopPrice: str
    icebergQty: str
    time: int
    updateTime: int
    isWorking: bool
    origQuoteOrderQty: str


class CancelOrderResponse(TypedDict):
    symbol: str
    origClientOrderId: str
    orderId: int
    orderListId: int
    clientOrderId: str
    price: str
    origQty: str
    executedQty: str
    cummulativeQuoteQty: str
    status: str
    timeInForce: str
    type: str
    side: str


class PriceTickerResponse(TypedDict):
    symbol: str
    price: str


class OrderBookResponse(TypedDict):
    lastUpdateId: int
    bids: list[list[str]]
    asks: list[list[str]]


class PriceFilterResponse(TypedDict):
    filterType: str
    minPrice: str
    maxPrice: str
    tickSize: str


class PercentPriceFilterResponse(TypedDict):
    filterType: str
    multiplierUp: str
    multiplierDown: str
    avgPriceMins: int


class PercentPriceBySiseFilterResponse(TypedDict):
    filterType: str
    bidMultiplierUp: str
    bidMultiplierDown: str
    askMultiplierUp: str
    askMultiplierDown: str
    avgPriceMins: int


class LotSizeFilterResponse(TypedDict):
    filterType: str
    minQty: str
    maxQty: str
    stepSize: str


class MinNotionalFilterResponse(TypedDict):
    filterType: str
    minNotional: str
    applyToMarket: bool
    avgPriceMins: int


class IcebergPartsFilterResponse(TypedDict):
    filterType: str
    limit: int


class MarketLotSizeFilterResponse(TypedDict):
    filterType: str
    minQty: str
    maxQty: bool
    stepSize: int


class MaxNumOrdersFilterResponse(TypedDict):
    filterType: str
    maxNumOrders: int


class MaxNumAlgoOrdersFilterResponse(TypedDict):
    filterType: str
    maxNumAlgoOrders: int


class MaxNumIcebergOrdersFilterResponse(TypedDict):
    filterType: str
    maxNumIcebergOrders: int


class MaxPositionFilterResponse(TypedDict):
    filterType: str
    maxPosition: str


class TrailingDeltaFilterResponse(TypedDict):
    filterType: str
    minTrailingAboveDelta: int
    maxTrailingAboveDelta: int
    minTrailingBelowDelta: int
    maxTrailingBelowDelta: int


PriceFilters = Union[
    PriceFilterResponse,
    PercentPriceFilterResponse,
    PercentPriceBySiseFilterResponse,
    LotSizeFilterResponse,
    MinNotionalFilterResponse,
    IcebergPartsFilterResponse,
    MarketLotSizeFilterResponse,
    MaxNumOrdersFilterResponse,
    MaxNumAlgoOrdersFilterResponse,
    MaxNumIcebergOrdersFilterResponse,
    MaxPositionFilterResponse,
    TrailingDeltaFilterResponse,
]


class SymbolInfoResponse(TypedDict):
    symbol: str
    status: str
    baseAsset: str
    baseAssetPrecision: int
    quoteAsset: str
    quotePrecision: int
    quoteAssetPrecision: int
    orderTypes: list[str]
    icebergAllowed: bool
    ocoAllowed: bool
    quoteOrderQtyMarketAllowed: bool
    allowTrailingStop: bool
    isSpotTradingAllowed: bool
    isMarginTradingAllowed: str
    filters: list[PriceFilters]
    permissions: list[Any]


class ExchangeInfoResponse(TypedDict):
    timezone: str
    serverTime: int
    rateLimits: list[Any]
    exchangeFilters: list[Any]
    symbols: list[SymbolInfoResponse]


class ListenKeyResponse(TypedDict):
    listenKey: str
