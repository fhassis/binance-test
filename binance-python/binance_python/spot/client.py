from typing import Optional

from binance_python.base_api_client import BaseApiClient, Params
from binance_python.spot.enums import OrderSide, OrderType, TimeInForce
from binance_python.spot.typings import (
    AccountResponse,
    CancelOrderResponse,
    ExchangeInfoResponse,
    ListenKeyResponse,
    NewOrderResponse,
    OrderBookResponse,
    PriceTickerResponse,
    QueryOrderResponse,
    ServerTimeResponse,
    TradesResponse,
)


class BinanceSpotClient(BaseApiClient):
    """
    Client to handle calls to the Binance API endpoints.
    """

    def __init__(self, api_key: str, api_secret: str, testnet: bool = False) -> None:
        super().__init__(api_key, api_secret, testnet)

    async def fetch_server_time(self) -> ServerTimeResponse:
        return await self._send_request("GET", "/api/v3/time")

    async def fetch_account_info(self) -> AccountResponse:
        params = dict(timestamp=self._get_timestamp())
        return await self._send_request("GET", "/api/v3/account", params)

    async def fetch_exchange_info(self) -> ExchangeInfoResponse:
        return await self._send_request("GET", "/api/v3/exchangeInfo")

    async def fetch_trades(
        self,
        symbol: str,
        from_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 1000,
    ) -> list[TradesResponse]:
        """
        Get trades for a specific account and symbol.
        :param symbol: symbol to get trades from
        :param from_id: TradeId to fetch from. it will get trades >= that fromId. Otherwise most recent trades are returned.
        :param start_time: start time to fetch the trades
        :param end_time: end time to fetch the trades
        :param limit: Default 500; max 1000
        """
        params: Params = dict(
            timestamp=self._get_timestamp(), symbol=symbol, limit=str(limit)
        )
        if from_id:
            params["fromId"] = str(from_id)
        if start_time:
            params["startTime"] = str(start_time)
        if end_time:
            params["endTime"] = str(end_time)
        return await self._send_request("GET", "/api/v3/myTrades", params)

    async def place_order(
        self,
        symbol: str,
        order_side: OrderSide,
        order_type: OrderType,
        amount: Optional[float] = None,
        price: Optional[float] = None,
        time_in_force: Optional[TimeInForce] = None,
        stop_price: Optional[float] = None,
    ) -> NewOrderResponse:
        """
        Send in a new order.
        """
        params: Params = dict(
            timestamp=self._get_timestamp(),
            symbol=symbol,
            side=order_side.name,
            type=order_type.name,
            newOrderRespType="ACK",  # to standardize responses. Other options: RESULT and FULL
        )
        if amount:
            params["quantity"] = str(amount)
        if price:
            params["price"] = str(price)
        if time_in_force:
            params["timeInForce"] = time_in_force.name
        if stop_price:
            params["stopPrice"] = str(stop_price)
        return await self._send_request("POST", "/api/v3/order", params)

    async def fetch_order_status(
        self, symbol: str, order_id: int
    ) -> QueryOrderResponse:
        """
        Check an order's status.
        """
        params: Params = dict(
            timestamp=self._get_timestamp(), symbol=symbol, orderId=str(order_id)
        )
        return await self._send_request("GET", "/api/v3/order", params)

    async def cancel_order(self, symbol: str, order_id: int) -> CancelOrderResponse:
        """
        Cancel an active order.
        """
        params: Params = dict(
            timestamp=self._get_timestamp(), symbol=symbol, orderId=str(order_id)
        )
        return await self._send_request("DELETE", "/api/v3/order", params)

    async def cancel_all_orders(self, symbol: str) -> list[CancelOrderResponse]:
        """
        Cancel all active orders on a symbol. This includes OCO orders.
        """
        params: Params = dict(timestamp=self._get_timestamp(), symbol=symbol)
        return await self._send_request("DELETE", "/api/v3/openOrders", params)

    async def fetch_open_orders(
        self, symbol: Optional[str] = None
    ) -> list[QueryOrderResponse]:
        """
        Get all open orders on a symbol. Careful when accessing this with no symbol.
        """
        params: Params = dict(timestamp=self._get_timestamp())
        if symbol:
            params["symbol"] = symbol
        return await self._send_request("GET", "/api/v3/openOrders", params)

    async def fetch_all_account_orders(
        self,
        symbol: str,
        from_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 1000,
    ) -> list[QueryOrderResponse]:
        """
        Get all account orders; active, canceled, or filled.
        :param symbol: symbol to get orders from
        :param from_id: OrderId to fetch from. it will get orders >= that orderId. Otherwise most recent trades are returned.
        :param start_time: start time to fetch the trades
        :param end_time: end time to fetch the trades
        :param limit: Default 500; max 1000
        """
        params: Params = dict(
            timestamp=self._get_timestamp(), symbol=symbol, limit=str(limit)
        )
        if from_id:
            params["orderId"] = str(from_id)
        if start_time:
            params["startTime"] = str(start_time)
        if end_time:
            params["endTime"] = str(end_time)
        return await self._send_request("GET", "/api/v3/allOrders", params)

    async def fetch_latest_price(self, symbol: str) -> PriceTickerResponse:
        """
        Latest price for a symbol.
        """
        params: Params = dict(symbol=symbol)
        return await self._send_request("GET", "/api/v3/ticker/price", params)

    async def fetch_latest_prices(self) -> list[PriceTickerResponse]:
        """
        Latest price for a symbol or symbols.
        """
        return await self._send_request("GET", "/api/v3/ticker/price")

    async def fetch_order_book(
        self, symbol: str, limit: Optional[int] = None
    ) -> OrderBookResponse:
        """
        Order book of a symbol.
        """
        params: Params = dict(symbol=symbol)
        if limit:
            params["limit"] = str(limit)
        return await self._send_request("GET", "/api/v3/depth", params)

    async def create_listen_key(self) -> str:
        """
        Creates a user account listen key.
        """
        raw_data: ListenKeyResponse = await self._send_request(
            "POST", "/api/v3/userDataStream"
        )
        return raw_data["listenKey"]

    async def keep_alive_listen_key(self, listen_key: str) -> None:
        """
        Keeps alive an existing user account listen key.
        """
        params = dict(listenKey=listen_key)
        return await self._send_request("PUT", "/api/v3/userDataStream", params)

    async def close_listen_key(self, listen_key: str) -> None:
        """
        Closes an existing user account listen key.
        """
        params = dict(listenKey=listen_key)
        return await self._send_request("DELETE", "/api/v3/userDataStream", params)
