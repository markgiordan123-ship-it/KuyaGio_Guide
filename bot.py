import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ---- CONFIG ----
TOKEN = "8577695558:AAEm8ZtcjqYYPbqo576JlwNkmJrytYycb_g"
CASINO_LINK = "http://kuyax333.paldopinas96.cc/?referralCode=opl5030"
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"

# 🔥 EXPANDED GAME LIST
games = {
    "JILI": [
        "Super Ace Deluxe","Mega Ace","Golden Empire","Lucky Dragon",
        "Fortune Gems","Money Coming","Crazy FaFaFa","Golden Bank"
    ],
    "PG": [
        "Mahjong Ways","Mahjong Ways 2","Lucky Neko","Treasure Hunt",
        "Dragon Legend","Wild Bandito","Candy Burst","Fortune Tiger"
    ],
    "CQ9": [
        "Fire Phoenix","Golden Rooster","Fortune King","Mystery Temple",
        "Dragon Ball","Zeus","Jump High","God of War"
    ],
    "Pragmatic": [
        "Sweet Bonanza","The Dog House","Wild West Gold","Great Rhino",
        "Gates of Olympus","Starlight Princess","Big Bass Splash","Fruit Party"
    ]
}

user_lang = {}

# --- FUNCTIONS ---
def gen_time():
    h = random.randint(8, 21)
    m = random.choice([0,10,20,30,40,50])
    me = m + 20
    if me >= 60:
        me -= 60
        h += 1
    p = "AM" if h < 12 else "PM"
    h12 = h if h <= 12 else h - 12
    return f"{h12}:{m:02d} {p} - {h12}:{me:02d} {p}"

def generate_provider(provider):
    """Generate NEW times EVERY CLICK"""
    data = {}
    for game in games[provider]:
        data[game] = gen_time()
    return data

def get_msg(provider, lang, data):
    msg = []
    
    # ✅ Canva FIRST
    msg.append("🌐 MORE GUIDE IN HERE:\n" + CANVA_LINK)
    msg.append("")
    
    msg.append(f"🎰 {provider} GUIDE 🎰" if lang=="EN" else f"🎰 {provider} ORAS NG LARO 🎰")
    
    for game, time in data.items():
        msg.append(f"🎮 {game}\n🕐 {time}\n👉 {CASINO_LINK}")
    
    return "\n\n".join(msg)

# --- HANDLERS ---
async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    user_lang[uid] = None

    kb = [[
        InlineKeyboardButton("English", callback_data="lang_EN"),
        InlineKeyboardButton("Tagalog", callback_data="lang_TL")
    ]]
    
    await update.message.reply_text(
        "Choose your language / Piliin ang wika:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def button(update:Update, context:ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    
    data = q.data
    uid = q.from_user.id

    if data.startswith("lang_"):
        user_lang[uid] = data.split("_")[1]

        kb = [[InlineKeyboardButton(p, callback_data=f"prov_{p}")] for p in games.keys()]
        
        await q.edit_message_text(
            "Select provider:" if user_lang[uid]=="EN" else "Pumili ng provider:",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    elif data.startswith("prov_"):
        prov = data.split("_")[1]
        lang = user_lang.get(uid, "EN")

        # 🔥 FIX: Generate NEW DATA EVERY CLICK
        provider_data = generate_provider(prov)

        msg = get_msg(prov, lang, provider_data)

        kb = [[InlineKeyboardButton("HourGuide 🔄", callback_data=f"prov_{prov}")]]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))

async def text(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please use /start to begin.")

# --- MAIN ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

app.run_polling()
