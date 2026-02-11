import os
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# إعدادات السيرفر الوهمي لإبقاء البوت يعمل
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running"

def run():
    app_web.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# إعدادات المتغيرات البيئية
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# القنوات (المصدر والوجهة)
# يمكن وضع معرف القناة (رقم) أو اليوزرنيم (بدون @)
FROM_CHANNEL = int(os.environ.get("FROM_CHANNEL")) 
TO_CHANNEL = int(os.environ.get("TO_CHANNEL"))

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@bot.on_message(filters.chat(FROM_CHANNEL) & (filters.document | filters.video | filters.photo | filters.audio))
def copy_content(client, message):
    try:
        # نسخ الرسالة إلى القناة الوجهة
        message.copy(TO_CHANNEL)
        print(f"Copied message: {message.id}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    keep_alive() # تشغيل السيرفر الوهمي
    bot.run() # تشغيل البوت
