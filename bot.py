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

PH = timezone(timedelta(hours=8))

# ---------------- ANTI SPAM ----------------
cooldown = {}

def anti_spam(uid):
    now = time.time()
    if uid in cooldown and now - cooldown[uid] < 1.5:
        return True
    cooldown[uid] = now
    return False

# ---------------- GAME DATA ----------------
games = {
"JILI": ["Super Ace","Golden Empire","Boxing King","Crazy777","Money Coming","Lucky Jaguar",
"Fortune Gems","Wild Ace","Golden Bank 2","Shogun","3 Lucky Pigs","3 Coin Treasures",
"Nightfall Hunting","Money Pot","Fruity Wheel","Aztec Priestess","Bangla Beauty",
"Go For Champion","Egypt Glow","Magic Lamp","Night City","Legacy of Egypt",
"Pirate Queen","Golden Temple","Jackpot Joker","Candy Baby","Mines Gold",
"Lucky Goldbricks","Bonus Hunter","Party Star","King Arthur","War Dragons",
"Book of Gold","Sweet Land","Boxing Extravaganza","Sin City","Golden Bank",
"Pharaoh Treasure","Witches Night","Arena Fighter","Lucky Doggy","Fortune Tree",
"Bone Fortune","Golden Queen","Master Tiger","Jungle King","Samba","Golden Joker"],

"PG": ["Mahjong Ways 1","Mahjong Ways 2","Lucky Neko","Fortune Tiger","Dragon Hatch",
"Wild Bandito","Treasures of Aztec","Ganesha Gold","Medusa","Symbol of Egypt",
"Hood vs Wolf","Rooster Rumble","Win Win Fish","Garuda Gems","Bikini Paradise",
"Double Fortune","Crypto Gold","Dragon Legend","Candy"Pirate Queen","Golden Temple","Jackpot Joker","Candy Baby","Mines Gold",
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
"Santa Gift Rush","Heist Stakes","Wild Coaster","Journey to Wealth",
"Dragon Tiger Luck","Fortune Mouse","Alchemy Gold","Captain Bounty",
"Mermaid Riches","Jurassic Kingdom","Vampire Night","Emoji Riches",
"Shark Hunter","Bali Vacation","Piggy Gold","Opera Dynasty","Wild Fireworks",
"Legend Perseus","Leprechaun Riches","Crypto Panda","Buffalo Win",
"Mahjong Ways 3","Golden Pig","Lucky Clover","Supermarket Spree",
"Mahjong Royal","Fortune Rabbit","Candy Bonanza"
],

"PRAGMATIC": [
"Gates of Olympus","Sweet Bonanza","Sugar Rush","Big Bass Bonanza","Wolf Gold",
"The Dog House","Wild West Gold","Buffalo King","Madame Destiny","Fire Strike",
"Aztec Gems","John Hunter","Release Kraken","Hot Safari","Extra Juicy",
"Fruit Party","Sugar Rush 1000","Sweet Xmas","Olympus 1000","Starlight Princess",
"Power Thor","Viking Forge","Hand Midas","Caishen Gold","Chilli Heat",
"5 Lions Megaways","Mustang Gold","Madame Megaways","Bronco Spirit","Cowboy Coins",
"Pixie Wings","Aztec King","Wild Walker","Cosmic Cash","Treasure Wild",
"Fruit Party 2","Gates Hades","Powernudge","Bigger Bass","Black Bull",
"Gold Party","Fire Hot 40","Lucky Lightning","Magic Maze","Super X",
"Vegas Nights","Ultra Hold","Mystery Symbols","Golden Odyssey"
],

"FA CHAI": [
"Fa Chai Fortune","Golden Monkey","Lucky Panda","Dragon Fortune","Money Tree",
"Fortune Festival","Golden Dragon","Lucky Coins","Red Packet Rush","Oriental Gold",
"Prosperity Tiger","Fortune Ox","Lucky Spin","Golden Prosperity","Rich Harvest",
"China Gold","Red Lantern","Mandarin Treasure","Golden Bamboo","Lucky Phoenix",
"Dragon Wealth","Fortune Dynasty","Imperial Gold","Red Dragon Rise","Golden Panda",
"Fortune Emperor","Dragon Blessing","Lucky Zodiac","Temple Luck","Money Rain",
"Fortune Bloom","Golden Dynasty","Asia Fortune","Spring Festival","Golden Asia",
"Tiger Asia","Dragon 2","Lucky Harvest","Prosperity Spin","Golden Wheel",
"Red Path","Mandarin Gold","Asia Star","Golden Festival","Fortune Cloud",
"Dragon Prosperity","Asia Win","Lucky Red","Imperial Fortune","Prosperity 2"
],

"BNG": [
"Book Fortune","Bonanza Gold","Super Marble","Dragon Fishing","Ocean King",
"Shark Hunter","Fire Rooster","Treasure Island","Lucky Fishing","Golden Crab",
"Deep Sea","Ocean Treasure","Golden Whale","Fish Pro","Ocean King 2",
"Mega Fishing","Sea Fortune","Dragon Ocean","Pirate Catch","Golden Reef",
"Lucky Spin","Fish King","Ocean Rush","Treasure Fish","Shark Attack",
"Sea Battle","Deep Gold","Ocean Storm","Fish Master","Sea King",
"Golden Fisher","Jackpot Ocean","Lucky Catch","Sea Treasure","Ocean Empire",
"Fish Bonanza","Golden Wave","Deep Fortune","Sea Dragon","Ocean Spin",
"Treasure Sea","Fish Wealth","Ocean Win","Sea Gold","Ocean Legend",
"Fish Empire","Deep King","Big Win","Fishing Pro","Sea Fortune 2"
],

"JDB": [
"Dragon Hunter","Fire Phoenix","Money Bang","Golden Disco","Candy Burst",
"Super Dragon","Hot Spin","Fortune Island","Mega Spin","Golden Boom",
"Circus","Lucky Wheels","Fire Machine","Dragon Spin","Gold Party",
"Super Fortune","Wild Circus","Candy Spin","Dragon Fire","Money Blast",
"Golden Rush","Super Boom","Fire Dragon 2","Lucky Machine","Spin X",
"Mega Circus","Dragon Spin Gold","Wild Boom","Hot Candy","Fire Fortune",
"Dragon Empire","Money Dragon","Golden Storm","Fire Spin","Candy World",
"Lucky Explosion","Fortune Machine","Mega Dragon","Candy Rush","Wild Fire",
"Dragon Win","Money Circus","Super Gold","Fire Jackpot","Lucky Dragon",
"Golden Blast","Money Spin","Fortune X","Mega Candy","Super Empire"
],

"YELLOW BAT": [
"Bat Frenzy","Golden Bat","Shadow Bat","Neon Rush","Vampire Gold",
"Midnight Bat","Bat King","Lucky Bat","Dark Wing","Night Hunter",
"Shadow Wings","Golden Rush","Bat Storm","Neon Vampire","Night Spin",
"Bat Fortune","Golden Wings","Night Pro","Vampire Rush","Shadow Hunter",
"Bat Empire","Midnight Spin","Neon King","Dark Gold","Lucky Wings",
"Bat Legend","Golden Shadow","Night Fury","Bat Power","Vampire Spin",
"Shadow Empire","Bat Rush 2","Golden King","Neon Bat","Night Wings",
"Bat Win","Shadow Gold","Vampire Empire","Bat Storm X","Golden Fury",
"Dark Bat","Neon Spin","Midnight Gold","Lucky Shadow","Bat Pro",
"Golden Vampire","Shadow Rush","Bat Mega","Neon Win"
],

"CO9": [
"CO9 Fortune","Golden CO9","Lucky Spin","Dragon Rise","Money Train",
"Wild Gold","Mega Win","Fire Wheel","CO9 Blast","Golden Rush",
"Lucky Dragon","Fortune Spin","CO9 Empire","Dragon Fortune","Gold Storm",
"Lucky Wheel","Mega Spin","Fire Dragon","Golden Path","Money Rush",
"CO9 Jackpot","Wild Spin","Fortune Gold","Dragon Gold","Lucky Star",
"Golden Blast","Mega Fortune","Spin Empire","Power Win","Fire Fortune",
"Golden Spin","Lucky Rush","Dragon King","Wild Gold Spin","Fortune Empire",
"Mega Dragon","Super Win","Golden Wheel","Lucky Blast","Fire Spin",
"Money King","Dragon Spin","Gold Fortune","Rush X","Mega Gold",
"Empire Spin","Spin Master","Wheel X","Fortune Pro","CO9 Max"
]
}

