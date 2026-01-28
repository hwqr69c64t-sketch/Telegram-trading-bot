import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("TOKEN")

def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Buy", callback_data="buy"),
            InlineKeyboardButton("Sell", callback_data="sell")
        ],
        [
            InlineKeyboardButton("Positions", callback_data="positions"),
            InlineKeyboardButton("Copy Trade", callback_data="copy")
        ],
        [
            InlineKeyboardButton("Watchlist", callback_data="watchlist"),
            InlineKeyboardButton("Withdraw", callback_data="withdraw")
        ],
        [
            InlineKeyboardButton("Refresh", callback_data="refresh")
        ]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Solana • 🟢\n"
        "Balance: 0 SOL ($0.00)\n"
        "—\n\n"
        "Thank you for using our bot. ⚠️ "
        "We have no control over ads shown by Telegram in this bot."
    )
    await update.message.reply_text(text, reply_markup=main_keyboard())

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Balance: 0 SOL ($0.00)")

async def create_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE, chain: str):
    await update.message.reply_text(
        f"🔐 {chain} wallet created (DEMO)\n\n"
        "⚠️ This is a demo wallet.\n"
        "No real funds involved."
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Usage stats:\nUsers: 1\nTrades: 0")

async def valuation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⭐ Community rating: 5/5")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    responses = {
        "buy": "🟢 Buy (demo)",
        "sell": "🔴 Sell (demo)",
        "positions": "📂 No open positions",
        "copy": "📋 Copy trading not active",
        "watchlist": "👁️ Watchlist empty",
        "withdraw": "⚠️ Withdraw disabled",
        "refresh": "🔄 Refreshed\nBalance: 0 SOL"
    }

    await q.edit_message_text(
        responses.get(q.data, "Unknown action"),
        reply_markup=main_keyboard()
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("createwalletsol", lambda u, c: create_wallet(u, c, "Solana")))
app.add_handler(CommandHandler("createwalleteth", lambda u, c: create_wallet(u, c, "Ethereum")))
app.add_handler(CommandHandler("createwalletbtc", lambda u, c: create_wallet(u, c, "Bitcoin")))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("valuation", valuation))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
