import logging
import os
import json

class StructuredFormatter(logging.Formatter):
    """Formats logs as JSON for structured ingestion (e.g., Datadog, ELK)."""
    def format(self, record):
        try:
            msg_data = json.loads(record.getMessage())
            if not isinstance(msg_data, dict):
                msg_data = {"message": record.getMessage()}
        except (ValueError, TypeError):
            msg_data = {"message": record.getMessage()}
            
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            **msg_data
        }
        return json.dumps(log_record)

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("TradingBot")
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        fh = logging.FileHandler("logs/trading_bot.log")
        fh.setLevel(logging.DEBUG)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        formatter = StructuredFormatter(fmt='%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
    return logger