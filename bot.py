import os
import random
import time
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ---------------- TOKEN ----------------
TOKEN = os.getenv("TOKEN")

# ---------------- LINKS ----------------
CASINO_LINK = "http://kuyax333.paldopinas96.cc/?referralCode=opl5030"
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"
SUPPORT = "@KuyaGioPaldo"

PH = timezone(timedelta(hours=8))

PER_PAGE = 10
COOLDOWN = 2  # seconds anti-spam

# ---------------- ANTI-SPAM MEMORY ----------------
user_cooldown = {}

def check_spam(user_id):
    now = time.time()
    if user_id in user_cooldown:
        if now - user_cooldown[user_id] < COOLDOWN:
            return True
    user_cooldown[user_id] = now
    return False

# ---------------- GAME DATABASE ----------------
games = {
"JILI": ["SUPER ACE","GOLDEN EMPIRE","BOXING KING","CRAZY777","MONEY COMING","LUCKY JAGUAR","FORTUNE GEMS","WILD ACE","GOLDEN BANK 2","SHANGHAI BEAUTY"] * 5,
"PG": ["Mahjong Ways","Lucky Neko","Fortune Tiger","Dragon Hatch","Ganesha Gold","Wild Bandito","Treasures of Aztec","Medusa","Rise of Apollo","Flirting Scholar"] * 5,
"PRAGMATIC": ["Sweet Bonanza","Gates of Olympus","Starlight Princess","Sugar Rush","Big Bass Bonanza","Wolf Gold","Buffalo King","Fruit Party","Madame Destiny","Hot Fiesta"] * 5,
"FA CHAI": ["Golden Monkey","Lucky Twins","Dragon Treasure","Fortune Festival","God of Wealth","Golden Panda","Lucky Koi","Five Dragons","Money Tree","Red Envelope"] * 5,
"BNG": ["Bonanza Gold","Book of Fortune","Super Marble","Legendary Monkey","Shark Hunter","Dragon Fishing","Ocean King","Lucky Wheel BNG","Fire Rooster","Treasure Island"] * 5,
"JDB": ["Dragon Hunter","Fire Phoenix","Money Bang Bang","Golden Disco","Candy Burst JDB","Lucky Star","Super Dragon","Hot Spin","Fortune Island","Crazy Money"] * 5,
"YELLOW BAT": ["Yellow Bat Riches","Bat Frenzy","Golden Night Bat","Shadow Bat","Vampire Bat Gold","Lucky Bat Empire","Bat Treasure","Midnight Bat","Bat King","Neon Bat Rush"] * 5,
"CO9": ["CO9 Fortune","Golden Empire CO9","Lucky Spin CO9","Dragon Rise CO9","Money Train CO9","Jungle King CO9","Mega Win CO9","Fire Wheel CO9","Treasure Box CO9","Wild Gold CO9"] * 5
}

# ---------------- CACHE SYSTEM ----------------
cache = {}

def gen_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=random.randint(0,25))
    end = start + timedelta(minutes=random.choice([20,30,45]))
    return start, end

def get_time(game):
    now = datetime.now(PH)

    if game in cache and now < cache[game]["exp"]:
        return cache[game]["text"]

    s, e = gen_time()
    text = f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}"

    cache[game] = {"text": text, "exp": now + timedelta(minutes=30)}
    return text

# ---------------- BUILD ----------------
def build(provider):
    lst = games[provider][:]
    random.shuffle(lst)
    return {g: get_time(g) for g in lst}

# ---------------- PAGINATION ----------------
def paginate(items, page):
    items = list(items.items())
    start = page * PER_PAGE
    end = start + PER_PAGE
    return items[start:end]

def max_page(provider):
    return (len(games[provider]) - 1) // PER_PAGE

# ---------------- MENU ----------------
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 JILI", callback_data="prov_JILI"),
         InlineKeyboardButton("🎲 PG", callback_data="prov_PG")],
        [InlineKeyboardButton("🔥 PRAGMATIC", callback_data="prov_PRAGMATIC"),
         InlineKeyboardButton("🧧 FA CHAI", callback_data="prov_FA CHAI")],
        [InlineKeyboardButton("⚡ BNG", callback_data="prov_BNG"),
         InlineKeyboardButton("🎮 JDB", callback_data="prov_JDB")],
        [InlineKeyboardButton("🦇 YELLOW BAT", callback_data="prov_YELLOW BAT"),
         InlineKeyboardButton("💎 CO9", callback_data="prov_CO9")],
        [InlineKeyboardButton("🔍 SEARCH", callback_data="search")]
    ])

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 SUPER ULTIMATE BOT ONLINE\n\nSelect option below 👇",
        reply_markup=menu()
    )

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    user_id = q.from_user.id

    # ANTI-SPAM CHECK
    if check_spam(user_id):
        return

    data = q.data

    # MENU
    if data == "menu":
        await q.edit_message_text("🏠 MAIN MENU", reply_markup=menu())

    # SEARCH
    elif data == "search":
        await q.edit_message_text("🔍 Send game name in chat.")

    # PROVIDER PAGE 0
    elif data.startswith("prov_"):
        provider = data.replace("prov_", "")
        page = 0

        data_map = build(provider)
        page_items = paginate(data_map, page)
        maxp = max_page(provider)

        msg = f"🎰 {provider}\n📩 {SUPPORT}\n\n📘 {CANVA_LINK}\n\n"

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

    # PAGINATION
    elif data.startswith("page_"):
        _, provider, page = data.split("_")
        page = int(page)

        data_map = build(provider)
        page_items = paginate(data_map, page)
        maxp = max_page(provider)

        msg = f"🎰 {provider}\n📩 {SUPPORT}\n\n📘 {CANVA_LINK}\n\n"

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

# ---------------- SEARCH TEXT ----------------
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.lower()

    for p in games:
        for g in games[p]:
            if txt in g.lower():
                await update.message.reply_text(
                    f"🎮 {g}\n🕐 {get_time(g)}\n👉 {CASINO_LINK}"
                )
                return

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

app.run_polling()