# ---------------- PAGINATION ----------------
PAGE_SIZE = 10

def paginate(items, page):
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    return items[start:end]

def max_page(provider):
    return (len(games[provider]) - 1) // PAGE_SIZE

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
    await update.message.reply_text(
        f"🎮 Welcome!\n\nGuide: {CANVA_LINK}\n\nChoose provider 👇",
        reply_markup=menu()
    )

# ---------------- BUTTON ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if anti_spam(q.from_user.id):
        return

    data = q.data

    if data in games:
        page = 0
        items = games[data]
        page_items = paginate(items, page)
        maxp = max_page(data)

        msg = f"🎰 {data}\n\nGuide: {CANVA_LINK}\n\n"

        for g in page_items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{data}_{page}"),
                InlineKeyboardButton(f"{page+1}/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{data}_{page}")
            ],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data == "menu":
        await q.edit_message_text("🏠 Menu", reply_markup=menu())

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()"Gates of Olympus","Sweet Bonanza","Sugar Rush","Big Bass Bonanza","Wolf Gold",
"The Dog House","Wild West Gold","Buffalo King","Madame Destiny","Fire Strike",
"Aztec Gems","John Hunter","Release Kraken","Hot Safari","Extra Juicy",
"Fruit Party","Sugar Rush 1000","Sweet Xmas","Olympus 1000","Starlight Princess",
"Power Thor","Viking Forge","Hand Midas","Caishen Gold","Chilli Heat",
"5 Lions Megaways","Mustang Gold","Madame Megaways","Bronco Spirit","Cowboy Coins",
"Pixie Wings","Aztec King","Wild Walker","Cosmic Cash","Treasure Wild",
"Fruit Party 2","Gates Hades","Powernudge","Bigger Bass","Black Bull",
"Gold Party","Fire Hot 40","Lucky Lightning","Magic Maze","Super X",
"Vegas Nights","Ultra Hold","Mystery Symbols","Golden Odyssey"
],

