import os
import random
import time
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ---------------- TOKEN ----------------
TOKEN = os.getenv("TOKEN")

# ---------------- LINKS ----------------
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"
CASINO_LINK = "https://example.com"
SUPPORT = "@KuyaGioPaldo"

PH = timezone(timedelta(hours=8))

# ---------------- SIMPLE ANTI-SPAM ----------------
cooldown = {}

def anti_spam(user_id):
    now = time.time()
    if user_id in cooldown and now - cooldown[user_id] < 2:
        return True
    cooldown[user_id] = now
    return False

# ---------------- SIMPLE GAME DATA ----------------
games = {
    "JILI": ["SUPER ACE", "GOLDEN EMPIRE", "BOXING KING"],
    "PG": ["Mahjong Ways", "Lucky Neko", "Fortune Tiger"],
    "PRAGMATIC": ["Sweet Bonanza", "Gates of Olympus", "Sugar Rush"]
}

# ---------------- MENU ----------------
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 JILI", callback_data="JILI"),
         InlineKeyboardButton("🎲 PG", callback_data="PG")],
        [InlineKeyboardButton("🔥 PRAGMATIC", callback_data="PRAGMATIC")]
    ])

# ---------------- TIME SYSTEM ----------------
def get_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=random.randint(0, 20))
    end = start + timedelta(minutes=30)
    return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 BOT RESET SUCCESSFULLY\nChoose provider 👇",
        reply_markup=menu()
    )

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if anti_spam(q.from_user.id):
        return

    provider = q.data

    if provider in games:
        text = f"🎰 {provider}\n\n📘 {CANVA_LINK}\n\n"
        for g in games[provider]:
            text += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        await q.edit_message_text(text, reply_markup=menu())

# ---------------- TEXT HANDLER ----------------
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use buttons only 👇", reply_markup=menu())

# ---------------- RUN BOT ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

app.run_polling() callback_data="prov_CO9")]
    

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🎮 GOOD DAY BOSSING!\n\n"
        "Gusto mo ba HourGuide ngayon?\n\n"
        "👇 Pili ka language"
    )

    kb = [[
        InlineKeyboardButton("English 🇬🇧", callback_data="lang_EN"),
        InlineKeyboardButton("Tagalog 🇵🇭", callback_data="lang_TL")
    ]]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

# ---------------- HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    # language -> menu
    if data.startswith("lang_"):
        await q.edit_message_text("🏠 MAIN MENU", reply_markup=menu())

    # provider
    elif data.startswith("prov_"):
        provider = data.replace("prov_", "")
        page = 0

        data_map = build(provider)
        page_items = paginate(data_map, page)
        maxp = max_page(provider)

        msg = f"🌐 {CANVA_LINK}\n\n📩 {SUPPORT}\n\n🎰 {provider}\n\n"

        for g, t in page_items:
            msg += f"🎮 {g}\n🕐 {t}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{provider}_{max(0,page-1)}"),
                InlineKeyboardButton(f"{page+1}/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{provider}_{page+1}")
            ],
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"prov_{provider}")],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))

    # pagination
    elif data.startswith("page_"):
        _, provider, page = data.split("_")
        page = int(page)

        data_map = build(provider)
        page_items = paginate(data_map, page)
        maxp = max_page(provider)

        msg = f"🌐 {CANVA_LINK}\n\n📩 {SUPPORT}\n\n🎰 {provider}\n\n"

        for g, t in page_items:
            msg += f"🎮 {g}\n🕐 {t}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{provider}_{max(0,page-1)}"),
                InlineKeyboardButton(f"{page+1}/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{provider}_{page+1}")
            ],
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"prov_{provider}")],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu":
        await q.edit_message_text("🏠 MAIN MENU", reply_markup=menu())

# ---------------- SEARCH ----------------
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.lower()

    for p in games:
        for g in games[p]:
            if txt in g.lower():
                await update.message.reply_text(
                    f"🎮 {g}\n🕐 {get_time(g)}\n👉 {CASINO_LINK}"
                )
                return

    await update.message.reply_text("Game not found.")

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

app.run_polling()
