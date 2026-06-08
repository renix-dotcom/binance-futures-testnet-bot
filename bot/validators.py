from .exceptions import ValidationError

def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None) -> bool:
    """Validates order input parameters before interacting with the API."""
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero.")
    
    if side not in ["BUY", "SELL"]:
        raise ValidationError("Side must be BUY or SELL.")
        
    if order_type not in ["MARKET", "LIMIT", "STOP_LIMIT", "OCO"]:
        raise ValidationError("Order type must be MARKET, LIMIT, STOP_LIMIT, or OCO.")

    if order_type == "LIMIT" and (price is None or price <= 0):
        raise ValidationError("A valid price greater than zero is required for LIMIT orders.")
        
    if order_type in ["STOP_LIMIT", "OCO"] and (stop_price is None or stop_price <= 0):
        raise ValidationError("A valid stop price is required for STOP_LIMIT and OCO orders.")
        
    return True