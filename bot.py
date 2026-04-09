import os
import random
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

# ---------------- PROVIDERS ----------------
games = {

"JILI": [
"SUPER ACE","GOLDEN EMPIRE","BOXING KING","CRAZY777","MONEY COMING",
"LUCKY JAGUAR","FORTUNE GEMS","WILD ACE","GOLDEN BANK 2","SHANGHAI BEAUTY",
"ZEUS","SUPER ACE DELUXE","MONEY POT","FA FA FA","JUNGLE KING","NEKO FORTUNE"
],

"PG": [
"Mahjong Ways","Mahjong Ways 2","Lucky Neko","Fortune Tiger","Fortune Ox",
"Dragon Hatch","Ganesha Gold","Wild Bandito","Treasures of Aztec","Medusa",
"Rise of Apollo","Flirting Scholar","Reel Love","Alchemy Gold","Diner Frenzy",
"Garuda Gems","Speed Winner","Dreams of Macau","Emoji Riches","Phoenix Rises"
],

"PRAGMATIC": [
"Sweet Bonanza","Gates of Olympus","Starlight Princess","Sugar Rush",
"Wild West Gold","Big Bass Splash","Big Bass Bonanza","Wolf Gold","Buffalo King",
"Fruit Party","Madame Destiny","Release the Kraken","5 Lions Megaways",
"Extra Juicy","Cash Patrol","Hot Fiesta","Chilli Heat","Neon Staxx","Fire Strike"
],

"FA CHAI": [
"Fa Chai Riches","Golden Monkey","Lucky Twins","Dragon Treasure","Fortune Festival",
"God of Wealth","Golden Panda","Lucky Koi","Prosperity Lion","Five Dragons",
"Dragon King","Money Tree","Golden Dragon","Lucky Lantern","Red Envelope"
],

# ---------------- NEW PROVIDERS YOU REQUESTED ----------------

"BNG": [
"Bonanza Gold","Book of Fortune","Super Marble","Legendary Monkey",
"Shark Hunter","Dragon Power Flame","Wild Tundra","Golden Empire BNG",
"Treasure Island","Ocean King","Super Bingo","Lucky Wheel BNG",
"Fishing Mania","Dragon Fishing","Fortune Cat BNG","Mega Spin",
"Fire Rooster","Golden Dragon BNG","Lucky Panda","Fortune House"
],

"JDB": [
"Dragon Hunter","Fire Phoenix","Money Bang Bang","Fortune Mouse JDB",
"Golden Disco","Candy Burst JDB","Jungle Treasure","Lucky Phoenix",
"Super Kids","Piggy Bank JDB","Golden Shark","Dragon King JDB",
"Fortune Tree JDB","Lucky Star","JDB Fishing","Hot Spin",
"Crazy Money","Golden Rooster","Super Dragon","Fortune Island"
],

"YELLOW BAT": [
"Yellow Bat Riches","Bat Frenzy","Golden Night Bat","Shadow Bat",
"Vampire Bat Gold","Lucky Bat Empire","Bat Treasure","Midnight Bat",
"Golden Cave Bat","Bat King","Dark Bat Fortune","Bat Storm",
"Neon Bat Rush","Lucky Wing Bat","Bat Jackpot","Golden Wing",
"Night Hunter Bat","Bat Galaxy","Shadow Fortune Bat","Mega Bat Spin"
],

"CO9": [
"CO9 Fortune","CO9 Golden Empire","CO9 Lucky Spin","CO9 Dragon Rise",
"CO9 Money Train","CO9 Jungle King","CO9 Mega Jackpot","CO9 Fire Wheel",
"CO9 Treasure Box","CO9 Wild Gold","CO9 Lucky Panda","CO9 Ocean Spin",
"CO9 Fortune Tiger","CO9 Gold Rush","CO9 Neon Luck","CO9 Super Spin",
"CO9 Dragon Gold","CO9 Crystal Win","CO9 Lucky Kingdom","CO9 Mega Win"
]
}

# ---------------- CACHE ----------------
cache = {}

def gen_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=random.randint(0,25))
    end = start + timedelta(minutes=random.choice([20,30,45]))
    return start, end

def get_time(game):
    now = datetime.now(PH)

    if game in cache and now < cache[game]["expires"]:
        return cache[game]["text"]

    s, e = gen_time()
    text = f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}"

    cache[game] = {
        "text": text,
        "expires": now + timedelta(minutes=30)
    }

    return text

# ---------------- BUILD ----------------
def build(provider):
    lst = games[provider][:]
    random.shuffle(lst)
    return {g: get_time(g) for g in lst}

# ---------------- MAIN MENU (APP UI STYLE) ----------------
def main_menu():
    kb = [
        [InlineKeyboardButton("🎰 JILI", callback_data="prov_JILI"),
         InlineKeyboardButton("🎲 PG", callback_data="prov_PG")],

        [InlineKeyboardButton("🔥 PRAGMATIC", callback_data="prov_PRAGMATIC"),
         InlineKeyboardButton("🧧 FA CHAI", callback_data="prov_FA CHAI")],

        [InlineKeyboardButton("⚡ BNG", callback_data="prov_BNG"),
         InlineKeyboardButton("🎮 JDB", callback_data="prov_JDB")],

        [InlineKeyboardButton("🦇 YELLOW BAT", callback_data="prov_YELLOW BAT"),
         InlineKeyboardButton("💎 CO9", callback_data="prov_CO9")]
    ]
    return InlineKeyboardMarkup(kb)

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🎮 GOOD DAY BOSSING!\n\n"
        "Gusto mo ba malaman ang HourGuide ngayon?\n\n"
        "👇 Pili ka ng language"
    )

    kb = [[
        InlineKeyboardButton("English 🇬🇧", callback_data="lang_EN"),
        InlineKeyboardButton("Tagalog 🇵🇭", callback_data="lang_TL")
    ]]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

# ---------------- BUTTONS ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    # LANGUAGE -> MAIN MENU
    if data.startswith("lang_"):
        await q.edit_message_text("🏠 MAIN MENU\nChoose Provider:", reply_markup=main_menu())

    # PROVIDER
    elif data.startswith("prov_"):
        provider = data.replace("prov_", "")
        data_map = build(provider)

        msg = (
            f"🌐 MORE GUIDE:\n{CANVA_LINK}\n\n"
            f"📩 SUPPORT: {SUPPORT}\n"
            f"🎰 {provider} PROVIDER\n\n"
        )

        for g, t in list(data_map.items())[:10]:
            msg += f"🎮 {g}\n🕐 {t}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"prov_{provider}")],
            [InlineKeyboardButton("🏠 Back to Menu", callback_data="back")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))

    # BACK
    elif data == "back":
        await q.edit_message_text("🏠 MAIN MENU\nChoose Provider:", reply_markup=main_menu())

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
