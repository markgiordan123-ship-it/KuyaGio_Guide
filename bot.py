import os
import time
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------------- TOKEN ----------------
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise Exception("Missing TOKEN")

# ---------------- ONLY ONE LINK RULE ----------------
CASINO_LINK = "https://example.com"

PH = timezone(timedelta(hours=8))

# ---------------- SMOOTH CLICK SYSTEM ----------------
click_cache = {}

def smooth_click(uid, action):
    now = time.time()
    key = f"{uid}:{action}"
    last = click_cache.get(key, 0)

    if now - last < 0.15:
        return False

    click_cache[key] = now
    return True

# ---------------- FULL GAME DATA (UNCHANGED) ----------------
games = {
    "JILI": ["Super Ace","Golden Empire","Boxing King","Crazy 777","Money Coming","Lucky Jaguar",
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
    "Double Fortune","Crypto Gold","Dragon Legend","Candy Burst","Phoenix Rises",
    "Santa Gift Rush","Heist Stakes","Wild Coaster","Journey to Wealth",
    "Dragon Tiger Luck","Fortune Mouse","Alchemy Gold","Captain Bounty",
    "Mermaid Riches","Jurassic Kingdom","Vampire Night","Emoji Riches",
    "Shark Hunter","Bali Vacation","Piggy Gold","Opera Dynasty","Wild Fireworks",
    "Legend Perseus","Leprechaun Riches","Crypto Panda","Buffalo Win",
    "Mahjong Ways 3","Golden Pig","Lucky Clover","Supermarket Spree",
    "Mahjong Royal","Fortune Rabbit","Candy Bonanza"],

    "PRAGMATIC": ["Gates of Olympus","Sweet Bonanza","Sugar Rush","Big Bass Bonanza","Wolf Gold",
    "The Dog House","Wild West Gold","Buffalo King","Madame Destiny","Fire Strike",
    "Aztec Gems","John Hunter","Release the Kraken","Hot Safari","Extra Juicy",
    "Fruit Party","Sugar Rush 1000","Sweet Xmas","Olympus 1000","Starlight Princess",
    "Power of Thor","Viking Forge","Hand of Midas","Caesars Gold","Chilli Heat",
    "5 Lions Megaways","Mustang Gold","Madame Megaways","Bronco Spirit","Cowboy Coins",
    "Pixie Wings","Aztec King","Wild Walker","Cosmic Cash","Treasure Wild",
    "Fruit Party 2","Gates of Hades","Powernudge","Bigger Bass","Black Bull",
    "Gold Party","Fire Hot 40","Lucky Lightning","Magic Maze","Super X",
    "Vegas Nights","Ultra Hold","Mystery Symbols","Golden Odyssey"]
}

# ---------------- PAGINATION ----------------
PAGE_SIZE = 10

def paginate(items, page):
    start = page * PAGE_SIZE
    return items[start:start + PAGE_SIZE]

def max_page(provider):
    return max(0, (len(games[provider]) - 1) // PAGE_SIZE)

# ---------------- MENU ----------------
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("JILI", callback_data="JILI"),
         InlineKeyboardButton("PG", callback_data="PG")],
        [InlineKeyboardButton("PRAGMATIC", callback_data="PRAGMATIC")]
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
        "🎮 Welcome Bossing!",
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
        items = paginate(games[data], page)
        maxp = max_page(data)

        msg = f"🎰 {data}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n\n"

        # 🔥 REQUIRED FINAL LINE RULE
        msg += "\n🚫 RESTRICTED THIS ONLY LINK WORKS\n"
        msg += f"{CASINO_LINK}"

        kb = [
            [
                InlineKeyboardButton("⬅️", callback_data=f"page_{data}_{max(0,page-1)}"),
                InlineKeyboardButton(f"1/{maxp+1}", callback_data="noop"),
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

        if provider not in games:
            return

        items = paginate(games[provider], page)
        maxp = max_page(provider)

        msg = f"🎰 {provider}\n\n"

        for g in items:
            msg += f"🎮 {g}\n🕐 {get_time()}\n\n"

        # 🔥 SAME FINAL RULE
        msg += "\n🚫 RESTRICTED THIS ONLY LINK WORKS\n"
        msg += f"{CASINO_LINK}"

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

# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
