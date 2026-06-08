import time
import hmac
import hashlib
import requests
from typing import Dict, Any, List
from .logging_config import setup_logger
from .exceptions import APIError

logger = setup_logger()

class BinanceTestnetClient:
    """Client wrapper for the Binance Futures Testnet REST API."""
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com"
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def _sign(self, query_string: str) -> str:
        """Generates an HMAC SHA256 signature for authenticated requests."""
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def send_signed_request(self, method: str, endpoint: str, payload: Dict[str, Any] = None) -> Any:
        """Sends a securely signed HTTP request to Binance."""
        payload = payload or {}
        payload["timestamp"] = int(time.time() * 1000)
        query_string = "&".join([f"{k}={v}" for k, v in payload.items()])
        signature = self._sign(query_string)
        url = f"{self.base_url}{endpoint}?{query_string}&signature={signature}"
        
        logger.debug(f'{{"action": "api_request", "method": "{method}", "endpoint": "{endpoint}"}}')
        response = self.session.request(method, url)
        
        if not response.ok:
            error_msg = response.text
            logger.error(f'{{"action": "api_error", "status_code": {response.status_code}, "response": {error_msg}}}')
            raise APIError(f"Binance API Error: {error_msg}")
            
        return response.json()

    def get_open_positions(self) -> List[Dict[str, Any]]:
        """Retrieves currently open positions."""
        positions = self.send_signed_request("GET", "/fapi/v2/positionRisk")
        return [pos for pos in positions if float(pos['positionAmt']) != 0]