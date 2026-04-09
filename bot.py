import os
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

ADMIN_USERNAME = "kuyagiopaldo"

PH = timezone(timedelta(hours=8))

# ---------------- ANTI SPAM ----------------
cooldown = {}

def anti_spam(uid):
    now = time.time()
    if uid in cooldown and now - cooldown[uid] < 2:
        return True
    cooldown[uid] = now
    return False

# ---------------- GAME DATA (50 EACH) ----------------
games = {
"JILI": [
"Super Ace","Golden Empire","Boxing King","Crazy777","Money Coming","Lucky Jaguar",
"Fortune Gems","Wild Ace","Golden Bank 2","Shōgun","3 Lucky Pigs","3 Coin Treasures",
"Nightfall Hunting","Money Pot","Fruity Wheel","Aztec Priestess","Bangla Beauty",
"Go For Champion","Egypt Glow","Magic Lamp","Night City","Legacy of Egypt",
"Pirate Queen","Golden Temple","Jackpot Joker","Candy Baby","Mines Gold",
"Lucky Goldbricks","Bonus Hunter","Party Star","King Arthur","War Dragons",
"Book of Gold","Sweet Land","Boxing Extravaganza","Sin City","Golden Bank",
"Pharaoh Treasure","Witches Night","Arena Fighter","Lucky Doggy","Fortune Tree",
"Bone Fortune","Golden Queen","Master Tiger","Jungle King","Samba","Golden Joker"
],

"PG": [
"Mahjong Ways 1","Mahjong Ways 2","Lucky Neko","Fortune Tiger","Dragon Hatch",
"Wild Bandito","Treasures of Aztec","Ganesha Gold","Medusa","Symbol of Egypt",
"Hood vs Wolf","Rooster Rumble","Win Win Fish","Garuda Gems","Bikini Paradise",
"Double Fortune","Crypto Gold","Dragon Legend","Candy Burst","Phoenix Rises",
"Santa's Gift Rush","Heist Stakes","Wild Coaster","Journey to the Wealth",
"Dragon Tiger Luck","Fortune Mouse","Alchemy Gold","Captain's Bounty",
"Mermaid Riches","Jurassic Kingdom","Vampire Night","Emoji Riches",
"Shark Hunter","Bali Vacation","Piggy Gold","Opera Dynasty","Wild Fireworks",
"Legend of Perseus","Leprechaun Riches","Bikini Paradise 2","Crypto Panda",
"Buffalo Win","Mahjong Ways 3","Golden Pig","Lucky Clover","Supermarket Spree",
"Mahjong Royal","Fortune Rabbit","Candy Bonanza"
],

"PRAGMATIC": [
"Gates of Olympus","Sweet Bonanza","Sugar Rush","Big Bass Bonanza","Wolf Gold",
"The Dog House","Wild West Gold","Buffalo King","Madame Destiny","Fire Strike",
"Aztec Gems","John Hunter","Release the Kraken","Hot Safari","Extra Juicy",
"Fruit Party","Sugar Rush 1000","Sweet Bonanza Xmas","Gates of Olympus 1000",
"Starlight Princess","Power of Thor","Viking Forge","The Hand of Midas",
"Caishen's Gold","Chilli Heat","5 Lions Megaways","Mustang Gold",
"Madame Destiny Megaways","Bronco Spirit","Cowboy Coins","Pixie Wings",
"Aztec King","Wild Walker","Cosmic Cash","Treasure Wild","Fruit Party 2",
"Gates of Hades","Sweet Powernudge","Bigger Bass Bonanza","Black Bull",
"Gold Party","Fire Hot 40","Lucky Lightning","Magic Money Maze","Super X",
"Vegas Nights","Ultra Hold","Mystery Symbols","Golden Odyssey"
],

"FA CHAI": [
"Fa Chai Fortune","Golden Monkey","Lucky Panda","Dragon Fortune","Money Tree",
"Fortune Festival","Golden Dragon","Lucky Coins","Red Packet Rush","Oriental Gold",
"Prosperity Tiger","Fortune Ox","Lucky Dragon Spin","Golden Prosperity",
"Rich Harvest","China Gold","Red Lantern Luck","Mandarin Treasure",
"Golden Bamboo","Lucky Phoenix","Dragon Wealth","Fortune Dynasty",
"Imperial Gold","Red Dragon Rise","Golden Panda Rush","Fortune Emperor",
"Dragon Blessing","Lucky Zodiac","Golden Temple Luck","Money Rain Asia",
"Fortune Bloom","Golden Dynasty","Asia Fortune","Lucky Spring Festival",
"Golden Empire Asia","Fortune Tiger Asia","Dragon Fortune 2","Lucky Harvest",
"Prosperity Spin","Golden Luck Wheel","Red Fortune Path","Mandarin Gold Rush",
"Asia Lucky Star","Golden Festival","Fortune Cloud","Dragon Prosperity",
"Golden Asia Win","Lucky Red Gold","Imperial Fortune","Golden Prosperity 2"
],

"BNG": [
"Book of Fortune","Bonanza Gold","Super Marble","Dragon Fishing","Ocean King",
"Shark Hunter","Fire Rooster","Treasure Island","Lucky Fishing","Golden Crab",
"Deep Sea Adventure","Ocean Treasure","Golden Whale","Fish Hunter Pro",
"Ocean King 2","Mega Fishing","Sea Fortune","Dragon Ocean","Pirate Catch",
"Golden Reef","Lucky Ocean Spin","Fish King","Ocean Gold Rush","Treasure Fish",
"Shark Attack","Golden Sea Battle","Deep Sea Gold","Ocean Storm","Fish Master",
"Sea King","Golden Fisher","Ocean Jackpot","Lucky Catch","Sea Treasure",
"Ocean Empire","Fish Bonanza","Golden Wave","Deep Sea Fortune","Sea Dragon",
"Ocean Spin King","Treasure Hunter Sea","Fish Wealth","Golden Ocean Win",
"Sea Gold Rush","Ocean Legend","Fish Empire","Deep Sea King","Ocean Big Win",
"Golden Fishing Pro","Sea Fortune 2"
],

"JDB": [
"Dragon Hunter","Fire Phoenix","Money Bang Bang","Golden Disco","Candy Burst",
"Super Dragon","Hot Spin","Fortune Island","Mega Spin","Golden Boom",
"Crazy Circus","Lucky Wheels","Fire Machine","Dragon Spin","Gold Party",
"Super Fortune","Wild Circus","Candy Spin","Dragon Fire","Money Blast",
"Golden Rush","Super Boom","Fire Dragon 2","Lucky Machine","Fortune Spin X",
"Mega Circus","Golden Dragon Spin","Wild Boom","Hot Candy","Fire Fortune",
"Dragon Empire","Money Dragon","Golden Storm","Super Fire Spin","Candy World",
"Lucky Explosion","Fortune Machine","Mega Dragon","Golden Candy Rush",
"Wild Fire Spin","Dragon Mega Win","Money Circus","Super Gold Spin",
"Fire Jackpot","Lucky Dragon Pro","Golden Blast","Crazy Money Spin",
"Fortune Dragon X","Mega Candy","Super Empire"
],

"YELLOW BAT": [
"Bat Frenzy","Golden Night Bat","Shadow Bat","Neon Rush","Vampire Bat Gold",
"Midnight Bat","Bat King","Lucky Bat Empire","Dark Wing","Night Hunter",
"Shadow Wings","Golden Bat Rush","Bat Storm","Neon Vampire","Dark Night Spin",
"Bat Fortune","Golden Wings","Night Bat Pro","Vampire Gold Rush","Shadow Hunter",
"Bat Empire","Midnight Spin","Neon Bat King","Dark Gold Bat","Lucky Night Wings",
"Bat Legend","Golden Shadow Bat","Night Fury","Bat Power","Vampire Spin",
"Shadow Empire","Bat Rush 2","Golden Night King","Neon Dark Bat",
"Night Wings Pro","Bat Mega Win","Shadow Gold Rush","Vampire Empire",
"Bat Storm X","Golden Night Fury","Dark Bat Legend","Neon Spin Bat",
"Midnight Gold Bat","Lucky Shadow Wings","Bat Fortune Pro","Night King Bat",
"Golden Vampire Spin","Shadow Rush X","Bat Mega Empire","Neon Night Win"
],

"CO9": [
"CO9 Fortune","Golden Empire CO9","Lucky Spin CO9","Dragon Rise CO9",
"Money Train CO9","Wild Gold CO9","Mega Win CO9","Fire Wheel CO9","CO9 Blast",
"Golden Rush CO9","Lucky Dragon CO9","Fortune Spin CO9","CO9 Empire",
"Dragon Fortune CO9","Gold Storm CO9","Lucky Wheel CO9","CO9 Mega Spin",
"Fire Dragon CO9","Golden Path CO9","Money Rush CO9","CO9 Jackpot",
"Wild Spin CO9","Fortune Gold CO9","Dragon Gold CO9","CO9 Lucky Star",
"Golden Blast CO9","Mega Fortune CO9","Spin Empire CO9","CO9 Power Win",
"Fire Fortune CO9","Golden Spin Pro CO9","Lucky Rush CO9","CO9 Dragon King",
"Wild Gold Spin CO9","Fortune Empire CO9","Mega Dragon CO9","CO9 Super Win",
"Golden Wheel CO9","Lucky Blast CO9","Fire Spin Pro CO9","CO9 Money King",
"Dragon Spin CO9","Gold Fortune Pro CO9","CO9 Rush X","Mega Gold CO9",
"Lucky Empire CO9","Spin Master CO9","Fortune Wheel X CO9"
]
}

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
        [InlineKeyboardButton("SEARCH", callback_data="search")]
    ])

