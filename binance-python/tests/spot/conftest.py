import pytest

from binance_python.spot.client import BinanceSpotClient


@pytest.fixture(scope="session")
def client(event_loop, api_keys):
    """
    Provides the binance client to be used in the tests.
    """
    # extract api keys
    api_key, api_secret = api_keys

    # creates the client
    binance = BinanceSpotClient(api_key, api_secret, testnet=True)

    # return the client to be used in tests
    yield binance

    # disposes the client
    event_loop.run_until_complete(binance.dispose())
