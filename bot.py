import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ---- CONFIG ----
TOKEN = "8577695558:AAEm8ZtcjqYYPbqo576JlwNkmJrytYycb_g"
CASINO_LINK = "http://kuyax333.paldopinas96.cc/?referralCode=opl5030"
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"
SUPPORT = "@KuyaGioPaldo"

# ---- PROVIDERS ----
games = {
    "JILI": [
        "SUPER ACE","GOLDEN EMPIRE","BOXING KING","CRAZY777","MONEY COMING",
        "LUCKY JAGUAR","FORTUNE GEMS","WILD ACE","GOLDEN BANK","ZEUS","SUPER ACE DELUXE"
    ],
    "PG": [
        "Mahjong Ways","Mahjong Ways 2","Lucky Neko","Fortune Tiger","Dragon Hatch",
        "Ganesha Gold","Wild Bandito","Treasures of Aztec"
    ],
    "PRAGMATIC": [
        "Sweet Bonanza","Gates of Olympus","Starlight Princess",
        "Wild West Gold","Fruit Party","Big Bass Splash"
    ],
    "FA CHAI": [
        "Fa Chai Riches","Golden Monkey","Lucky Twins","Dragon Treasure"
    ]
}

# --- REAL-TIME GENERATOR ---
def gen_time():
    now = datetime.now()

    # random offset (past or future)
    start_offset = random.randint(-30, 30)
    end_offset = start_offset + random.randint(15, 25)

    start_time = now + timedelta(minutes=start_offset)
    end_time = now + timedelta(minutes=end_offset)

    return f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}"

# --- GENERATE DATA ---
def generate(provider):
    lst = games[provider][:]
    random.shuffle(lst)

    data = {g: gen_time() for g in lst}
    hot = random.sample(lst, min(3, len(lst)))

    return data, hot

# --- PAGINATION ---
def paginate(data, page=0, per_page=10):
    items = list(data.items())
    total_pages = (len(items) + per_page - 1) // per_page
    return items[page*per_page:(page+1)*per_page], total_pages

# --- MESSAGE ---
def build_msg(provider, data, hot, page):
    chunk, total_pages = paginate(data, page)

    msg = []
    msg.append("🌐 MORE GUIDE IN HERE:\n" + CANVA_LINK)
    msg.append(f"📩 NEED HELP? {SUPPORT}")
    msg.append("⚠️ FOR PALDOPINAS USERS ONLY!")
    msg.append("")

    msg.append(f"🔥 HOT GAMES ({provider})")
    for g in hot:
        msg.append(f"⭐ {g}")

    msg.append("")
    msg.append(f"🎰 {provider} PROVIDER 🎰")

    for g, t in chunk:
        msg.append(f"🎮 {g}\n🕐 {t}\n👉 {CASINO_LINK}")

    msg.append(f"\n📄 Page {page+1}/{total_pages}")

    return "\n\n".join(msg), total_pages

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[
        InlineKeyboardButton("English", callback_data="lang_EN"),
        InlineKeyboardButton("Tagalog", callback_data="lang_TL")
    ]]
    await update.message.reply_text("Choose language:", reply_markup=InlineKeyboardMarkup(kb))

# --- BUTTON ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data

    if d.startswith("lang_"):
        kb = [[InlineKeyboardButton(p, callback_data=f"prov_{p}")] for p in games]
        await q.edit_message_text("Select provider:", reply_markup=InlineKeyboardMarkup(kb))

    elif d.startswith("prov_"):
        prov = d.split("_")[1]
        data, hot = generate(prov)

        msg, total_pages = build_msg(prov, data, hot, 0)

        buttons = [
            [InlineKeyboardButton(str(i+1), callback_data=f"page_{prov}_{i}") for i in range(total_pages)],
            [InlineKeyboardButton("HourGuide 🔄", callback_data=f"prov_{prov}")],
            [InlineKeyboardButton("Change Provider 🔘", callback_data="back")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

    elif d.startswith("page_"):
        _, prov, page = d.split("_")
        page = int(page)

        data, hot = generate(prov)
        msg, total_pages = build_msg(prov, data, hot, page)

        buttons = [
            [InlineKeyboardButton(str(i+1), callback_data=f"page_{prov}_{i}") for i in range(total_pages)],
            [InlineKeyboardButton("HourGuide 🔄", callback_data=f"prov_{prov}")],
            [InlineKeyboardButton("Change Provider 🔘", callback_data="back")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

    elif d == "back":
        kb = [[InlineKeyboardButton(p, callback_data=f"prov_{p}")] for p in games]
        await q.edit_message_text("Select provider:", reply_markup=InlineKeyboardMarkup(kb))

# --- SEARCH ---
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.lower()

    for p in games:
        for g in games[p]:
            if txt in g.lower():
                await update.message.reply_text(
                    f"🎮 {g}\n🕐 {gen_time()}\n👉 {CASINO_LINK}"
                )
                return

    await update.message.reply_text("Game not found.")

# --- MAIN ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

app.run_polling()
