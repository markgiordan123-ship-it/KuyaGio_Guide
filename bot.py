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

# ---------------- ANTI-SPAM ----------------
cooldown = {}

def anti_spam(user_id):
    now = time.time()
    if user_id in cooldown and now - cooldown[user_id] < 2:
        return True
    cooldown[user_id] = now
    return False

# ---------------- GAME DATA (50 EACH SAFE) ----------------
def expand(base, prefix):
    return base + [f"{prefix} Game {i+1}" for i in range(40)]

games = {
"JILI": expand(["Super Ace","Golden Empire","Boxing King","Crazy777","Money Coming"], "JILI"),
"PG": expand(["Mahjong Ways 1","Mahjong Ways 2","Lucky Neko","Fortune Tiger","Dragon Hatch"], "PG"),
"PRAGMATIC": expand(["Gates of Olympus","Sweet Bonanza","Sugar Rush","Big Bass","Wolf Gold"], "PRAG"),
"FA CHAI": expand(["Fa Chai Fortune","Golden Monkey","Lucky Panda","Dragon Fortune"], "FCH"),
"BNG": expand(["Book of Fortune","Bonanza Gold","Super Marble","Dragon Fishing"], "BNG"),
"JDB": expand(["Dragon Hunter","Fire Phoenix","Money Bang Bang","Golden Disco"], "JDB"),
"YELLOW BAT": expand(["Bat Frenzy","Golden Night Bat","Shadow Bat","Neon Rush"], "YBAT"),
"CO9": expand(["CO9 Fortune","Golden Empire","Lucky Spin","Dragon Rise"], "CO9")
}

providers = list(games.keys())

# ---------------- UI MENU ----------------
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 JILI", callback_data="prov_JILI"),
         InlineKeyboardButton("🎲 PG", callback_data="prov_PG")],
        [InlineKeyboardButton("🔥 PRAGMAT", callback_data="prov_PRAGMATIC"),
         InlineKeyboardButton("🧧 FA CHAI", callback_data="prov_FA CHAI")],
        [InlineKeyboardButton("⚡ BNG", callback_data="prov_BNG"),
         InlineKeyboardButton("🎮 JDB", callback_data="prov_JDB")],
        [InlineKeyboardButton("🦇 YELLOW BAT", callback_data="prov_YELLOW BAT"),
         InlineKeyboardButton("💎 CO9", callback_data="prov_CO9")],
        [InlineKeyboardButton("🔍 SEARCH GAME", callback_data="search")]
    ])

# ---------------- TIME ----------------
def get_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=random.randint(0, 20))
    end = start + timedelta(minutes=30)
    return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"

# ---------------- PAGINATION ----------------
PER_PAGE = 10

def paginate(items, page):
    start = page * PER_PAGE
    end = start + PER_PAGE
    return items[start:end], page

def max_page(provider):
    return len(games[provider]) // PER_PAGE

# ---------------- START UI ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎮 GOOD DAY BOSSING!\n\n"
        "Gusto mo ba HourGuide ngayon?\n\n"
        "👇 Pili ka provider"
    )
    await update.message.reply_text(text, reply_markup=menu())

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if anti_spam(q.from_user.id):
        return

    data = q.data

    # ---------------- SEARCH MODE ----------------
    if data == "search":
        await q.edit_message_text("🔍 Send game name in chat.")
        return

    # ---------------- PROVIDER ----------------
    if data.startswith("prov_"):
        provider = data.replace("prov_", "")
        page = 0

        items, _ = paginate(games[provider], page)
        maxp = max_page(provider)

        msg = f"🌐 {CANVA_LINK}\n\n📩 {SUPPORT}\n\n🎰 {provider}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{provider}_{page-1}"),
                InlineKeyboardButton(f"{page+1}/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{provider}_{page+1}")
            ],
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"prov_{provider}")],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))

    # ---------------- PAGINATION ----------------
    elif data.startswith("page_"):
        _, provider, page = data.split("_")
        page = int(page)

        items, _ = paginate(games[provider], page)
        maxp = max_page(provider)

        msg = f"🌐 {CANVA_LINK}\n\n📩 {SUPPORT}\n\n🎰 {provider}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{provider}_{page-1}"),
                InlineKeyboardButton(f"{page+1}/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{provider}_{page+1}")
            ],
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"prov_{provider}")],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu":
        await q.edit_message_text("🏠 MAIN MENU", reply_markup=menu())

# ---------------- SEARCH FUNCTION ----------------
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.lower()

    for p in games:
        for g in games[p]:
            if txt in g.lower():
                await update.message.reply_text(
                    f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}"
                )
                return

    await update.message.reply_text("Game not found.", reply_markup=menu())

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
app.run_polling()
