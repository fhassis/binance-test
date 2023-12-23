from httpx import AsyncClient
from time import time
from hashlib import sha256
from hmac import new as hmac
from orjson import loads
from typing import Any, Optional


CONNECTION_ERROR_CODE = 99
Params = dict[str, str]


class BinanceApiException(Exception):
    def __init__(self, error_code: int, error_message: str) -> None:
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(f"{self.error_code}: {self.error_message}")


class BaseApiClient:
    """
    Base class to handle calls to the Binance API endpoints.
    """

    testnet: bool

    def __init__(self, api_key: str, api_secret: str, testnet: bool = False) -> None:
        self._api_secret = api_secret.encode("utf-8")
        self._http = AsyncClient(
            base_url="https://testnet.binance.vision"
            if testnet
            else "https://api.binance.com",
            headers={"X-MBX-APIKEY": api_key},
        )
        self.testnet = testnet

    async def dispose(self) -> None:
        """
        Disposes the client and releases inner resources.
        """
        await self._http.aclose()

    @staticmethod
    def _get_timestamp() -> str:
        """
        Returns the UTC milliseconds since epoch.
        """
        return str(int(time() * 1000))

    def _generate_query_params(self, params: Params) -> str:
        """
        Form query parameters for the requests. Adds "signature" if "timestamp" is present.
        """
        # generate query parameters as bytes
        query_params = "&".join([f"{key}={value}" for key, value in params.items()])

        # check if it is a signed method (has a timestamp)
        if "timestamp" in params:
            query_params += f"&signature={hmac(self._api_secret, query_params.encode('utf-8'), sha256).hexdigest()}"

        return query_params

    async def _send_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Params] = None,
    ) -> Any:
        """
        Performs an http request to the Binance server.
        """
        # generate query params
        query_params = self._generate_query_params(params) if params else None

        # make the request
        try:
            response = await self._http.request(
                method=method,
                url=endpoint,
                params=query_params,
            )
        except Exception:
            raise BinanceApiException(
                CONNECTION_ERROR_CODE,
                "Unable to connect with binance server",
            )

        # handles response
        data = loads(response.content)
        if response.status_code == 200:
            return data
        else:
            raise BinanceApiException(data["code"], data["msg"])
