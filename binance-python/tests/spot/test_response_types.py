import pytest

from binance_python.spot.client import BinanceSpotClient
from binance_python.spot.enums import OrderSide, OrderType, TimeInForce


@pytest.mark.asyncio
async def test_fetch_server_time_response(client: BinanceSpotClient):
    """
    Test return type of fetch_server_time endpoint.
    """
    data = await client.fetch_server_time()

    # ServerTimeResponse
    assert "serverTime" in data


@pytest.mark.asyncio
async def test_account_info_response(client: BinanceSpotClient):
    """
    Test return type of fetch_account_info endpoint.
    """
    data = await client.fetch_account_info()

    # AccountResponse
    assert "makerCommission" in data
    assert "takerCommission" in data
    assert "buyerCommission" in data
    assert "sellerCommission" in data
    assert "canTrade" in data
    assert "canWithdraw" in data
    assert "canDeposit" in data
    assert "updateTime" in data
    assert "accountType" in data
    assert "balances" in data
    assert "permissions" in data


@pytest.mark.asyncio
async def test_exchange_info_response(client: BinanceSpotClient):
    """
    Test return type of fetch_exchange_info endpoint.
    """
    data = await client.fetch_exchange_info()

    # ExchangeInfoResponse
    assert "timezone" in data
    assert "serverTime" in data
    assert "rateLimits" in data
    assert "exchangeFilters" in data
    assert "symbols" in data

    # SymbolInfoResponse
    symbol_data = data["symbols"][0]
    assert "symbol" in symbol_data
    assert "status" in symbol_data
    assert "baseAsset" in symbol_data
    assert "baseAssetPrecision" in symbol_data
    assert "quoteAsset" in symbol_data
    assert "quotePrecision" in symbol_data
    assert "quoteAssetPrecision" in symbol_data
    assert "orderTypes" in symbol_data
    assert "icebergAllowed" in symbol_data
    assert "ocoAllowed" in symbol_data
    assert "quoteOrderQtyMarketAllowed" in symbol_data
    assert "allowTrailingStop" in symbol_data
    assert "isSpotTradingAllowed" in symbol_data
    assert "isMarginTradingAllowed" in symbol_data
    assert "filters" in symbol_data
    assert "permissions" in symbol_data


@pytest.mark.asyncio
async def test_fetch_trades_response(client: BinanceSpotClient, trade_symbol: str):
    """
    Test return type of fetch_trades endpoint.
    """
    # places a market order to test
    order_data = await client.place_order(
        symbol=trade_symbol,
        order_side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        amount=0.01,
    )

    resp = await client.fetch_trades(trade_symbol)

    # list[TradesResponse]
    data = resp[0]

    # TradesResponse
    assert "symbol" in data
    assert "id" in data
    assert "orderId" in data
    assert "orderListId" in data
    assert "price" in data
    assert "qty" in data
    assert "quoteQty" in data
    assert "commission" in data
    assert "commissionAsset" in data
    assert "time" in data
    assert "isBuyer" in data
    assert "isMaker" in data
    assert "isBestMatch" in data


@pytest.mark.asyncio
async def test_place_order_response(client: BinanceSpotClient, trade_symbol: str):
    """
    Test return type of place_order endpoint.
    """
    # get entry price for a buy limit order
    price_data = await client.fetch_latest_price(trade_symbol)
    entry_price = round(float(price_data["price"]) * 0.8, 1)

    # creates a limit order
    data = await client.place_order(
        symbol=trade_symbol,
        order_side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        amount=0.01,
        price=entry_price,
        time_in_force=TimeInForce.GTC,
    )
    order_id = data["orderId"]

    # NewOrderResponse (ACK mode)
    assert "symbol" in data
    assert "orderId" in data
    assert "orderListId" in data
    assert "clientOrderId" in data
    assert "transactTime" in data

    # cancel the created test order
    await client.cancel_order(trade_symbol, order_id)


@pytest.mark.asyncio
async def test_fetch_order_status_response(
    client: BinanceSpotClient, trade_symbol: str
):
    """
    Test return type of fetch_order_status endpoint.
    """
    # get entry price for a buy limit order
    price_data = await client.fetch_latest_price(trade_symbol)
    entry_price = round(float(price_data["price"]) * 0.8, 1)

    # creates a test limit order
    new_order_data = await client.place_order(
        symbol=trade_symbol,
        order_side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        amount=0.01,
        price=entry_price,
        time_in_force=TimeInForce.GTC,
    )
    order_id = new_order_data["orderId"]

    data = await client.fetch_order_status(symbol=trade_symbol, order_id=order_id)

    # QueryOrderResponse
    assert "symbol" in data
    assert "orderId" in data
    assert "orderListId" in data
    assert "clientOrderId" in data
    assert "price" in data
    assert "origQty" in data
    assert "executedQty" in data
    assert "cummulativeQuoteQty" in data
    assert "status" in data
    assert "timeInForce" in data
    assert "type" in data
    assert "side" in data
    assert "stopPrice" in data
    assert "icebergQty" in data
    assert "time" in data
    assert "updateTime" in data
    assert "isWorking" in data
    assert "origQuoteOrderQty" in data

    # cancel the created test order
    await client.cancel_order(trade_symbol, order_id)


