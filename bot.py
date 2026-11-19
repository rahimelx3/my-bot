import telebot
from telebot import types
import yt_dlp
import os

BOT_TOKEN = "9037733679:AAFWq47decaeZCuY7aPY2rWZEQ4KDBKCy6U"
bot = telebot.TeleBot(BOT_TOKEN)

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎬 تحميل فيديو", callback_data="video"),
        types.InlineKeyboardButton("🎵 تحميل صوت MP3", callback_data="audio"),
        types.InlineKeyboardButton("❓ مساعدة", callback_data="help"),
        types.InlineKeyboardButton("ℹ️ عن البوت", callback_data="about")
    )
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    text = (
        "أهلاً بيك في بوت تحميل فيديوهات من سوشيال ميديا 🎬🔥\n\n"
        "هنا تقدر تحمل أي فيديو بضغطة واحدة\n\n"
        "✨ بيدعم:\n"
        "🎥 يوتيوب\n"
        "🎵 تيك توك\n"
        "📸 انستجرام\n"
        "📘 فيسبوك\n\n"
        "🚀 ابعت أي رابط وأنا هجيبهولك فوراً\n"
        "👇 اختار من الزرارير تحت:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def buttons(call):
    if call.data == "video":
        bot.send_message(call.message.chat.id, "🎬 تمام، ابعتلي رابط الفيديو دلوقتي.")
    elif call.data == "audio":
        bot.send_message(call.message.chat.id, "🎵 تمام، ابعتلي رابط الفيديو وأنا هحولهولك MP3.")
    elif call.data == "help":
        bot.send_message(call.message.chat.id, "❓ ابعت رابط الفيديو بس وأنا هنزلهولك.\n⚠️ آخر الفيديو 50 ميجا عشان حدود تيليجرام")
    elif call.data == "about":
        bot.send_message(call.message.chat.id, "ℹ️ بوت تحميل فيديوهات من سوشيال ميديا 🎬")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: m.text and m.text.startswith("http"))
def download(message):
    url = message.text.strip()
    msg = bot.send_message(message.chat.id, "🔄 جاري التحميل... استنى شوية ⏳")
    ydl_opts = {'outtmpl': 'video_%(id)s.%(ext)s','format': 'best[filesize<50M]/best','quiet': True,'noplaylist': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        bot.edit_message_text("📤 جاري الرفع...", chat_id=message.chat.id, message_id=msg.message_id)
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التحميل ✅🔥", reply_markup=main_menu())
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ حصل خطأ: {e}", chat_id=message.chat.id, message_id=msg.message_id)

print("البوت شغال...")
bot.infinity_polling()
