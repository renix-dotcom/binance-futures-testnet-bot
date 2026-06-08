# Binance Futures Testnet Trading Bot 🚀

An enterprise-grade, lightweight trading bot built in Python. Features a beautifully styled Rich CLI and a clean Streamlit Dashboard to interact with the Binance Futures Testnet.

## 🏗 Architecture & Design Decisions

1. **Isolated Validation Layer**: `bot/validators.py` ensures bad parameters (e.g., negative quantities, missing prices) are caught locally *before* wasting network requests.
2. **Exception Hierarchy**: Custom exceptions (`TradingBotError`, `ValidationError`, `APIError`) in `bot/exceptions.py` make error handling deterministic.
3. **Service Segregation**: 
   - `client.py` strictly handles authentication and raw HTTP requests.
   - `orders.py` handles business logic and payload structuring.
4. **Structured JSON Logging**: Logs are centrally formatted into pure JSON by `bot/logging_config.py`. This ensures production-readiness for tools like Datadog or ELK.

## 📂 Project Structure
```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
├── logs/
│   └── trading_bot.log
├── screenshots/
├── app.py
├── cli.py
├── .env.example
├── requirements.txt
└── README.md
```

## Setup Steps

1. Clone this repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and insert your API keys:
   ```bash
   cp .env.example .env
   ```

## Running the CLI
You can place trades using the command line:
The CLI uses `rich` to provide beautiful terminal output.

**Place Orders:**
```bash
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --qty 0.01
python cli.py order --symbol ETHUSDT --side SELL --type LIMIT --qty 0.05 --price 3500
```

## Running the Interface
To launch the trading terminal with the Bitcoin/Cyberpunk trader aesthetics:
```bash
streamlit run app.py
```

## Assumptions
- All operations are restricted to Binance Futures Testnet.
- `bot` module logic is deployed flat in the directory per previous context to simplify Streamlit loading logic, fulfilling all structure goals directly alongside the interface.