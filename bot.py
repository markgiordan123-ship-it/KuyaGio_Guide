import os
import random
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ---------------- TOKEN (USE RAILWAY VARIABLE) ----------------
TOKEN = os.getenv("TOKEN")

# ---------------- LINKS ----------------
CASINO_LINK = "http://kuyax333.paldopinas96.cc/?referralCode=opl5030"
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"
SUPPORT = "@KuyaGioPaldo"

PH = timezone(timedelta(hours=8))

# ---------------- PROVIDERS ----------------
games = {
    "JILI": [
        "SUPER ACE","GOLDEN EMPIRE","BOXING KING","CRAZY777","MONEY COMING",
        "LUCKY JAGUAR","FORTUNE GEMS","WILD ACE","GOLDEN BANK 2","ZEUS",
        "SUPER ACE DELUXE","FA FA FA","MONEY POT","SEVEN SEVEN SEVEN"
    ],
    "PG": [
        "Mahjong Ways","Mahjong Ways 2","Lucky Neko","Fortune Tiger",
        "Dragon Hatch","Ganesha Gold","Wild Bandito","Treasures of Aztec",
        "Candy Burst","Emoji Riches","Phoenix Rises","Secrets of Cleopatra"
    ],
    "PRAGMATIC": [
        "Sweet Bonanza","Gates of Olympus","Starlight Princess",
        "Wild West Gold","Fruit Party","Big Bass Splash","Wolf Gold",
        "Sugar Rush","Hot Fiesta","Buffalo King"
    ],
    "FA CHAI": [
        "Fa Chai Riches","Golden Monkey","Lucky Twins",
        "Dragon Treasure","Fortune Festival","God of Wealth"
    ]
}

# ---------------- CACHE (STABLE TIME SYSTEM) ----------------
game_cache = {}

def generate_time():
    now = datetime.now(PH)

    start_offset = random.randint(0, 25)
    duration = random.choice([20, 30, 45])

    start = now + timedelta(minutes=start_offset)
    end = start + timedelta(minutes=duration)

    return start, end

def get_game_time(game):
    now = datetime.now(PH)

    if game in game_cache:
        if now < game_cache[game]["expires"]:
            return game_cache[game]["text"]

    start, end = generate_time()
    text = f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"

    game_cache[game] = {
        "text": text,
        "expires": now + timedelta(minutes=30)
    }

    return text

# ---------------- BUILD PROVIDER DATA ----------------
def build_provider(provider):
    shuffled = games[provider][:]
    random.shuffle(shuffled)
    return {g: get_game_time(g) for g in shuffled}

# ---------------- PAGINATION ----------------
def paginate(data, page, per_page=10):
    items = list(data.items())
    total = (len(items) + per_page - 1) // per_page
    return items[page*per_page:(page+1)*per_page], total

# ---------------- UI MESSAGE ----------------
def build_message(provider, data, page):
    chunk, total = paginate(data, page)

    msg = []
    msg.append("🌐 MORE GUIDE IN HERE:\n" + CANVA_LINK)
    msg.append(f"📩 SUPPORT: {SUPPORT}")
    msg.append("⚠️ FOR PHILIPPINES USERS ONLY\n")
    msg.append(f"🎰 {provider} PROVIDER GUIDE\n")

    for g, t in chunk:
        msg.append(f"🎮 {g}\n🕐 {t}\n👉 {CASINO_LINK}\n")

    msg.append(f"📄 Page {page+1}/{total}")

    return "\n".join(msg), total

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[
        InlineKeyboardButton("English", callback_data="lang_EN"),
        InlineKeyboardButton("Tagalog", callback_data="lang_TL")
    ]]
    await update.message.reply_text("Choose language:", reply_markup=InlineKeyboardMarkup(kb))

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data.startswith("lang_"):
        kb = [[InlineKeyboardButton(p, callback_data=f"prov_{p}")] for p in games]
        await q.edit_message_text("Select provider:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("prov_"):
        provider = data.split("_")[1]

        data_map = build_provider(provider)
        msg, total = build_message(provider, data_map, 0)

        kb = [
            [InlineKeyboardButton(str(i+1), callback_data=f"page_{provider}_{i}") for i in range(total)],
            [InlineKeyboardButton("🔄 Refresh HourGuide", callback_data=f"prov_{provider}")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("page_"):
        _, provider, page = data.split("_")
        page = int(page)

        data_map = build_provider(provider)
        msg, total = build_message(provider, data_map, page)

        kb = [
            [InlineKeyboardButton(str(i+1), callback_data=f"page_{provider}_{i}") for i in range(total)],
            [InlineKeyboardButton("🔄 Refresh HourGuide", callback_data=f"prov_{provider}")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))

    elif data == "back":
        kb = [[InlineKeyboardButton(p, callback_data=f"prov_{p}")] for p in games]
        await q.edit_message_text("Select provider:", reply_markup=InlineKeyboardMarkup(kb))

# ---------------- SEARCH ----------------
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.lower()

    for p in games:
        for g in games[p]:
            if txt in g.lower():
                await update.message.reply_text(
                    f"🎮 {g}\n🕐 {get_game_time(g)}\n👉 {CASINO_LINK}"
                )
                return

    await update.message.reply_text("Game not found.")

# ---------------- MAIN ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

app.run_polling()
