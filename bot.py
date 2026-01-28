import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Please set the TOKEN environment variable")

# Tvoje Solana peněženka
SOL_WALLET = "9ryYUqtmyUhy5DV8F2s24Fv5L4Pkjcn4LtUH6oPR3HUo"

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
        f"Solana • 🟢\n"
        f"Balance: 0 SOL ($0.00)\n"
        f"Wallet: {SOL_WALLET}\n"
        "—\n\n"
        "Thank you for using our bot. ⚠️ "
        "We have no control over ads shown by Telegram in this bot."
    )
    await update.message.reply_text(text, reply_markup=main_keyboard())

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Balance: 0 SOL ($0.00)\nWallet: {SOL_WALLET}"
    )

async def create_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE, chain: str):
    # Použij tvou adresu pro Solanu, pro ostatní demo
    if chain.lower() == "solana":
        wallet = SOL_WALLET
    else:
        wallet = "DEMO_ADDRESS"

    await update.message.reply_text(
        f"🔐 {chain} wallet created (DEMO)\n"
        f"Wallet address: {wallet}\n\n"
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
        "refresh": f"🔄 Refreshed\nBalance: 0 SOL\nWallet: {SOL_WALLET}"
    }

    await q.edit_message_text(
        responses.get(q.data, "Unknown action"),
        reply_markup=main_keyboard()
    )

# Async handlers pro vytvoření peněženky
async def create_wallet_sol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_wallet(update, context, "Solana")

async def create_wallet_eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_wallet(update, context, "Ethereum")

async def create_wallet_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_wallet(update, context, "Bitcoin")

# Build app
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("createwalletsol", create_wallet_sol))
app.add_handler(CommandHandler("createwalleteth", create_wallet_eth))
app.add_handler(CommandHandler("createwalletbtc", create_wallet_btc))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("valuation", valuation))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
