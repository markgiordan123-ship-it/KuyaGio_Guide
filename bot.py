import random
from datetime import date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ---- CONFIG ----
TOKEN = "8577695558:AAEm8ZtcjqYYPbqo576JlwNkmJrytYycb_g"
CASINO_LINK = "http://kuyax333.paldopinas96.cc/?referralCode=opl5030"
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"

# All providers and all their games
games = {
    "JILI": ["Super Ace Deluxe", "Mega Ace", "Golden Empire", "Lucky Dragon"],
    "PG": ["Mahjong Ways", "Lucky Neko", "Treasure Hunt", "Dragon Legend"],
    "CQ9": ["Fire Phoenix", "Golden Rooster", "Fortune King", "Mystery Temple"],
    "Pragmatic": ["Sweet Bonanza", "The Dog House", "Wild West Gold", "Great Rhino"]
}

daily_data = {}
saved_date = ""
user_lang = {}

# --- FUNCTIONS ---
def gen_time(slot=None):
    """Generate random time within a slot (Morning, Afternoon, Evening)"""
    if slot == "Morning":
        h = random.randint(8,11)
    elif slot == "Afternoon":
        h = random.randint(12,16)
    elif slot == "Evening":
        h = random.randint(17,21)
    else:
        h = random.randint(8,21)
    m = random.choice([0,10,20,30,40,50])
    me = m+20
    if me >= 60:
        me -= 60
        h +=1
        if h>23:
            h = h-24
    p = "AM" if h<12 else "PM"
    h12 = h if h<=12 else h-12
    return f"{h12}:{m:02d} {p} - {h12}:{me:02d} {p}"

def gen_daily():
    """Generate daily times for all games in all providers"""
    global daily_data
    daily_data = {}
    for provider, game_list in games.items():
        daily_data[provider] = {}
        for game in game_list:
            slot = random.choice(["Morning","Afternoon","Evening"])
            daily_data[provider][game] = gen_time(slot)

def get_msg(provider,lang):
    """Prepare the full guide message for all games in the provider"""
    msg_lines = []
    msg_lines.append(f"🎰 {provider} GUIDE 🎰" if lang=="EN" else f"🎰 {provider} ORAS NG LARO 🎰")
    for game, time in daily_data[provider].items():
        msg_lines.append(f"🎮 {game}\n🕐 {time}\n👉 {CASINO_LINK}")
    msg_lines.append("\n🌐 MORE GUIDE IN HERE:\n" + CANVA_LINK)
    return "\n\n".join(msg_lines)

# --- TELEGRAM HANDLERS ---
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("English",callback_data="lang_EN"),
           InlineKeyboardButton("Tagalog",callback_data="lang_TL")]]
    await update.message.reply_text("Choose your language / Piliin ang wika:",reply_markup=InlineKeyboardMarkup(kb))

async def button(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    uid = q.from_user.id
    global saved_date

    today = str(date.today())
    if today != saved_date:
        gen_daily()
        saved_date = today

    if data.startswith("lang_"):
        user_lang[uid] = data.split("_")[1]
        kb = [[InlineKeyboardButton(p,callback_data=f"prov_{p}")] for p in games.keys()]
        await q.edit_message_text("Select provider:" if user_lang[uid]=="EN" else "Pumili ng provider:",
                                  reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("prov_"):
        prov = data.split("_")[1]
        lang = user_lang.get(uid,"EN")
        msg = get_msg(prov,lang)
        # Add "HourGuide" button to let user see other games again
        kb = [[InlineKeyboardButton("HourGuide 🔄",callback_data=f"prov_{prov}")]]
        await q.edit_message_text(msg,reply_markup=InlineKeyboardMarkup(kb))

async def text(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please use the buttons to select language and provider.")

# --- MAIN ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,text))
app.run_polling()
