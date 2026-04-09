import os
import random
import time
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

CASINO_LINK = "http://kuyax333.paldopinas96.cc/?referralCode=opl5030"
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"
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

# ---------------- SIMPLE DATA ----------------
games = {
"JILI": ["SUPER ACE","GOLDEN EMPIRE","BOXING KING","CRAZY777","MONEY COMING"],
"PG": ["Mahjong Ways","Lucky Neko","Fortune Tiger","Dragon Hatch","Medusa"],
"PRAGMATIC": ["Sweet Bonanza","Gates of Olympus","Sugar Rush","Big Bass Bonanza","Wolf Gold"]
}

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 JILI", callback_data="JILI"),
         InlineKeyboardButton("🎲 PG", callback_data="PG")],
        [InlineKeyboardButton("🔥 PRAGMATIC", callback_data="PRAGMATIC")]
    ])

def get_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=random.randint(0,20))
    end = start + timedelta(minutes=30)
    return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎮 Bot is back online\nChoose provider:", reply_markup=menu())

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

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use buttons below 👇", reply_markup=menu())

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

app.run_polling()    await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))

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

app.run_polling()"Mahjong Ways","Mahjong Ways 2","Mahjong Ways 3","Lucky Neko","Fortune Tiger",
"Fortune Ox","Fortune Rabbit","Fortune Mouse","Dragon Hatch","Dragon Hatch 2",
"Ganesha Gold","Wild Bandito","Treasures of Aztec","Symbols of Egypt","Rise of Apollo",
"Medusa","Medusa II","Flirting Scholar","Reel Love","Bali Vacation",
"Circus Delight","Plushie Frenzy","Jewels of Prosperity","Opera Dynasty","Heist Stakes",
"Legend of Perseus","Ways of the Qilin","Shaolin Soccer","Hip Hop Panda","Garuda Gems",
"Muay Thai Champion","Mr Hallow-Win","Speed Winner","Alchemy Gold","Dreams of Macau",
"Fortune Gods","Diner Frenzy","Crypto Gold","Emoji Riches","Phoenix Rises",
"Santa’s Gift Rush","Win Win Won","Bikini Paradise","Safari Wilds","Jurassic Kingdom",
"Golden Genie","Lucky Piggy","Mermaid Riches","Dragon Fortune","Wild Safari"
],

"PRAGMATIC": [
"Sweet Bonanza","Gates of Olympus","Starlight Princess","Sugar Rush","Wild West Gold",
"Big Bass Splash","Big Bass Bonanza","Wolf Gold","Buffalo King","Fruit Party",
"Madame Destiny","Release the Kraken","5 Lions Megaways","Extra Juicy","Cash Patrol",
"Hot Fiesta","Chilli Heat","Neon Staxx","Fire Strike","Diamond Strike",
"Ultra Burn","Treasure Wild","Sea of Riches","Vegas Magic","Mystic Fortune",
"Power of Thor","Great Rhino","Aztec Gems","The Dog House","Zombie Carnival",
"Fruit Party 2","Gates of Olympus 1000","Sweet Bonanza Xmas","Sugar Rush 1000",
"Buffalo King Megaways","Wild West Duels","Big Bass Hold Spin","Book of Dead",
"Fire Joker","Lucky Lightning","Super X","Gold Train","Golden Explorer",
"Hot Safari","Mega Wheel","Space Gem","Tropical Wilds","Cash Elevator"
],

"FA CHAI": [
"Fa Chai Riches","Golden Monkey","Lucky Twins","Dragon Treasure","Fortune Festival",
"God of Wealth","Golden Panda","Lucky Koi","Prosperity Lion","Five Dragons",
"Dragon King","Fu Lu Shou","Fortune Ox","Golden Dragon","Lucky Fortune Cat",
"Chinese New Year","Money Tree","Blessed Fortune","Golden Year","Red Envelope",
"Fortune Panda","Lucky Lantern","Imperial Wealth","Jade Emperor","Golden Zodiac",
"Prosperity Gate","Wealth God","Lucky Spring","Dragon Blessing","Fortune Coins",
"Golden Fireworks","Royal Fortune","China Gold","Lucky Empire","Fortune Heaven",
"Golden Dynasty","Lucky Palace","Dragon Gold","Wealth Fortune","Prosperity Luck",
"Golden Prosperity","Fortune Temple","Lucky Emperor","Dragon Blessing 2","Golden Blessing"
],