# ---------------- TIME ----------------
def get_time():
    now = datetime.now(PH)
    start = now + timedelta(minutes=5)
    end = start + timedelta(minutes=30)
    return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🎮 Welcome!\n\nGuide: {CANVA_LINK}\n\nChoose provider 👇",
        reply_markup=menu()
    )

# ---------------- ADMIN ----------------
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME:
        await update.message.reply_text("❌ Not authorized.")
        return
    await update.message.reply_text("🛠 Admin Panel Active")

# ---------------- BUTTON ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if anti_spam(q.from_user.id):
        return

    data = q.data

    if data == "search":
        await q.edit_message_text("Send game name to search 🔍")
        return

    if data in games:
        text = f"🎰 {data}\n\nGuide: {CANVA_LINK}\n\n"
        for g in games[data]:
            text += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        await q.edit_message_text(text, reply_markup=menu())

# ---------------- SEARCH ----------------
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.lower()

    for p, items in games.items():
        for g in items:
            if txt in g.lower():
                await update.message.reply_text(
                    f"🎮 {g}\n🎰 {p}\n🕐 {get_time()}\n👉 {CASINO_LINK}"
                )
                return

    await update.message.reply_text("Game not found.", reply_markup=menu())

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
app.run_polling()"Book of Gold","Sweet Land","Boxing Extravaganza","Sin City","Golden Bank",
"Pharaoh Treasure","Witches Night","Arena Fighter","Lucky Doggy","Fortune Tree",
"Bone Fortune","Golden Queen","Master Tiger","Jungle King","Samba","Golden Joker"
],

