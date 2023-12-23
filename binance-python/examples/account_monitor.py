from logging import getLogger
from typing import NoReturn

from binance_python.spot.client import BinanceSpotClient
from binance_python.spot.user_data_stream import BinanceUserDataStream


logger = getLogger(__name__)


async def monitor_account(api_key: str, api_secret: str, testnet: bool) -> NoReturn:
    """
    Executes a main asyncio application.
    """
    # creates a binance spot client
    binance_spot_client = BinanceSpotClient(api_key, api_secret, testnet)

    # creates a user data stream
    user_data_stream = BinanceUserDataStream(binance_spot_client)

    # loops forever
    while True:

        # handles incoming messages
        async for message in user_data_stream.stream():
            match message["e"]:
                case "outboundAccountPosition":
                    logger.info(message)
                case "balanceUpdate":
                    logger.info(message)
                case "executionReport":
                    logger.info(message)
                case "listStatus":
                    logger.info(message)
                case _:
                    logger.error(f"unknown message data: {message}")


if __name__ == "__main__":

    import logging
    from os import environ
    from asyncio import get_event_loop

    # configures the logger
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s | %(message)s",
        level=logging.INFO,
    )

    # executes the application
    try:
        loop = get_event_loop()
        loop.run_until_complete(
            monitor_account(
                api_key=environ["BINANCE_API_KEY"],
                api_secret=environ["BINANCE_API_SECRET"],
                testnet=bool(environ["BINANCE_TESTNET"]),
            )
        )
    except KeyboardInterrupt:
        print("Shutting down...")
