from websockets.client import connect, WebSocketClientProtocol
from websockets.exceptions import ConnectionClosed
from logging import Logger, getLogger
from typing import Optional, AsyncIterator, cast
from orjson import loads, dumps
from time import time


class BaseWebsocketClient:
    """
    Websocket client class.
    """

    _websocket = Optional[WebSocketClientProtocol]
    _subscriptions: set[str] = set()
    _base_url: str
    _logger: Logger

    def __init__(self, logger: Optional[Logger], testnet=False) -> None:
        self._base_url = (
            "wss://testnet.binance.vision"
            if testnet
            else "wss://stream.binance.com:9443"
        )
        self._logger = logger if logger else getLogger(__name__)

    async def _send_subscription(self, subscriptions: list[str], subscribe: bool):
        """
        Sends a subscribe / unsubscribe message over websocket.
        """
        if self._websocket:
            try:
                message = {
                    "method": "SUBSCRIBE" if subscribe else "UNSUBSCRIBE",
                    "params": subscriptions,
                    "id": int(time() * 1000),
                }
                await self._websocket.send(dumps(message).decode("utf-8"))  # type: ignore
            except Exception as exc:
                self._logger.warning(f"unable to send subscription message: {exc}")
        else:
            self._logger.warning(
                f"unable to send subscription: websocket is disconnected"
            )

    async def _stream(self, raw_stream: bool) -> AsyncIterator[dict]:
        """
        Provides a stream of messages received over a connected websocket.
        """
        # defines the kind of stream: raw or combined
        url = f"{self._base_url}/ws" if raw_stream else f"{self._base_url}/stream"

        # connects with binance server
        self._logger.info(f"connecting websocket: {url}")
        async with connect(uri=url, ssl=True) as websocket:
            try:
                # handles websocket connection
                self._logger.info(f"connected websocket: {url}")
                self._websocket = websocket

                # send subscriptions if there are any
                if self._subscriptions:
                    self._logger.info(f"subscribing to streams {self._subscriptions}")
                    await self._send_subscription(list(self._subscriptions), subscribe=True)

                # keep waiting for messages and process them
                async for data in websocket:
                    
                    # just type cast Data as str for type checking properly
                    message = cast(str, data)

                    # logs the received message for debug purposes
                    self._logger.debug(f"received raw message: {message}")

                    # it is a subscription response
                    if message.startswith('{"return"'):
                        self._logger.debug("ignoring subscription response")

                    # it is a new data message
                    else:
                        # parses the json object and passes as dict
                        yield loads(message)

            except ConnectionClosed:
                self._logger.warning(f"disconnected websocket: {url}")
                self._websocket = None

            except Exception as exc:
                self._logger.error(f"unknown error in websocket: {exc}")
