import os
import time
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ---------------- TOKEN ----------------
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise Exception("Missing TOKEN")

# ---------------- LINKS ----------------
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"
CASINO_LINK = "https://example.com"
ADMIN = "kuyagiopaldo"

PH = timezone(timedelta(hours=8))

# ---------------- ANTI SPAM ----------------
cooldown = {}

def anti_spam(uid):
    now = time.time()
    if uid in cooldown and now - cooldown[uid] < 1.2:
        return True
    cooldown[uid] = now
    return False

# ---------------- GAME DATA ----------------
games = { ... }  # 👈 SAME DATA (not changed to avoid breaking your system)

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
         InlineKeyboardButton("CO9", callback_data="CO9")],
        [InlineKeyboardButton("🔍 SEARCH", callback_data="search")]
    ])

# ---------------- TIME ----------------
def get_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=5)
    end = start + timedelta(minutes=30)
    return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username

    text = (
        "🎮 GOOD DAY BOSSING!\n\n"
        "Gusto mo ba HourGuide ngayon?\n\n"
        "👇 Pili ka provider"
    )

    await update.message.reply_text(text, reply_markup=menu())

# ---------------- ADMIN PANEL ----------------
async def admin_panel(update: Update):
    if update.message.from_user.username != ADMIN:
        await update.message.reply_text("❌ No access")
        return

    total_games = sum(len(v) for v in games.values())

    await update.message.reply_text(
        f"🛠 ADMIN PANEL\n\n"
        f"👤 Admin: @{ADMIN}\n"
        f"🎮 Total Games: {total_games}\n"
        f"📦 Providers: {len(games)}"
    )

# ---------------- SEARCH ----------------
def search_game(query):
    results = []
    for p in games:
        for g in games[p]:
            if query.lower() in g.lower():
                results.append((p, g))
    return results[:10]

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if anti_spam(q.from_user.id):
        return

    data = q.data

    # ---------------- MENU ----------------
    if data == "menu":
        await q.edit_message_text("🏠 Menu", reply_markup=menu())
        return

    # ---------------- PROVIDER ----------------
    if data in games:
        page = 0
        items = paginate(games[data], page)
        maxp = max_page(data)

        msg = f"🎰 {data}\n\nGuide: {CANVA_LINK}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data="noop"),
                InlineKeyboardButton(f"1/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{data}_1")
            ],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))
        return

    # ---------------- PAGINATION ----------------
    if data.startswith("page_"):
        _, provider, page = data.split("_")
        page = int(page)

        items = paginate(games[provider], page)
        maxp = max_page(provider)

        msg = f"🎰 {provider}\n\nGuide: {CANVA_LINK}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{provider}_{max(0,page-1)}"),
                InlineKeyboardButton(f"{page+1}/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{provider}_{min(maxp,page+1)}")
            ],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))
        return

    # ---------------- SEARCH MODE ----------------
    if data == "search":
        await q.edit_message_text("🔍 Send a game name to search")
        context.user_data["search"] = True
        return

    # ---------------- NOOP ----------------
    if data == "noop":
        return

# ---------------- TEXT HANDLER ----------------
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.username == ADMIN and update.message.text.startswith("/admin"):
        await admin_panel(update)
        return

    if context.user_data.get("search"):
        query = update.message.text
        results = search_game(query)

        if not results:
            await update.message.reply_text("❌ No game found")
            return

        msg = "🔍 SEARCH RESULTS\n\n"
        for p, g in results:
            msg += f"🎰 {p}\n🎮 {g}\n\n"

        await update.message.reply_text(msg)
        return

    await update.message.reply_text("Use menu 👇", reply_markup=menu())

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

app.run_polling()
