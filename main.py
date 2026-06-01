import requests
import time
from datetime import datetime, timedelta
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

# ====== تنظیمات ======
symbol = "BTCUSDT"

# 👇 اینو فقط عوض کن
TIMEFRAME = "1h"

# ====== مپ تایم‌فریم ======
tf_map = {
    "15m": (Interval.INTERVAL_15_MINUTES, 15),
    "30m": (Interval.INTERVAL_30_MINUTES, 30),
    "1h": (Interval.INTERVAL_1_HOUR, 60),
    "4h": (Interval.INTERVAL_4_HOURS, 240),
}

interval, minutes = tf_map[TIMEFRAME]

handler = TA_Handler(
    symbol=symbol,
    screener="crypto",
    exchange="BINANCE",
    interval=interval
)

# ====== کنترل ======
prev_ema20 = None
prev_ema50 = None
last_signal = None

# ====== تابع زمان‌بندی ======
def wait_until_next_run():
    now = datetime.now()

    current_minute = now.minute

    next_minute = ((current_minute // minutes) + 1) * minutes

    if next_minute >= 60:
        next_time = now.replace(minute=0, second=5, microsecond=0) + timedelta(hours=1)
    else:
        next_time = now.replace(minute=next_minute, second=5, microsecond=0)

    wait_seconds = (next_time - now).total_seconds()

    print(f"⏳ Waiting {int(wait_seconds)} seconds...")
    time.sleep(wait_seconds)

# ====== شروع ======
send_msg(f"🚀 Bot started\n{symbol} | TF={TIMEFRAME}")

# ====== Loop ======
while True:
    try:
        analysis = handler.get_analysis()
        time.sleep(1)

        rsi = analysis.indicators.get("RSI")
        ema20 = analysis.indicators.get("EMA20")
        ema50 = analysis.indicators.get("EMA50")

        print(f"DEBUG -> RSI={rsi} EMA20={ema20} EMA50={ema50}")

        cross_up = False
        cross_down = False

        if prev_ema20 and prev_ema50:
            if prev_ema20 < prev_ema50 and ema20 > ema50:
                cross_up = True
            elif prev_ema20 > prev_ema50 and ema20 < ema50:
                cross_down = True

        prev_ema20 = ema20
        prev_ema50 = ema50

        # ====== شرط ======
        if rsi < 40 and cross_up:
            signal = "BUY"
        elif rsi >= 60 and cross_down:
            signal = "SELL"
        else:
            signal = "NONE"

        if signal == "BUY":
            message = f"{symbol}\n📈 BUY SIGNAL\nRSI={rsi:.2f}"
        elif signal == "SELL":
            message = f"{symbol}\n📉 SELL SIGNAL\nRSI={rsi:.2f}"

        if signal != "NONE" and signal != last_signal:
            send_msg(message)
            last_signal = signal

    except Exception as e:
    print("Error:", e)
    time.sleep(10)

    # 👇 این خیلی مهمه
    wait_until_next_run()
