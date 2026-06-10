import requests
import time
from datetime import datetime
from tradingview_ta import TA_Handler, Interval

# ====== Telegram Config (امن) ======
TOKEN = ("8374305315:AAFtQ-GZp_Uq13sSrb9vE3b3lH90xpGLR2U")
CHAT_ID = ("7726161526")

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print("Telegram Error:", e)

# ====== تنظیمات ======
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
tf_input = "1h"
interval = Interval.INTERVAL_1_HOUR

# ====== وضعیت جدا ======
prev_ema = {}
last_signal = {}

# ====== شروع ======
send_msg(f"🚀 Bot started\nSymbols={symbols} | TF={tf_input}")

# ====== Loop ======
while True:
    try:
        for symbol in symbols:
            print(f"🔍 Checking {symbol}")

            try:
                handler = TA_Handler(
                    symbol=symbol,
                    screener="crypto",
                    exchange="BINANCE",
                    interval=interval
                )

                analysis = handler.get_analysis()

                rsi = analysis.indicators.get("RSI")
                ema20 = analysis.indicators.get("EMA20")
                ema50 = analysis.indicators.get("EMA50")

                print(f"DEBUG {symbol} -> RSI={rsi} | EMA20={ema20} | EMA50={ema50}")

                # ====== مقدار اولیه ======
                if symbol not in prev_ema:
                    prev_ema[symbol] = {"ema20": None, "ema50": None}
                    last_signal[symbol] = None

                prev20 = prev_ema[symbol]["ema20"]
                prev50 = prev_ema[symbol]["ema50"]

                cross_up = False
                cross_down = False

                if prev20 and prev50:
                    if prev20 < prev50 and ema20 > ema50:
                        cross_up = True
                    elif prev20 > prev50 and ema20 < ema50:
                        cross_down = True

                prev_ema[symbol]["ema20"] = ema20
                prev_ema[symbol]["ema50"] = ema50

                # ====== شرط RSI + کراس ======
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

                # ====== جلوگیری از اسپم ======
                if signal != "NONE" and signal != last_signal[symbol]:
                    send_msg(message)
                    last_signal[symbol] = signal

            except Exception as e:
                print(f"❌ Error on {symbol}: {e}")

    except Exception as e:
        print("Main Error:", e)

    time.sleep(900)
