import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure clean path resolution to your 'bot' package
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bot.client import BinanceTestnetClient
from bot.orders import OrderManager
from bot.validators import validate_inputs
from bot.logging_config import setup_logger

setup_logger()

def main():
    st.set_page_config(page_title="Binance Terminal", page_icon="⚡")
    st.title("⚡ Binance Futures Testnet Terminal")
    st.caption("Python Trading Bot Assignment - Primetrade.ai")

    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    st.sidebar.header("Configuration")
    st.sidebar.success("✅ Application Running")
    mock_mode = st.sidebar.toggle("MOCK MODE", value=True)

    if mock_mode:
        st.warning("🧪 MOCK MODE ENABLED - No real Binance orders are being sent")
        # Inject dummy keys so the app runs without .env
        api_key = api_key or "mock_key"
        api_secret = api_secret or "mock_secret"
        st.sidebar.warning("🧪 MOCK MODE")
    else:
        if not api_key or not api_secret:
            st.error("❌ Missing API Keys in `.env` file.")
            st.stop()
        st.sidebar.success("🔗 Binance Testnet Connected")

    st.header("Place Order")
    col1, col2 = st.columns(2)
    with col1:
        symbol = st.selectbox("Symbol", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
        side = st.radio("Side", ["BUY", "SELL"], horizontal=True)
    with col2:
        order_type = st.selectbox("Type", ["MARKET", "LIMIT", "STOP_LIMIT", "OCO"])
        quantity = st.number_input("Quantity", min_value=0.000, step=0.001, format="%.3f")

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        price = st.number_input("Price", min_value=0.0, step=0.1)
    with p_col2:
        stop_price = st.number_input("Stop Price", min_value=0.0, step=0.1)

    if st.button("Execute Trade", type="primary", use_container_width=True):
        try:
            exec_price = price if order_type != "MARKET" and price > 0 else None
            exec_stop = stop_price if order_type in ["STOP_LIMIT", "OCO"] and stop_price > 0 else None
            
            validate_inputs(symbol, side, order_type, quantity, exec_price, exec_stop)
            
            client = BinanceTestnetClient(api_key, api_secret)
            manager = OrderManager(client, mock_mode=mock_mode)
            
            with st.spinner("Placing Order..."):
                res = manager.place_futures_order(symbol, side, order_type, quantity, exec_price, exec_stop)
            
            st.success(f"✅ Order {res.get('orderId')} Placed Successfully!")
            
            mcol1, mcol2, mcol3 = st.columns(3)
            mcol1.metric("Order ID", res.get("orderId"))
            mcol2.metric("Status", res.get("status"))
            mcol3.metric("Quantity", res.get("executedQty", "0"))
            
            st.json(res)
        except Exception as e:
            st.error(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()