"PG": [
"Mahjong Ways 1","Mahjong Ways 2","Lucky Neko","Fortune Tiger","Dragon Hatch",
"Wild Bandito","Treasures of Aztec","Ganesha Gold","Medusa","Symbol of Egypt",
"Hood vs Wolf","Rooster Rumble","Win Win Fish","Garuda Gems","Bikini Paradise",
"Double Fortune","Crypto Gold","Dragon Legend","Candy Burst","Phoenix Rises"
],

"PRAGMATIC": [
"Gates of Olympus","Sweet Bonanza","Sugar Rush","Big Bass Bonanza","Wolf Gold",
"The Dog House","Wild West Gold","Buffalo King","Madame Destiny","Fire Strike",
"Aztec Gems","John Hunter","Release the Kraken","Hot Safari","Extra Juicy"
],

"FA CHAI": [
"Fa Chai Fortune","Golden Monkey","Lucky Panda","Dragon Fortune","Money Tree",
"Fortune Festival","Golden Dragon","Lucky Coins","Red Packet Rush","Oriental Gold"
],

"BNG": [
"Book of Fortune","Bonanza Gold","Super Marble","Dragon Fishing","Ocean King",
"Shark Hunter","Fire Rooster","Treasure Island","Lucky Fishing","Golden Crab"
],

