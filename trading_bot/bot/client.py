from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any, Dict
from urllib.parse import urlencode

import requests


class BinanceAPIError(Exception):
    def __init__(self, status_code: int, payload: Any):
        self.status_code = status_code
        self.payload = payload
        super().__init__(f"Binance API error {status_code}: {payload}")


class BinanceFuturesTestnetClient:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://testnet.binancefuture.com",
        timeout: int = 15,
        logger=None,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": api_key})

    def _sign(self, params: Dict[str, Any]) -> str:
        query_string = urlencode(params, doseq=True)
        return hmac.new(self.api_secret, query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    def _request(self, method: str, path: str, signed: bool = False, **params: Any) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        params = {k: v for k, v in params.items() if v is not None}
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["recvWindow"] = 5000
            params["signature"] = self._sign(params)

        if self.logger:
            safe_params = {k: v for k, v in params.items() if k != "signature"}
            self.logger.info("api_request method=%s path=%s params=%s", method, path, safe_params)

        try:
            response = self.session.request(method=method, url=url, params=params, timeout=self.timeout)
        except requests.RequestException as exc:
            if self.logger:
                self.logger.exception("network_error method=%s path=%s error=%s", method, path, exc)
            raise

        try:
            data = response.json()
        except ValueError:
            data = {"raw": response.text}

        if self.logger:
            self.logger.info("api_response status_code=%s path=%s body=%s", response.status_code, path, data)

        if not response.ok:
            raise BinanceAPIError(response.status_code, data)
        return data

    def ping(self) -> Dict[str, Any]:
        return self._request("GET", "/fapi/v1/ping")

    def place_order(self, **params: Any) -> Dict[str, Any]:
        return self._request("POST", "/fapi/v1/order", signed=True, **params)