"FA CHAI": [
"Fa Chai Fortune","Golden Monkey","Lucky Panda","Dragon Fortune","Money Tree",
"Fortune Festival","Golden Dragon","Lucky Coins","Red Packet Rush","Oriental Gold",
"Prosperity Tiger","Fortune Ox","Lucky Spin","Golden Prosperity","Rich Harvest",
"China Gold","Red Lantern","Mandarin Treasure","Golden Bamboo","Lucky Phoenix",
"Dragon Wealth","Fortune Dynasty","Imperial Gold","Red Dragon Rise","Golden Panda",
"Fortune Emperor","Dragon Blessing","Lucky Zodiac","Temple Luck","Money Rain",
"Fortune Bloom","Golden Dynasty","Asia Fortune","Spring Festival","Golden Asia",
"Tiger Asia","Dragon 2","Lucky Harvest","Prosperity Spin","Golden Wheel",
"Red Path","Mandarin Gold","Asia Star","Golden Festival","Fortune Cloud",
"Dragon Prosperity","Asia Win","Lucky Red","Imperial Fortune","Prosperity 2"
],

"BNG": [
"Book Fortune","Bonanza Gold","Super Marble","Dragon Fishing","Ocean King",
"Shark Hunter","Fire Rooster","Treasure Island","Lucky Fishing","Golden Crab",
"Deep Sea","Ocean Treasure","Golden Whale","Fish Pro","Ocean King 2",
"Mega Fishing","Sea Fortune","Dragon Ocean","Pirate Catch","Golden Reef",
"Lucky Spin","Fish King","Ocean Rush","Treasure Fish","Shark Attack",
"Sea Battle","Deep Gold","Ocean Storm","Fish Master","Sea King",
"Golden Fisher","Jackpot Ocean","Lucky Catch","Sea Treasure","Ocean Empire",
"Fish Bonanza","Golden Wave","Deep Fortune","Sea Dragon","Ocean Spin",
"Treasure Sea","Fish Wealth","Ocean Win","Sea Gold","Ocean Legend",
"Fish Empire","Deep King","Big Win","Fishing Pro","Sea Fortune 2"
],

