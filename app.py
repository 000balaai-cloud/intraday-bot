import requests
import yfinance as yf
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8748280375:AAHvC6xJ-KTkies0XQF_dmBd98_m2sLxbDs"

# Function to analyze stock
def analyze_stock(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="5d", interval="15m")

    if len(data) < 10:
        return None

    last_price = data['Close'].iloc[-1]
    sma = data['Close'].rolling(window=5).mean().iloc[-1]

    if last_price > sma:
        signal = "BUY"
    else:
        signal = "SELL"

    return f"{symbol} → {signal} at ₹{round(last_price,2)}"

# Bot reply
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.lower()

    if message == "hi":
        stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "SBIN.NS"]
        results = []

        for s in stocks:
            result = analyze_stock(s)
            if result:
                results.append(result)

        reply_text = "📊 Top Intraday Picks:\n\n" + "\n".join(results)
        await update.message.reply_text(reply_text)

    else:
        await update.message.reply_text("Send 'hi' to get intraday picks.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))


app.run_polling()
