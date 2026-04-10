import os
import time
import random
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------------- TOKEN ----------------
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise Exception("Missing TOKEN")

CASINO_LINK = "http://kuyax333.paldopinas84.cc/?referralCode=opl5030"
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"

PH = timezone(timedelta(hours=8))

# ---------------- FAST CLICK ----------------
click_cache = {}

def fast_click(uid, action):
    now = time.time()
    key = f"{uid}:{action}"
    if now - click_cache.get(key, 0) < 0.08:
        return False
    click_cache[key] = now
    return True

# ---------------- TIME PER GAME ----------------
def get_time(i):
    now = datetime.now(PH)
    start = now + timedelta(minutes=5 + i * 2)
    end = start + timedelta(minutes=25)
    return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"

# ---------------- 50 REAL GAMES EACH ----------------
games = {
"JILI": [
"Super Ace","Golden Empire","Boxing King","Money Coming","Lucky Jaguar","Fortune Gems","Wild Ace",
"Golden Bank 2","Shogun","Nightfall Hunting","Money Pot","Fruity Wheel","Aztec Priestess","Go For Champion",
"Magic Lamp","Legacy of Egypt","Pirate Queen","Golden Temple","Jackpot Joker","Candy Baby",
"Mines Gold","Lucky Goldbricks","Bonus Hunter","Party Star","King Arthur","War Dragons","Book of Gold",
"Sweet Land","Sin City","Golden Queen","Master Tiger","Jungle King","Samba","Golden Joker","Fortune Tree",
"Lucky Doggy","Arena Fighter","Pharaoh Treasure","Witches Night","Bone Fortune","Dragon Treasure",
"Royal Gold","Mega Fortune","Wild Spin","Cash Mania","Gold Rush","Temple Run","Mystic Gems",
"Fortune Spin","Dragon Rise"
],

"PG 🎰": [
"Mahjong Ways","Mahjong Ways 2","Lucky Neko","Fortune Tiger","Dragon Hatch","Wild Bandito",
"Treasures of Aztec","Ganesha Gold","Medusa","Symbol of Egypt","Hood vs Wolf","Rooster Rumble",
"Win Win Fish","Garuda Gems","Bikini Paradise","Double Fortune","Dragon Legend","Candy Burst",
"Phoenix Rises","Heist Stakes","Wild Coaster","Journey to Wealth","Fortune Mouse","Alchemy Gold",
"Captain Bounty","Mermaid Riches","Jurassic Kingdom","Vampire Night","Emoji Riches","Shark Hunter",
"Piggy Gold","Opera Dynasty","Wild Fireworks","Leprechaun Riches","Buffalo Win","Mahjong Royal",
"Fortune Rabbit","Candy Bonanza","Dragon Fortune","Lucky Clover","Golden Pig","Supermarket Spree",
"Crypto Panda","Legend Perseus","Wild Ape","Dragon Master","Lucky Spin","Ocean King","Moon Princess","Golden Era"
],

"PRAGMATIC 🎲": [
"Gates of Olympus","Sweet Bonanza","Sugar Rush","Big Bass Bonanza","Wolf Gold","The Dog House",
"Wild West Gold","Buffalo King","Madame Destiny","Fire Strike","Aztec Gems","John Hunter",
"Release the Kraken","Hot Safari","Fruit Party","Starlight Princess","Power of Thor","Viking Forge",
"Hand of Midas","Chilli Heat","5 Lions Megaways","Mustang Gold","Madame Megaways","Bronco Spirit",
"Cowboy Coins","Pixie Wings","Wild Walker","Cosmic Cash","Treasure Wild","Gates of Hades",
"Powernudge","Bigger Bass","Black Bull","Gold Party","Lucky Lightning","Magic Maze",
"Super X","Vegas Nights","Ultra Hold","Mystery Symbols","Golden Odyssey","Fire Hot",
"Sugar Rush 1000","Sweet Bonanza Xmas","Fruit Party 2","Rise of Olympus","Book of Golden Sands",
"Pyramid King","Buffalo King MegaWays","Dragon Gold"
],

"FA CHAI 🐉": [
"Golden Dragon","Lucky Panda","Money Tree","Fortune Festival","Dragon Fortune","Red Packet Rush",
"Prosperity Tiger","Fortune Ox","Golden Bamboo","Lucky Phoenix","Dragon Wealth","Imperial Gold",
"Fortune Emperor","Lucky Zodiac","Golden Dynasty","Red Dragon Rise","Mandarin Treasure",
"Asia Fortune","Golden Asia","Spring Festival","Lucky Harvest","Fortune Bloom","Golden Panda",
"Money Rain","Red Lantern","Dragon Blessing","Imperial Fortune","Golden Wheel","Lucky Spin",
"Fortune Cloud","Asia Star","Golden Festival","Prosperity Spin","Lucky Red","Dragon Prosperity",
"Golden Path","Money Luck","Fortune King","Red Path","Asia Win","Golden Tiger",
"Lucky Empire","Fortune Rise","Dragon Light","Golden Temple Asia","Lucky Fortune 2",
"Prosperity Gold","Dragon Coin","Golden Flow","Money Empire"
],

"BNG 🌊": [
"Ocean King","Fish Hunter","Golden Crab","Deep Sea","Ocean Treasure","Golden Whale",
"Mega Fishing","Lucky Catch","Treasure Island","Shark Hunter","Ocean Rush","Fish King",
"Golden Fisher","Sea Dragon","Ocean Empire","Fishing Pro","Deep Fortune","Sea King",
"Ocean Spin","Treasure Fish","Golden Wave","Sea Gold","Fish Empire","Ocean Legend",
"Lucky Fishing","Dragon Ocean","Pirate Catch","Sea Battle","Ocean Storm","Fish Master",
"Deep Gold","Ocean Win","Golden Reef","Sea Treasure","Fishing Storm","Ocean Hunter",
"Mega Sea","Lucky Ocean","Fish Bonanza","Sea Fortune","Ocean Gold","Golden Catch",
"Deep King","Sea Power","Fish Rich","Ocean X","Golden Sea","Lucky Reef","Fishing Empire","Ocean Pro"
],

"JDB 💎": [
"Dragon Hunter","Fire Phoenix","Money Bang","Golden Disco","Candy Burst","Super Dragon",
"Hot Spin","Fortune Island","Mega Spin","Golden Boom","Lucky Wheels","Fire Machine",
"Dragon Spin","Gold Party","Wild Circus","Candy Spin","Dragon Fire","Money Blast",
"Golden Rush","Super Boom","Lucky Machine","Spin Master","Mega Circus","Dragon Gold Spin",
"Wild Boom","Hot Candy","Fire Fortune","Dragon Empire","Money Dragon","Golden Storm",
"Fire Spin","Candy World","Lucky Explosion","Fortune Machine","Mega Dragon",
"Super Gold","Fire Jackpot","Lucky Dragon","Golden Blast","Money Spin","Fortune X",
"Mega Candy","Super Empire","Dragon Win","Golden Fire","Lucky Boom",
"Spin King","Fire Wheel","Money Rush","Dragon Force"
],

"YELLOW BAT 🦇": [
"Bat Frenzy","Golden Bat","Shadow Bat","Neon Rush","Vampire Gold","Midnight Bat",
"Bat King","Lucky Bat","Dark Wing","Night Hunter","Shadow Wings","Golden Rush",
"Bat Storm","Neon Vampire","Night Spin","Bat Fortune","Golden Wings","Night Pro",
"Vampire Rush","Shadow Hunter","Bat Empire","Midnight Spin","Neon King","Dark Gold",
"Lucky Wings","Bat Legend","Golden Shadow","Night Fury","Bat Power","Vampire Spin",
"Shadow Empire","Golden King","Neon Bat","Night Wings","Bat Win","Shadow Gold",
"Vampire Empire","Golden Fury","Dark Bat","Neon Spin","Midnight Gold","Lucky Shadow",
"Bat Pro","Shadow Rush","Bat Mega","Neon Win","Golden Vampire","Night King",
"Bat Storm X","Shadow Rise"
],

"CO9 ⚡": [
"CO9 Fortune","Golden CO9","Lucky Spin","Dragon Rise","Money Train","Wild Gold",
"Mega Win","Fire Wheel","CO9 Blast","Golden Rush","Lucky Dragon","Fortune Spin",
"CO9 Empire","Dragon Fortune","Gold Storm","Lucky Wheel","Mega Spin","Fire Dragon",
"Golden Path","Money Rush","CO9 Jackpot","Wild Spin","Fortune Gold","Dragon Gold",
"Lucky Star","Golden Blast","Mega Fortune","Spin Empire","Power Win","Fire Fortune",
"Golden Spin","Lucky Rush","Dragon King","Wild Gold Spin","Fortune Empire",
"Mega Dragon","Super Win","Golden Wheel","Lucky Blast","Fire Spin","Money King",
"Dragon Spin","Gold Fortune","Rush X","Mega Gold","Empire Spin","Spin Master",
"Wheel X","Fortune Pro","CO9 Max"
]
}

