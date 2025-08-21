import time
import requests
from tradingview_ta import TA_Handler, Interval
import os 

# ====== Telegram Config ======
TOKEN = os.getenv ("BOT_TOKEN")
CHAT_ID = os.getenv ("CHAT_ID")

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
        print("Telegram response:", r.json())   # debug
    except Exception as e:
        print("Telegram Error:", e)

# ====== Normalize symbol ======
def normalize_symbol(sym: str) -> str:
    sym = sym.upper().replace("USDT", "")
    return sym + "USDT"

# ====== Inputs ======
symbol_input = input("Enter coin symbol (BTC, ETH): ").strip()
tf_input = input("Choose timeframe (1m,5m,15m,30m,1h,2h,4h,1d,1W,1M): ").strip()

tf_key = tf_input.lower()
tf_map = {
    "1m": Interval.INTERVAL_1_MINUTE,
    "5m": Interval.INTERVAL_5_MINUTES,
    "15m": Interval.INTERVAL_15_MINUTES,
    "30m": Interval.INTERVAL_30_MINUTES,
    "1h": Interval.INTERVAL_1_HOUR,
    "2h": Interval.INTERVAL_2_HOURS,
    "4h": Interval.INTERVAL_4_HOURS,
    "1d": Interval.INTERVAL_1_DAY,
    "1w": Interval.INTERVAL_1_WEEK,
    "1mth": Interval.INTERVAL_1_MONTH
}
if tf_input == "1W":
    interval = Interval.INTERVAL_1_WEEK
elif tf_input == "1M":
    interval = Interval.INTERVAL_1_MONTH
else:
    interval = tf_map.get(tf_key)

if interval is None:
    raise ValueError("Invalid timeframe!")

symbol = normalize_symbol(symbol_input)

handler = TA_Handler(
    symbol=symbol,
    screener="crypto",
    exchange="BINANCE",
    interval=interval,
    timeout=9
)

# --- پیام اولیه برای تست تلگرام ---
send_msg(f"🚀 Bot started.\nSymbol={symbol} | TF={tf_input}")

# ====== Loop every 15 minutes ======
while True:
    try:
        analysis = handler.get_analysis()
        b = analysis.indicators.get("RSI")   # RSI
        a = analysis.indicators.get("ADX")   # ADX

        print(f"DEBUG -> {symbol} | {tf_input} | RSI={b} | ADX={a}")

        d, e = None, None

        # ---- Conditions ----
        if 0 < a < 20:
            d = 1
        elif 20 <= a < 60:
            d = 2

        if b < 20 or b > 80:
            e = 1
        elif 20 <= b <= 50:
            e = 2
        elif 50 < b <= 80:
            e = 3

        message = None
        if d == 2 and e == 2:
            message = f"{symbol} | {tf_input}\n📉 You can open a SELL position.\nRSI={b:.2f}, ADX={a:.2f}"
        elif d == 2 and e == 3:
            message = f"{symbol} | {tf_input}\n📈 You can open a BUY position.\nRSI={b:.2f}, ADX={a:.2f}"
        else:
            message = f"{symbol} | {tf_input}\n❌ You can't open a position.\nRSI={b:.2f}, ADX={a:.2f}"

        # --- ارسال پیام به تلگرام ---
        send_msg(message)

    except Exception as e:
        print("Error:", e)

    time.sleep(900)   # هر 15 دقیقه
