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

interval = Interval.INTERVAL_1_HOUR

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

#------------------------------------------------------------------

symbol2 = "SOLUSDT"   # اینجا ارز رو عوض کن

handler2 = TA_Handler(
    symbol=symbol2,
    screener="crypto",
    exchange="BINANCE",
    interval=interval
)

# ====== متغیرهای کنترل ======
prev2_ema20 = None
prev2_ema50 = None
last2_signal = None

# ====== شروع ======
send_msg(f"🚀 Bot started\nSymbol={symbol2} | TF={tf_input}")

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

    try:
        analysis = handler.get_analysis()

        rsi2 = analysis.indicators.get("RSI")
        ema220 = analysis.indicators.get("EMA20")
        ema250 = analysis.indicators.get("EMA50")

        print(f"DEBUG -> RSI={rsi2} | EMA20={ema220} | EMA50={ema250}")

        cross2_up = False
        cross2_down = False

        if prev2_ema20 and prev2_ema50:
            if prev2_ema20 < prev2_ema50 and ema220 > ema250:
                cross2_up = True
            elif prev2_ema20 > prev2_ema50 and ema220 < ema250:
                cross2_down = True

        prev2_ema20 = ema220
        prev2_ema50 = ema250

        # ====== شرط‌ها ======
        if rsi2 >= 58 and cross2_up:
            signal2 = "BUY"
        elif rsi2 <= 42 and cross2_down:
            signal2 = "SELL"
        else:
            signal2 = "NONE"

        # ====== پیام ======
        if signal2 == "BUY":
            message = f"{symbol2} | {tf_input}\n📈 BUY SIGNAL\nRSI={rsi2:.2f}"
        elif signal == "SELL":
            message = f"{symbol2} | {tf_input}\n📉 SELL SIGNAL\nRSI={rsi2:.2f}"

        # ====== ارسال فقط در صورت سیگنال جدید ======
        if signal2 != "NONE" and signal2 != last_signal2:
            send_msg(message)
            last_signal2 = signal2

    except Exception as e:
        print("Error:", e)

    time.sleep(900)  # هر 15 دقیقه
