import requests
import time
from datetime import datetime
from tradingview_ta import TA_Handler, Interval

# ====== Telegram Config ======
TOKEN = '8374305315:AAHakQ4jTQ3_YVt50N2veH_xGSv1TRIEXcA'
CHAT_ID = '7726161526'

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print("Telegram Error:", e)

# ====== تنظیمات ثابت ======
symbol = "BTCUSDT"   # اینجا ارز رو عوض کن
tf_input = "1h"

interval = Interval.INTERVAL_15_MINUTES

handler = TA_Handler(
    symbol=symbol,
    screener="crypto",
    exchange="BINANCE",
    interval=interval
)

# ====== متغیرهای کنترل ======
prev_ema20 = None
prev_ema50 = None
last_signal = None

# ====== شروع ======
send_msg(f"🚀 Bot started\nSymbol={symbol} | TF={tf_input}")

# ====== Loop ======
while True:
    try:
        analysis = handler.get_analysis()

        rsi = analysis.indicators.get("RSI")
        ema20 = analysis.indicators.get("EMA20")
        ema50 = analysis.indicators.get("EMA50")

        print(f"DEBUG -> RSI={rsi} | EMA20={ema20} | EMA50={ema50}")

        cross_up = False
        cross_down = False

        if prev_ema20 and prev_ema50:
            if prev_ema20 < prev_ema50 and ema20 > ema50:
                cross_up = True
            elif prev_ema20 > prev_ema50 and ema20 < ema50:
                cross_down = True

        prev_ema20 = ema20
        prev_ema50 = ema50

        # ====== شرط‌ها ======
        if rsi >= 58 and cross_up:
            signal = "BUY"
        elif rsi <= 42 and cross_down:
            signal = "SELL"
        else:
            signal = "NONE"

        # ====== پیام ======
        if signal == "BUY":
            message = f"{symbol} | {tf_input}\n📈 BUY SIGNAL\nRSI={rsi:.2f}"
        elif signal == "SELL":
            message = f"{symbol} | {tf_input}\n📉 SELL SIGNAL\nRSI={rsi:.2f}"

        # ====== ارسال فقط در صورت سیگنال جدید ======
        if signal != "NONE" and signal != last_signal:
            send_msg(message)
            last_signal = signal

    except Exception as e:
        print("Error:", e)

    time.sleep(900)  # هر 15 دقیقه