"JDB": [
"Dragon Hunter","Fire Phoenix","Money Bang Bang","Golden Disco","Candy Burst",
"Super Dragon","Hot Spin","Fortune Island","Mega Spin","Golden Boom"
],

"YELLOW BAT": [
"Bat Frenzy","Golden Night Bat","Shadow Bat","Neon Bat Rush","Vampire Bat Gold",
"Midnight Bat","Bat King","Lucky Bat Empire","Dark Wing","Night Hunter"
],

"CO9": [
"CO9 Fortune","Golden Empire CO9","Lucky Spin CO9","Dragon Rise CO9",
"Money Train CO9","Wild Gold CO9","Mega Win CO9","Fire Wheel CO9","CO9 Blast"
]
}

providers = list(games.keys())

# ---------------- MENU ----------------
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 JILI", callback_data="JILI"),
         InlineKeyboardButton("🎲 PG", callback_data="PG")],
        [InlineKeyboardButton("🔥 PRAGMATIC", callback_data="PRAGMATIC"),
         InlineKeyboardButton("🧧 FA CHAI", callback_data="FA CHAI")],
        [InlineKeyboardButton("⚡ BNG", callback_data="BNG"),
         InlineKeyboardButton("🎮 JDB", callback_data="JDB")],
        [InlineKeyboardButton("🦇 YELLOW BAT", callback_data="YELLOW BAT"),
         InlineKeyboardButton("💎 CO9", callback_data="CO9")],
        [InlineKeyboardButton("🔍 SEARCH", callback_data="search")]
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
    return (len(games[provider]) - 1) // PER_PAGE

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 GOOD DAY BOSSING!\n\nChoose provider 👇",
        reply_markup=menu()
    )

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if anti_spam(q.from_user.id):
        return

    data = q.data

    # SEARCH MODE
    if data == "search":
        await q.edit_message_text("🔍 Send game name in chat.")
        return

    # PROVIDER
    if data in games:
        page = 0
        items, _ = paginate(games[data], page)
        maxp = max_page(data)

        msg = f"🌐 {CANVA_LINK}\n📩 {SUPPORT}\n\n🎰 {data}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{data}_{page-1}"),
                InlineKeyboardButton(f"{page+1}/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{data}_{page+1}")
            ],
            [InlineKeyboardButton("🔄 Refresh", callback_data=data)],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))
        return

    # PAGINATION
    if data.startswith("page_"):
        _, provider, page = data.split("_")
        page = int(page)

        items, _ = paginate(games[provider], page)
        maxp = max_page(provider)

        msg = f"🌐 {CANVA_LINK}\n📩 {SUPPORT}\n\n🎰 {provider}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{provider}_{page-1}"),
                InlineKeyboardButton(f"{page+1}/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{provider}_{page+1}")
            ],
            [InlineKeyboardButton("🔄 Refresh", callback_data=provider)],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data == "menu":
        await q.edit_message_text("🏠 MAIN MENU", reply_markup=menu())

# ---------------- SEARCH ----------------
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
