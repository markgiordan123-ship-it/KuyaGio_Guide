import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ---- CONFIG ----
TOKEN = "8577695558:AAEm8ZtcjqYYPbqo576JlwNkmJrytYycb_g"
CASINO_LINK = "http://kuyax333.paldopinas96.cc/?referralCode=opl5030"
CANVA_LINK = "https://kuyagiometerguide.my.canva.site/"
SUPPORT_LINK = "https://t.me/KuyaGioPaldo"

# ---- PROVIDERS ----
games = {
    "JILI": [ "SUPER ACE","GOLDEN EMPIRE","BOXING KING","CRAZY777","MONEY COMING","LUCKY JAGUAR",
        "SHANGHAI BEAUTY","FORTUNE GEMS","WILD ACE","GOLDEN BANK 2","Shōgun","3 LUCKY PIGS",
        "3 COIN TREASURES","NIGHTFALL HUNTING","MONEY POT","FRUITY WHEEL","AZTEC PRIESTESS",
        "BANGLA BEAUTY","GO FOR CHAMPION","EGYPT GLOW","MAGIC LAMP","NIGHT CITY","LEGACY OF EGYPT",
        "PIRATE QUEEN","GOLDEN TEMPLE","JACKPOT JOKER","CANDY BABY","MINES GOLD","LUCKY GOLDBRICKS",
        "BONUS HUNTER","PARTY STAR","KING ARTHUR","WAR DRAGONS","BOOK OF GOLD","SWEET LAND",
        "BOXING EXTRAVAGANZA","SIN CITY","GOLDEN BANK","PHARAOH TREASURE","WITCHES NIGHT",
        "ARENA FIGHTER","LUCKY DOGGY","FORTUNE TREE","BONE FORTUNE","GOLDEN QUEEN",
        "MASTER TIGER","JUNGLE KING","SAMBA","GOLDEN JOKER","NEKO FORTUNE","ELF BINGO",
        "AGENT ACE","JACKPOT BINGO","WILD RACER","GOD OF MARTIAL","GEM PARTY","LUCKY BALL",
        "HYPER BURST","FA FA FA","HAWAII BEAUTY","SEVENSEVENSEVEN","FORTUNE PIG",
        "BAO BOON CHIN","XIYANGYANG","DIAMOND PARTY","MONKEY PARTY","SUPER RICH",
        "ROMAX","TWIN WINS","MEDUSA","THOR X","CRAZY PUSHER","WORLD CUP",
        "CRICKET KING 18","CRICKET SAH 75","CRAZY HUNTER 2","MONEY COMING EXPAND BETS",
        "SUPER ACE SCRATCH","XI YANG YANG","SEVEN SEVEN SEVEN","SUPER E-SABONG",
        "FORTUNE GEMS SCRATCH","MONEY COMING 2","SUPER ACE II","3 CHARGE BUFFALO",
        "MONEY POT DELUXE","DEVIL FIRE 2","DEVIL FIRE","CHARGE BUFFALO ASCENT",
        "FORTUNE GEMS 2","ZEUS","SUPER ACE DELUXE"
    ],
    "PG": ["Mahjong Ways","Mahjong Ways 2","Lucky Neko","Fortune Tiger","Dragon Hatch","Wild Bandito"],
    "PRAGMATIC": ["Sweet Bonanza","Gates of Olympus","Starlight Princess","Wild West Gold","Fruit Party"],
    "FA CHAI": ["Fa Chai Riches","Golden Monkey","Lucky Twins","Dragon Treasure"]
}

user_lang = {}

# --- TIME SYSTEM ---
def gen_time():
    now = datetime.now()
    is_am = now.hour < 12
    h = random.randint(8,11) if is_am else random.randint(1,11)
    m = random.choice([0,10,20,30,40])
    p = "AM" if is_am else "PM"
    return f"{h}:{m:02d} {p} - {h}:{(m+20)%60:02d} {p}"

# --- GENERATE DATA ---
def generate(provider):
    lst = games[provider][:]
    random.shuffle(lst)
    return {g:gen_time() for g in lst}

# --- PAGINATION ---
def paginate(data, page=0, per_page=10):
    items = list(data.items())
    return items[page*per_page:(page+1)*per_page], len(items)//per_page+1

# --- MESSAGE ---
def build_msg(provider, data, page, lang):
    chunk, total_pages = paginate(data, page)
    msg = []
    msg.append("🌐 MORE GUIDE IN HERE:\n"+CANVA_LINK)
    msg.append("⚠️ FOR PALDOPINAS USERS ONLY!")
    msg.append("📩 NEED HELP? "+SUPPORT_LINK)
    msg.append("")
    msg.append(f"🎰 {provider} PROVIDER 🎰")
    for g,t in chunk:
        msg.append(f"🎮 {g}\n🕐 {t}\n👉 {CASINO_LINK}")
    return "\n\n".join(msg), total_pages

# --- START ---
async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    kb=[[InlineKeyboardButton("English",callback_data="lang_EN"),
         InlineKeyboardButton("Tagalog",callback_data="lang_TL")]]
    await update.message.reply_text("Choose language:",reply_markup=InlineKeyboardMarkup(kb))

# --- BUTTON ---
async def button(update:Update, context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()
    d=q.data
    uid=q.from_user.id

    if d.startswith("lang_"):
        user_lang[uid]=d.split("_")[1]
        kb=[[InlineKeyboardButton(p,callback_data=f"prov_{p}")] for p in games]
        await q.edit_message_text("Select provider:",reply_markup=InlineKeyboardMarkup(kb))

    elif d.startswith("prov_"):
        prov=d.split("_")[1]
        data=generate(prov)
        msg,tp=build_msg(prov,data,0,"EN")

        buttons=[[InlineKeyboardButton(str(i+1),callback_data=f"page_{prov}_{i}") for i in range(tp)]]
        buttons.append([InlineKeyboardButton("HourGuide 🔄",callback_data=f"prov_{prov}")])
        buttons.append([InlineKeyboardButton("Change Provider 🔘",callback_data="back")])

        await q.edit_message_text(msg,reply_markup=InlineKeyboardMarkup(buttons))

    elif d.startswith("page_"):
        _,prov,page=d.split("_")
        page=int(page)
        data=generate(prov)
        msg,tp=build_msg(prov,data,page,"EN")

        buttons=[[InlineKeyboardButton(str(i+1),callback_data=f"page_{prov}_{i}") for i in range(tp)]]
        buttons.append([InlineKeyboardButton("HourGuide 🔄",callback_data=f"prov_{prov}")])
        buttons.append([InlineKeyboardButton("Change Provider 🔘",callback_data="back")])

        await q.edit_message_text(msg,reply_markup=InlineKeyboardMarkup(buttons))

    elif d=="back":
        kb=[[InlineKeyboardButton(p,callback_data=f"prov_{p}")] for p in games]
        await q.edit_message_text("Select provider:",reply_markup=InlineKeyboardMarkup(kb))

# --- SEARCH ---
async def text(update:Update, context:ContextTypes.DEFAULT_TYPE):
    txt=update.message.text.lower()
    for p in games:
        for g in games[p]:
            if txt in g.lower():
                await update.message.reply_text(f"🎮 {g}\n🕐 {gen_time()}\n👉 {CASINO_LINK}")
                return
    await update.message.reply_text("Game not found.")

# --- MAIN ---
app=ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,text))

app.run_polling()
