class TradingBotError(Exception):
    """Base exception for the trading bot."""
    pass

class ValidationError(TradingBotError):
    """Raised when input validation fails before hitting the API."""
    pass

class APIError(TradingBotError):
    """Raised when the Binance API returns a non-200 response."""
    pass