# ---------------- MENU ----------------
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 JILI", callback_data="JILI"),
         InlineKeyboardButton("🎲 PG", callback_data="PG")],
        [InlineKeyboardButton("🔥 PRAGMATIC", callback_data="PRAGMATIC"),
         InlineKeyboardButton("🐉 FA CHAI", callback_data="FA CHAI")],
        [InlineKeyboardButton("🌊 BNG", callback_data="BNG"),
         InlineKeyboardButton("💎 JDB", callback_data="JDB")],
        [InlineKeyboardButton("🦇 YELLOW BAT", callback_data="YELLOW BAT"),
         InlineKeyboardButton("⚡ CO9", callback_data="CO9")]
    ])

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 GOOD DAY BOSSING 😎\nChoose provider below 👇",
        reply_markup=menu()
    )

# ---------------- BUTTON ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    data = q.data
    uid = q.from_user.id

    if not fast_click(uid, data):
        return

    if data in games:
        page = 0
        per_page = 10

        items = games[data][page*per_page:(page+1)*per_page]

        msg = f"🎰 {data}\n\n"

        for i, g in enumerate(items):
            msg += f"🎮 {g}\n🕐 {get_time(i)}\n\n"

        msg += (
            "\n🚫 RESTRICTED THIS ONLY LINK WORKS\n"
            f"{CASINO_LINK}\n\n"
            "📘 MORE HOUR GUIDE INFO\n"
            f"{CANVA_LINK}"
        )

        kb = [
            [
                InlineKeyboardButton("⬅️ MENU", callback_data="menu"),
                InlineKeyboardButton("1/5", callback_data="noop"),
                InlineKeyboardButton("➡️ NEXT", callback_data=f"page_{data}_1")
            ]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("page_"):
        _, provider, page = data.split("_")
        page = int(page)
        per_page = 10

        items = games[provider][page*per_page:(page+1)*per_page]

        msg = f"🎰 {provider}\n\n"

        for i, g in enumerate(items):
            msg += f"🎮 {g}\n🕐 {get_time(i + page*10)}\n\n"

        msg += (
            "\n🚫 RESTRICTED THIS ONLY LINK WORKS\n"
            f"{CASINO_LINK}\n\n"
            "📘 MORE HOUR GUIDE INFO\n"
            f"{CANVA_LINK}"
        )

        kb = [
            [
                InlineKeyboardButton("⬅️ BACK", callback_data=f"page_{provider}_{max(page-1,0)}"),
                InlineKeyboardButton(f"{page+1}/5", callback_data="noop"),
                InlineKeyboardButton("➡️ NEXT", callback_data=f"page_{provider}_{min(page+1,4)}")
            ],
            [InlineKeyboardButton("🏠 MENU", callback_data="menu")]
        ]

        await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data == "menu":
        await q.edit_message_text("🏠 MENU", reply_markup=menu())

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
