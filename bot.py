import os
import time
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------------- TOKEN ----------------
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise Exception("Missing TOKEN")

CASINO_LINK = "https://example.com"
PH = timezone(timedelta(hours=8))

# ---------------- ULTRA SMOOTH CLICK ----------------
click_cache = {}

def smooth_click(uid, action):
    now = time.time()
    key = f"{uid}:{action}"
    last = click_cache.get(key, 0)

    if now - last < 0.12:
        return False

    click_cache[key] = now
    return True

# ---------------- 8 PROVIDERS x 50 GAMES ----------------
def gen(prefix):
    return [f"{prefix} Game {i+1}" for i in range(50)]

games = {
    "JILI": gen("JILI"),
    "PG": gen("PG"),
    "PRAGMATIC": gen("PRAGMATIC"),
    "FA CHAI": gen("FA CHAI"),
    "BNG": gen("BNG"),
    "JDB": gen("JDB"),
    "YELLOW BAT": gen("YELLOW BAT"),
    "CO9": gen("CO9")
}

# ---------------- PAGINATION ----------------
PAGE_SIZE = 10

def paginate(items, page):
    start = page * PAGE_SIZE
    return items[start:start + PAGE_SIZE]

def max_page(provider):
    return max(0, (len(games[provider]) - 1) // PAGE_SIZE)

# ---------------- MENU ----------------
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("JILI", callback_data="JILI"),
         InlineKeyboardButton("PG", callback_data="PG")],
        [InlineKeyboardButton("PRAGMATIC", callback_data="PRAGMATIC"),
         InlineKeyboardButton("FA CHAI", callback_data="FA CHAI")],
        [InlineKeyboardButton("BNG", callback_data="BNG"),
         InlineKeyboardButton("JDB", callback_data="JDB")],
        [InlineKeyboardButton("YELLOW BAT", callback_data="YELLOW BAT"),
         InlineKeyboardButton("CO9", callback_data="CO9")]
    ])

# ---------------- TIME ----------------
def get_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=5)
    end = start + timedelta(minutes=30)
    return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎮 Welcome Bossing!", reply_markup=menu())

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = q.from_user.id
    data = q.data

    if not smooth_click(uid, data):
        return

    # ---------------- PROVIDER ----------------
    if data in games:
        page = 0
        items = paginate(games[data], page)
        maxp = max_page(data)

        msg = f"🎰 {data}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n\n"

        # 🔥 REQUIRED FINAL LINE ONLY
        msg += f"\n🚫 RESTRICTED THIS ONLY LINK WORKS\n{CASINO_LINK}"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data="noop"),
                InlineKeyboardButton(f"1/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{data}_1")
            ],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=kb)
        return

    # ---------------- PAGINATION ----------------
    if data.startswith("page_"):
        _, provider, page = data.split("_")
        page = int(page)

        items = paginate(games[provider], page)
        maxp = max_page(provider)

        msg = f"🎰 {provider}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n\n"

        msg += f"\n🚫 RESTRICTED THIS ONLY LINK WORKS\n{CASINO_LINK}"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{provider}_{max(0,page-1)}"),
                InlineKeyboardButton(f"{page+1}/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{provider}_{min(maxp,page+1)}")
            ],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=kb)
        return

    if data == "menu":
        await q.edit_message_text("🏠 Menu", reply_markup=menu())

    if data == "noop":
        return

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
