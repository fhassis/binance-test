import pytest
from dotenv import load_dotenv
from os import environ
from asyncio import new_event_loop


@pytest.fixture(scope="session")
def event_loop():
    """
    Returns the event loop to be used in the tests.
    """
    loop = new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def api_keys():
    """
    Returns the api key and secret to be used in the tests.
    """
    # load environment variables from file
    load_dotenv("config.env")

    try:
        api_key = environ["BINANCE_API_KEY"]
        api_secret = environ["BINANCE_API_SECRET"]
        return (api_key, api_secret)
    except:
        raise Exception("Binance api keys are not set.")


@pytest.fixture(scope="session")
def trade_symbol():
    """
    Returns the symbol to use in trades.
    """
    return "BTCUSDT"
