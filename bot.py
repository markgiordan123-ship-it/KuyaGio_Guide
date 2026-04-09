import os
import random
import time
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"
CASINO_LINK = "https://example.com"
SUPPORT = "@KuyaGioPaldo"

PH = timezone(timedelta(hours=8))

cooldown = {}

def anti_spam(user_id):
    now = time.time()
    if user_id in cooldown and now - cooldown[user_id] < 2:
        return True
    cooldown[user_id] = now
    return False

# ---------------- PROVIDERS ----------------
providers = ["JILI","PG","PRAGMATIC","FA CHAI","BNG","JDB","YELLOW BAT","CO9"]

# ---------------- AUTO GENERATE 50 GAMES EACH ----------------
def generate_games(prefix):
    return [f"{prefix} GAME {i+1}" for i in range(50)]

games = {
    "JILI": generate_games("JILI"),
    "PG": generate_games("PG"),
    "PRAGMATIC": generate_games("PRAG"),
    "FA CHAI": generate_games("FCH"),
    "BNG": generate_games("BNG"),
    "JDB": generate_games("JDB"),
    "YELLOW BAT": generate_games("YBAT"),
    "CO9": generate_games("CO9")
}

# ---------------- MENU ----------------
def menu():
    buttons = []
    row = []

    for i, p in enumerate(providers):
        row.append(InlineKeyboardButton(p, callback_data=p))

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(buttons)

# ---------------- TIME ----------------
def get_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=random.randint(0, 20))
    end = start + timedelta(minutes=30)
    return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 GOOD DAY BOSSING!\n\nSelect provider 👇",
        reply_markup=menu()
    )

# ---------------- BUTTON ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if anti_spam(q.from_user.id):
        return

    provider = q.data

    if provider in games:
        text = f"🎰 {provider}\n\n📘 {CANVA_LINK}\n📩 {SUPPORT}\n\n"

        for g in games[provider]:
            text += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        await q.edit_message_text(text, reply_markup=menu())

# ---------------- TEXT ----------------
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use buttons only 👇", reply_markup=menu())

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
app.run_polling()
