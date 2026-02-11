import os
import logging
from threading import Thread
from flask import Flask
from pyrogram import Client, filters

# ══════════════════════════════════════════
#              إعدادات اللوق
# ══════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════
#        سيرفر ويب (مطلوب لـ Render)
# ══════════════════════════════════════════
flask_app = Flask(__name__)


@flask_app.route("/")
def home():
    return "✅ Bot is running!"


@flask_app.route("/health")
def health():
    return "OK", 200


def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)


# ══════════════════════════════════════════
#              إعدادات البوت
# ══════════════════════════════════════════
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

# معرّفات القنوات المصدر (ممكن أكثر من قناة، مفصولة بفاصلة)
# مثال: -1001234567890,-1009876543210
SOURCE_CHANNELS = [
    int(x.strip())
    for x in os.environ["SOURCE_CHANNELS"].split(",")
]

# معرّف قناة الوجهة (قناتك)
DEST_CHANNEL = int(os.environ["DEST_CHANNEL"])

# وضع التوجيه:
#   "files"  = ملفات فقط (مستندات، صور، فيديو، صوت)
#   "all"    = جميع الرسائل
FORWARD_MODE = os.environ.get("FORWARD_MODE", "files")

# طريقة الإرسال:
#   "copy"    = إرسال بدون علامة "Forwarded from"
#   "forward" = إرسال مع علامة "Forwarded from"
SEND_METHOD = os.environ.get("SEND_METHOD", "copy")

# ══════════════════════════════════════════
#              إنشاء العميل
# ══════════════════════════════════════════
app = Client(
    "forwarder",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# ══════════════════════════════════════════
#              فلتر الملفات
# ══════════════════════════════════════════
FILES_FILTER = (
    filters.document
    | filters.video
    | filters.audio
    | filters.photo
    | filters.voice
    | filters.video_note
    | filters.animation
)

# تحديد الفلتر حسب الوضع
if FORWARD_MODE == "files":
    message_filter = filters.chat(SOURCE_CHANNELS) & FILES_FILTER
else:
    message_filter = filters.chat(SOURCE_CHANNELS)


# ══════════════════════════════════════════
#           معالج الرسائل
# ══════════════════════════════════════════
@app.on_message(message_filter)
async def forward_handler(client, message):
    try:
        if SEND_METHOD == "forward":
            await message.forward(chat_id=DEST_CHANNEL)
        else:
            await message.copy(chat_id=DEST_CHANNEL)

        logger.info(
            f"✅ تم توجيه الرسالة {message.id} "
            f"من [{message.chat.title}]"
        )
    except Exception as e:
        logger.error(
            f"❌ خطأ في توجيه الرسالة {message.id}: {e}"
        )


# ══════════════════════════════════════════
#              التشغيل
# ══════════════════════════════════════════
if __name__ == "__main__":
    # تشغيل سيرفر الويب في thread منفصل
    web_thread = Thread(target=start_web_server, daemon=True)
    web_thread.start()
    logger.info("🌐 سيرفر الويب يعمل")

    # تشغيل البوت
    logger.info("🤖 جاري تشغيل البوت...")
    logger.info(f"📡 مراقبة {len(SOURCE_CHANNELS)} قناة")
    logger.info(f"📨 الوجهة: {DEST_CHANNEL}")
    logger.info(f"📋 الوضع: {FORWARD_MODE}")
    app.run()