@pytest.mark.asyncio
async def test_cancel_order_response(client: BinanceSpotClient, trade_symbol: str):
    """
    Test return type of cancel_order endpoint.
    """
    # get entry price for a buy limit order
    price_data = await client.fetch_latest_price(trade_symbol)
    entry_price = round(float(price_data["price"]) * 0.8, 1)

    # creates a test limit order
    new_order_data = await client.place_order(
        symbol=trade_symbol,
        order_side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        amount=0.01,
        price=entry_price,
        time_in_force=TimeInForce.GTC,
    )
    order_id = new_order_data["orderId"]

    data = await client.cancel_order(symbol=trade_symbol, order_id=order_id)

    # CancelOrderResponse
    assert "symbol" in data
    assert "origClientOrderId" in data
    assert "orderId" in data
    assert "orderListId" in data
    assert "clientOrderId" in data
    assert "price" in data
    assert "origQty" in data
    assert "executedQty" in data
    assert "cummulativeQuoteQty" in data
    assert "status" in data
    assert "timeInForce" in data
    assert "type" in data
    assert "side" in data


@pytest.mark.asyncio
async def test_cancel_all_orders_response(client: BinanceSpotClient, trade_symbol: str):
    """
    Test return type of cancel_all_orders endpoint.
    """
    # get entry price for a buy limit order
    price_data = await client.fetch_latest_price(trade_symbol)
    entry_price = round(float(price_data["price"]) * 0.8, 1)

    # creates a test limit order 1
    new_order_data_1 = await client.place_order(
        symbol=trade_symbol,
        order_side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        amount=0.01,
        price=entry_price,
        time_in_force=TimeInForce.GTC,
    )

    # creates a test limit order 2
    new_order_data_2 = await client.place_order(
        symbol=trade_symbol,
        order_side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        amount=0.01,
        price=entry_price,
        time_in_force=TimeInForce.GTC,
    )

    resp = await client.cancel_all_orders(symbol=trade_symbol)

    # list[CancelOrderResponse]
    data = resp[0]

    # CancelOrderResponse
    assert "symbol" in data
    assert "origClientOrderId" in data
    assert "orderId" in data
    assert "orderListId" in data
    assert "clientOrderId" in data
    assert "price" in data
    assert "origQty" in data
    assert "executedQty" in data
    assert "cummulativeQuoteQty" in data
    assert "status" in data
    assert "timeInForce" in data
    assert "type" in data
    assert "side" in data


@pytest.mark.asyncio
async def test_fetch_open_orders_response(client: BinanceSpotClient, trade_symbol: str):
    """
    Test return type of fetch_open_orders endpoint.
    """
    # get entry price for a buy limit order
    price_data = await client.fetch_latest_price(trade_symbol)
    entry_price = round(float(price_data["price"]) * 0.8, 1)

    # creates a test limit order 1
    new_order_data_1 = await client.place_order(
        symbol=trade_symbol,
        order_side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        amount=0.01,
        price=entry_price,
        time_in_force=TimeInForce.GTC,
    )
    order_id_1 = new_order_data_1["orderId"]

    # creates a test limit order 2
    new_order_data_2 = await client.place_order(
        symbol=trade_symbol,
        order_side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        amount=0.01,
        price=entry_price,
        time_in_force=TimeInForce.GTC,
    )
    order_id_2 = new_order_data_2["orderId"]

    resp = await client.fetch_open_orders(symbol=trade_symbol)

    # list[QueryOrderResponse]
    data = resp[0]

    # QueryOrderResponse
    assert "symbol" in data
    assert "orderId" in data
    assert "orderListId" in data
    assert "clientOrderId" in data
    assert "price" in data
    assert "origQty" in data
    assert "executedQty" in data
    assert "cummulativeQuoteQty" in data
    assert "status" in data
    assert "timeInForce" in data
    assert "type" in data
    assert "side" in data
    assert "stopPrice" in data
    assert "icebergQty" in data
    assert "time" in data
    assert "updateTime" in data
    assert "isWorking" in data
    assert "origQuoteOrderQty" in data

    # cancel the test orders
    await client.cancel_order(trade_symbol, order_id_1)
    await client.cancel_order(trade_symbol, order_id_2)


@pytest.mark.asyncio
async def test_fetch_all_account_orders_response(
    client: BinanceSpotClient, trade_symbol: str
):
    """
    Test return type of fetch_all_account_orders endpoint.
    """
    resp = await client.fetch_all_account_orders(symbol=trade_symbol)

    # list[QueryOrderResponse]
    data = resp[0]  # assuming that there is already some order in the server...

    # QueryOrderResponse
    assert "symbol" in data
    assert "orderId" in data
    assert "orderListId" in data
    assert "clientOrderId" in data
    assert "price" in data
    assert "origQty" in data
    assert "executedQty" in data
    assert "cummulativeQuoteQty" in data
    assert "status" in data
    assert "timeInForce" in data
    assert "type" in data
    assert "side" in data
    assert "stopPrice" in data
    assert "icebergQty" in data
    assert "time" in data
    assert "updateTime" in data
    assert "isWorking" in data
    assert "origQuoteOrderQty" in data


@pytest.mark.asyncio
async def test_fetch_latest_price(client: BinanceSpotClient, trade_symbol: str):
    """
    Test return type of fetch_latest_price endpoint.
    """
    data = await client.fetch_latest_price(symbol=trade_symbol)

    # PriceTickerResponse
    assert "symbol" in data
    assert "price" in data


@pytest.mark.asyncio
async def test_fetch_latest_prices(client: BinanceSpotClient):
    """
    Test return type of fetch_latest_prices endpoint.
    """
    resp = await client.fetch_latest_prices()

    # list[PriceTickerResponse]
    if resp:
        data = resp[0]

        # PriceTickerResponse
        assert "symbol" in data
        assert "price" in data
    else:
        assert False


@pytest.mark.asyncio
async def test_fetch_order_book(client: BinanceSpotClient, trade_symbol: str):
    """
    Test return type of fetch_order_book endpoint.
    """
    data = await client.fetch_order_book(trade_symbol)

    # OrderBookResponse
    assert "lastUpdateId" in data
    assert "bids" in data
    assert "asks" in data
