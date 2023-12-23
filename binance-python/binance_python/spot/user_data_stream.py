from logging import getLogger
from typing import Optional, NoReturn, AsyncIterator
from asyncio import sleep, Task, create_task

from binance_python.base_ws_client import BaseWebsocketClient
from binance_python.spot.client import BinanceSpotClient


logger = getLogger(__name__)


class BinanceUserDataStream(BaseWebsocketClient):

    _binance_client: BinanceSpotClient
    _renew_task: Optional[Task] = None

    def __init__(self, binance_client: BinanceSpotClient):
        super().__init__(logger, binance_client.testnet)
        self._binance_client = binance_client

    async def _renew_listen_key(self, listen_key: str) -> NoReturn:
        """
        Periodically renews the listen key.
        """
        logger.info("renew listen key task started")
        retry_seconds = 60.0  # 1 minute
        renew_seconds = 1800.0  # 30 minutes

        while True:
            # waits until the next renewal time
            await sleep(renew_seconds)

            # renews the listen key
            while True:
                try:
                    logger.info(f"renewing listen key: {listen_key}")
                    await self._binance_client.keep_alive_listen_key(listen_key)
                    break
                except Exception as exc:
                    logger.error(f"unable to renew listen key: {exc}")
                    await sleep(retry_seconds)

    async def stream(self) -> AsyncIterator[dict]:
        """
        Provides user data as a stream.
        """
        # handles websocket disconnection
        while True:

            # creates the subscription
            listen_key = await self._binance_client.create_listen_key()
            renew_task = create_task(self._renew_listen_key(listen_key))
            self._subscriptions.add(listen_key)

            # handles incoming data
            async for message in self._stream(raw_stream=True):
                yield message

            # handles disconnection
            self._subscriptions.remove(listen_key)
            renew_task.cancel()