"BNG": [
"Bonanza Gold","Book of Fortune","Super Marble","Legendary Monkey","Shark Hunter",
"Dragon Power Flame","Wild Tundra","Golden Empire BNG","Treasure Island","Ocean King",
"Super Bingo","Lucky Wheel BNG","Fishing Mania","Dragon Fishing","Fortune Cat BNG",
"Mega Spin","Fire Rooster","Golden Dragon BNG","Lucky Panda","Fortune House",
"Ocean Treasure","Deep Sea King","Wild Catch","Fish Hunter","Golden Fishing",
"Jackpot Fishing","Lucky Ocean","Sea Monster","Mega Fishing","Treasure Catch"
],

"JDB": [
"Dragon Hunter","Fire Phoenix","Money Bang Bang","Fortune Mouse JDB","Golden Disco",
"Candy Burst JDB","Jungle Treasure","Lucky Phoenix","Super Kids","Piggy Bank JDB",
"Golden Shark","Dragon King JDB","Fortune Tree JDB","Lucky Star","JDB Fishing",
"Hot Spin","Crazy Money","Golden Rooster","Super Dragon","Fortune Island",
"Neon Party","Lucky Spin JDB","Mega Boom","Power Win","Golden Rush"
],

"YELLOW BAT": [
"Yellow Bat Riches","Bat Frenzy","Golden Night Bat","Shadow Bat","Vampire Bat Gold",
"Lucky Bat Empire","Bat Treasure","Midnight Bat","Golden Cave Bat","Bat King",
"Dark Bat Fortune","Bat Storm","Neon Bat Rush","Lucky Wing Bat","Bat Jackpot",
"Golden Wing","Night Hunter Bat","Bat Galaxy","Shadow Fortune Bat","Mega Bat Spin",
"Sky Bat","Thunder Bat","Crystal Bat","Moon Bat","Dark Wing"
],

"CO9": [
"CO9 Fortune","CO9 Golden Empire","CO9 Lucky Spin","CO9 Dragon Rise","CO9 Money Train",
"CO9 Jungle King","CO9 Mega Jackpot","CO9 Fire Wheel","CO9 Treasure Box","CO9 Wild Gold",
"CO9 Lucky Panda","CO9 Ocean Spin","CO9 Fortune Tiger","CO9 Gold Rush","CO9 Neon Luck",
"CO9 Super Spin","CO9 Dragon Gold","CO9 Crystal Win","CO9 Lucky Kingdom","CO9 Mega Win",
"CO9 Power Spin","CO9 Lucky Storm","CO9 Golden Rush","CO9 Ultra Win","CO9 Sky Jackpot"
]
}

# ---------------- CACHE (ANTI LAG CORE) ----------------
cache = {}

def gen_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=random.randint(0,25))
    end = start + timedelta(minutes=random.choice([20,30,45]))
    return start, end

def get_time(game):
    now = datetime.now(PH)

    if game in cache:
        if now < cache[game]["expire"]:
            return cache[game]["text"]

    s, e = gen_time()
    text = f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}"

    cache[game] = {
        "text": text,
        "expire": now + timedelta(minutes=30)
    }

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

# ---------------- UI ----------------
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 JILI", callback_data="prov_JILI"),
         InlineKeyboardButton("🎲 PG", callback_data="prov_PG")],

        [InlineKeyboardButton("🔥 PRAGMATIC", callback_data="prov_PRAGMATIC"),
         InlineKeyboardButton("🧧 FA CHAI", callback_data="prov_FA CHAI")],

        [InlineKeyboardButton("⚡ BNG", callback_data="prov_BNG"),
         InlineKeyboardButton("🎮 JDB", callback_data="prov_JDB")],

        [InlineKeyboardButton("🦇 YELLOW BAT", callback_data="prov_YELLOW BAT"),
         InlineKeyboardButton("💎 CO9", callback_data="prov_CO9")]
    ])

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
