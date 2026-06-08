import json
import time
from typing import Dict, Any, Optional
from .logging_config import setup_logger

logger = setup_logger()

class OrderManager:
    """Manages order logic, payload construction, and execution."""
    
    def __init__(self, client, mock_mode: bool = False):
        self.client = client
        self.mock_mode = mock_mode

    def place_futures_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None, stop_price: Optional[float] = None) -> Dict[str, Any]:
        """Constructs and executes a Futures order payload."""
        logger.info(json.dumps({
            "action": "order_request",
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "mock_mode": self.mock_mode
        }))
        payload = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        
        if order_type in ["LIMIT", "STOP_LIMIT", "OCO"]:
            payload["price"] = price
            payload["timeInForce"] = "GTC"
            
        if order_type in ["STOP_LIMIT", "OCO"]:
            payload["stopPrice"] = stop_price or price
            
        if self.mock_mode:
            mock_id = int(time.time() * 1000)
            mock_price = price if price and price > 0 else 107500.00
            response = {
                "orderId": mock_id,
                "status": "NEW" if order_type in ["LIMIT", "STOP_LIMIT", "OCO"] else "FILLED",
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "executedQty": str(quantity) if order_type == "MARKET" else "0.000",
                "avgPrice": f"{mock_price:.2f}",
                "transactTime": mock_id
            }
        else:
            response = self.client.send_signed_request("POST", "/fapi/v1/order", payload)
        
        logger.info(json.dumps({
            "action": "order_success",
            "orderId": response.get('orderId'),
            "status": response.get('status')
        }))
        return response