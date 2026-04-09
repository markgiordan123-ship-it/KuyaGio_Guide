import random
from datetime import date
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ---- CONFIG ----
TOKEN = "8577695558:AAEm8ZtcjqYYPbqo576JlwNkmJrytYycb_g"
CASINO_LINK = "http://kuyax333.paldopinas96.cc/?referralCode=opl5030"
games = {"JILI":["Super Ace Deluxe","Mega Ace","Golden Empire"],"PG":["Mahjong Ways","Lucky Neko"]}
daily_data = {}
saved_date = ""
user_lang = {}

# --- FUNCTIONS ---
def gen_time():
    h = random.randint(1,12)
    m = random.choice([0,10,20,30,40])
    me = m+20
    p = random.choice(["AM","PM"])
    return f"{h}:{m:02d} {p} - {h}:{me:02d} {p}"

def gen_daily():
    global daily_data
    for p in games: daily_data[p] = {"game": random.choice(games[p]), "time": gen_time()}

def get_msg(provider,lang):
    d = daily_data[provider]
    if lang=="EN":
        return f"🎰 {provider} RESULT 🎰\n🎮 Game: {d['game']}\n🕐 Time: {d['time']}\n👉 PLAY NOW:\n{CASINO_LINK}"
    else:
        return f"🎰 {provider} RESULT 🎰\n🎮 Laro: {d['game']}\n🕐 Oras: {d['time']}\n👉 LARO NGAYON:\n{CASINO_LINK}"

# --- TELEGRAM HANDLERS ---
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("English",callback_data="lang_EN"),InlineKeyboardButton("Tagalog",callback_data="lang_TL")]]
    await update.message.reply_text("Choose your language / Piliin ang wika:",reply_markup=InlineKeyboardMarkup(kb))

async def button(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    uid = q.from_user.id
    global saved_date
    if d.startswith("lang_"):
        user_lang[uid] = d.split("_")[1]
        kb = [[InlineKeyboardButton(p,callback_data=f"prov_{p}")] for p in games.keys()]
        await q.edit_message_text("Select provider:" if user_lang[uid]=="EN" else "Pumili ng provider:",reply_markup=InlineKeyboardMarkup(kb))
    elif d.startswith("prov_"):
        prov = d.split("_")[1]
        lang = user_lang.get(uid,"EN")
        today = str(date.today())
        if today != saved_date: gen_daily(); saved_date = today
        await q.edit_message_text(get_msg(prov,lang))

async def text(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please use the buttons to select language and provider.")

# --- MAIN ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,text))
app.run_polling()
