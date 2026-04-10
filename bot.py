import os
import time
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------------- TOKEN ----------------
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise Exception("Missing TOKEN")

# ---------------- LINKS (ONLY FOOTER USE) ----------------
CASINO_LINK = "https://example.com"
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"

PH = timezone(timedelta(hours=8))

# ---------------- CLICK SMOOTH SYSTEM ----------------
click_cache = {}

def smooth_click(uid, action):
    now = time.time()
    key = f"{uid}:{action}"
    last = click_cache.get(key, 0)

    if now - last < 0.12:
        return False

    click_cache[key] = now
    return True

# ---------------- REAL GAME DATA ----------------
games = {
    "JILI": [
        "Super Ace","Golden Empire","Boxing King","Money Coming","Lucky Jaguar",
        "Fortune Gems","Wild Ace","Golden Bank 2","Shogun","Nightfall Hunting",
        "Money Pot","Fruity Wheel","Aztec Priestess","Go For Champion","Magic Lamp",
        "Legacy of Egypt","Pirate Queen","Golden Temple","Jackpot Joker","Candy Baby",
        "Mines Gold","Lucky Goldbricks","Bonus Hunter","Party Star","King Arthur",
        "War Dragons","Book of Gold","Sweet Land","Sin City","Golden Queen",
        "Master Tiger","Jungle King","Samba","Golden Joker","Fortune Tree",
        "Lucky Doggy","Arena Fighter","Pharaoh Treasure","Witches Night","Bone Fortune",
        "Dragon Treasure","Royal Gold","Mega Fortune","Wild Spin","Cash Mania",
        "Gold Rush","Temple Run","Mystic Gems","Fortune Spin","Dragon Rise"
    ],

    "PG": [
        "Mahjong Ways","Mahjong Ways 2","Lucky Neko","Fortune Tiger","Dragon Hatch",
        "Wild Bandito","Treasures of Aztec","Ganesha Gold","Medusa","Symbol of Egypt",
        "Hood vs Wolf","Rooster Rumble","Win Win Fish","Garuda Gems","Bikini Paradise",
        "Double Fortune","Dragon Legend","Candy Burst","Phoenix Rises","Heist Stakes",
        "Wild Coaster","Journey to Wealth","Fortune Mouse","Alchemy Gold","Captain Bounty",
        "Mermaid Riches","Jurassic Kingdom","Vampire Night","Emoji Riches","Shark Hunter",
        "Piggy Gold","Opera Dynasty","Wild Fireworks","Leprechaun Riches","Buffalo Win",
        "Mahjong Royal","Fortune Rabbit","Candy Bonanza","Dragon Fortune","Lucky Clover",
        "Golden Pig","Supermarket Spree","Crypto Panda","Legend Perseus","Wild Ape",
        "Dragon Master","Lucky Spin","Ocean King","Moon Princess","Golden Era"
    ],

    "PRAGMATIC": [
        "Gates of Olympus","Sweet Bonanza","Sugar Rush","Big Bass Bonanza","Wolf Gold",
        "The Dog House","Wild West Gold","Buffalo King","Madame Destiny","Fire Strike",
        "Aztec Gems","John Hunter","Release the Kraken","Hot Safari","Fruit Party",
        "Starlight Princess","Power of Thor","Viking Forge","Hand of Midas","Chilli Heat",
        "5 Lions Megaways","Mustang Gold","Madame Megaways","Bronco Spirit","Cowboy Coins",
        "Pixie Wings","Wild Walker","Cosmic Cash","Treasure Wild","Gates of Hades",
        "Powernudge","Bigger Bass","Black Bull","Gold Party","Lucky Lightning",
        "Magic Maze","Super X","Vegas Nights","Ultra Hold","Mystery Symbols",
        "Golden Odyssey","Fire Hot","Sugar Rush 1000","Sweet Bonanza Xmas","Fruit Party 2",
        "Rise of Olympus","Book of Golden Sands","Pyramid King","Buffalo King MegaWays","Dragon Gold"
    ],

    "FA CHAI": [
        "Golden Dragon","Lucky Panda","Money Tree","Fortune Festival","Dragon Fortune",
        "Red Packet Rush","Prosperity Tiger","Fortune Ox","Golden Bamboo","Lucky Phoenix",
        "Dragon Wealth","Imperial Gold","Fortune Emperor","Lucky Zodiac","Golden Dynasty",
        "Red Dragon Rise","Mandarin Treasure","Asia Fortune","Golden Asia","Spring Festival",
        "Lucky Harvest","Fortune Bloom","Golden Panda","Money Rain","Red Lantern",
        "Dragon Blessing","Imperial Fortune","Golden Wheel","Lucky Spin","Fortune Cloud",
        "Asia Star","Golden Festival","Prosperity Spin","Lucky Red","Dragon Prosperity",
        "Golden Path","Money Luck","Fortune King","Red Path","Asia Win",
        "Golden Tiger","Lucky Empire","Fortune Rise","Dragon Light","Golden Temple Asia",
        "Lucky Fortune 2","Prosperity Gold","Dragon Coin","Golden Flow","Money Empire"
    ],

    "BNG": [
        "Ocean King","Fish Hunter","Golden Crab","Deep Sea","Ocean Treasure",
        "Golden Whale","Mega Fishing","Lucky Catch","Treasure Island","Shark Hunter",
        "Ocean Rush","Fish King","Golden Fisher","Sea Dragon","Ocean Empire",
        "Fishing Pro","Deep Fortune","Sea King","Ocean Spin","Treasure Fish",
        "Golden Wave","Sea Gold","Fish Empire","Ocean Legend","Lucky Fishing",
        "Dragon Ocean","Pirate Catch","Sea Battle","Ocean Storm","Fish Master",
        "Deep Gold","Ocean Win","Golden Reef","Sea Treasure","Fishing Storm",
        "Ocean Hunter","Mega Sea","Lucky Ocean","Fish Bonanza","Sea Fortune",
        "Ocean Gold","Golden Catch","Deep King","Sea Power","Fish Rich",
        "Ocean X","Golden Sea","Lucky Reef","Fishing Empire","Ocean Pro"
    ],

    "JDB": [
        "Dragon Hunter","Fire Phoenix","Money Bang","Golden Disco","Candy Burst",
        "Super Dragon","Hot Spin","Fortune Island","Mega Spin","Golden Boom",
        "Lucky Wheels","Fire Machine","Dragon Spin","Gold Party","Wild Circus",
        "Candy Spin","Dragon Fire","Money Blast","Golden Rush","Super Boom",
        "Lucky Machine","Spin Master","Mega Circus","Dragon Gold Spin","Wild Boom",
        "Hot Candy","Fire Fortune","Dragon Empire","Money Dragon","Golden Storm",
        "Fire Spin","Candy World","Lucky Explosion","Fortune Machine","Mega Dragon",
        "Super Gold","Fire Jackpot","Lucky Dragon","Golden Blast","Money Spin",
        "Fortune X","Mega Candy","Super Empire","Dragon Win","Golden Fire",
        "Lucky Boom","Spin King","Fire Wheel","Money Rush","Dragon Force"
    ],

    "YELLOW BAT": [
        "Bat Frenzy","Golden Bat","Shadow Bat","Neon Rush","Vampire Gold",
        "Midnight Bat","Bat King","Lucky Bat","Dark Wing","Night Hunter",
        "Shadow Wings","Golden Rush","Bat Storm","Neon Vampire","Night Spin",
        "Bat Fortune","Golden Wings","Night Pro","Vampire Rush","Shadow Hunter",
        "Bat Empire","Midnight Spin","Neon King","Dark Gold","Lucky Wings",
        "Bat Legend","Golden Shadow","Night Fury","Bat Power","Vampire Spin",
        "Shadow Empire","Golden King","Neon Bat","Night Wings","Bat Win",
        "Shadow Gold","Vampire Empire","Golden Fury","Dark Bat","Neon Spin",
        "Midnight Gold","Lucky Shadow","Bat Pro","Shadow Rush","Bat Mega",
        "Neon Win","Golden Vampire","Night King","Bat Storm X","Shadow Rise"
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
        "🎮 GOOD DAY BOSSING!\nChoose provider below 👇",
        reply_markup=menu()
    )

# ---------------- BUTTON ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    data = q.data
    uid = q.from_user.id

    if not smooth_click(uid, data):
        return

    # ---------------- PROVIDER ----------------
    if data in games:
        page = 0
        items = games[data][:10]
        maxp = max(0, (len(games[data]) - 1) // 10)

        msg = f"🎰 {data}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n\n"

        # FINAL FOOTER ONLY
        msg += (
            "\n🚫 RESTRICTED THIS ONLY LINK WORKS\n"
            f"{CASINO_LINK}\n\n"
            f"📘 MORE GUIDE INFO\n{CANVA_LINK}"
        )

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data="noop"),
                InlineKeyboardButton("1/5", callback_data="noop"),
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

        items = games[provider][page*10:(page+1)*10]
        maxp = max(0, (len(games[provider]) - 1) // 10)

        msg = f"🎰 {provider}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n\n"

        msg += (
            "\n🚫 RESTRICTED THIS ONLY LINK WORKS\n"
            f"{CASINO_LINK}\n\n"
            f"📘 MORE GUIDE INFO\n{CANVA_LINK}"
        )

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
