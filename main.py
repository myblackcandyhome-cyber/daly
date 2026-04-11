import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ตั้งค่า Log เพื่อดูสถานะผ่านหน้าเว็บ Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ดึง Token จาก Environment Variable (ที่เราจะไปตั้งใน Railway)
TOKEN = os.getenv('BOT_TOKEN')

async def delete_service_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ฟังก์ชันลบข้อความระบบ (คนเข้า/คนออก)"""
    try:
        await context.bot.delete_message(
            chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        logging.info(f"ลบข้อความแจ้งเตือนในกลุ่ม: {update.message.chat.title}")
    except Exception as e:
        logging.error(f"ไม่สามารถลบข้อความได้: {e}")

if __name__ == '__main__':
    if not TOKEN:
        logging.error("หา BOT_TOKEN ไม่เจอ! กรุณาเช็คการตั้งค่า Variables ใน Railway")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()

    # ดักจับทั้งข้อความคนเข้า (NEW_CHAT_MEMBERS) และคนออก (LEFT_CHAT_MEMBER)
    service_filter = (filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER)
    app.add_handler(MessageHandler(service_filter, delete_service_message))

    logging.info("บอทเริ่มทำงานแล้ว...")
    app.run_polling()