"JDB": [
"Dragon Hunter","Fire Phoenix","Money Bang","Golden Disco","Candy Burst",
"Super Dragon","Hot Spin","Fortune Island","Mega Spin","Golden Boom",
"Circus","Lucky Wheels","Fire Machine","Dragon Spin","Gold Party",
"Super Fortune","Wild Circus","Candy Spin","Dragon Fire","Money Blast",
"Golden Rush","Super Boom","Fire Dragon 2","Lucky Machine","Spin X",
"Mega Circus","Dragon Spin Gold","Wild Boom","Hot Candy","Fire Fortune",
"Dragon Empire","Money Dragon","Golden Storm","Fire Spin","Candy World",
"Lucky Explosion","Fortune Machine","Mega Dragon","Candy Rush","Wild Fire",
"Dragon Win","Money Circus","Super Gold","Fire Jackpot","Lucky Dragon",
"Golden Blast","Money Spin","Fortune X","Mega Candy","Super Empire"
],

"YELLOW BAT": [
"Bat Frenzy","Golden Bat","Shadow Bat","Neon Rush","Vampire Gold",
"Midnight Bat","Bat King","Lucky Bat","Dark Wing","Night Hunter",
"Shadow Wings","Golden Rush","Bat Storm","Neon Vampire","Night Spin",
"Bat Fortune","Golden Wings","Night Pro","Vampire Rush","Shadow Hunter",
"Bat Empire","Midnight Spin","Neon King","Dark Gold","Lucky Wings",
"Bat Legend","Golden Shadow","Night Fury","Bat Power","Vampire Spin",
"Shadow Empire","Bat Rush 2","Golden King","Neon Bat","Night Wings",
"Bat Win","Shadow Gold","Vampire Empire","Bat Storm X","Golden Fury",
"Dark Bat","Neon Spin","Midnight Gold","Lucky Shadow","Bat Pro",
"Golden Vampire","Shadow Rush","Bat Mega","Neon Win"
],

"CO9": [
"CO9 Fortune","Golden CO9","Lucky Spin","Dragon Rise","Money Train",
"Wild Gold","Mega Win","Fire Wheel","CO9 Blast","Golden Rush",
"Lucky Dragon","Fortune Spin","CO9 Empire","Dragon Fortune","Gold Storm",
"Lucky Wheel","Mega Spin","Fire Dragon","Golden Path","Money Rush",
"CO9 Jackpot","Wild Spin","Fortune Gold","Dragon Gold","Lucky Star",
"Golden Blast","Mega Fortune","Spin Empire","Power Win","Fire Fortune",
"Golden Spin","Lucky Rush","Dragon King","Wild Gold Spin","Fortune Empire",
"Mega Dragon","Super Win","Golden Wheel","Lucky Blast","Fire Spin",
"Money King","Dragon Spin","Gold Fortune","Rush X","Mega Gold",
"Empire Spin","Spin Master","Wheel X","Fortune Pro","CO9 Max"
]
}

# ---------------- PAGINATION ----------------
PAGE_SIZE = 10

def paginate(items, page):
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    return items[start:end]

def max_page(provider):
    return (len(games[provider]) - 1) // PAGE_SIZE

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
    await update.message.reply_text(
        f"🎮 Welcome!\n\nGuide: {CANVA_LINK}\n\nChoose provider 👇",
        reply_markup=menu()
    )

# ---------------- BUTTON ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if anti_spam(q.from_user.id):
        return

    data = q.data

    if data in games:
        page = 0
        items = games[data]
        page_items = paginate(items, page)
        maxp = max_page(data)

        msg = f"🎰 {data}\n\nGuide: {CANVA_LINK}\n\n"

        for g in page_items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n👉 {CASINO_LINK}\n\n"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{data}_{page}"),
                InlineKeyboardButton(f"{page+1}/{maxp+1}", callback_data="noop"),
                InlineKeyboardButton("➡️", callback_data=f"page_{data}_{page}")
            ],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data == "menu":
        await q.edit_message_text("🏠 Menu", reply_markup=menu())

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
