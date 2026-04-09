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

games = {
    "JILI": ["SUPER ACE", "GOLDEN EMPIRE", "BOXING KING"],
    "PG": ["Mahjong Ways", "Lucky Neko", "Fortune Tiger"],
    "PRAGMATIC": ["Sweet Bonanza", "Gates of Olympus", "Sugar Rush"]
}

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 JILI", callback_data="JILI"),
         InlineKeyboardButton("🎲 PG", callback_data="PG")],
        [InlineKeyboardButton("🔥 PRAGMATIC", callback_data="PRAGMATIC")]
    ])

def get_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=random.randint(0, 20))
    end = start + timedelta(minutes=30)
    return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎮 GOOD DAY BOSSING!\n\n"
        "Gusto mo ba HourGuide ngayon?\n\n"
        "👇 Pili ka provider"
    )
    await update.message.reply_text(text, reply_markup=menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if anti_spam(q.from_user.id):
        return

    provider = q.data

    if provider in games:
        text = f"🌐 {CANVA_LINK}\n\n📩 {SUPPORT}\n\n🎰 {provider}\n\n"
        for g in games[provider]:
            text += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        await q.edit_message_text(text, reply_markup=menu())

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use buttons only 👇", reply_markup=menu())

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

app.run_polling()
