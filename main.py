import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ตั้งค่า Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv('BOT_TOKEN')

async def delete_service_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ฟังก์ชันลบข้อความแจ้งเตือนทันที"""
    try:
        # สั่งลบข้อความ
        success = await context.bot.delete_message(
            chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        if success:
            logging.info(f"ลบข้อความสำเร็จในกลุ่ม: {update.message.chat.title}")
    except Exception as e:
        # หากลบไม่ได้ (เช่น บอทไม่ใช่ Admin หรือข้อความถูกลบไปก่อนแล้ว)
        logging.error(f"ไม่สามารถลบข้อความได้: {e}")

if __name__ == '__main__':
    if not TOKEN:
        logging.error("กรุณาตั้งค่า BOT_TOKEN ใน Railway Variables")
        exit(1)

    # สร้าง Application
    app = ApplicationBuilder().token(TOKEN).build()

    # ปรับ Filter ให้ครอบคลุม New Members และ Left Member
    # filters.StatusUpdate.NEW_CHAT_MEMBERS ครอบคลุมทั้งเข้าเองและถูกเพิ่มโดยคนอื่น
    service_filter = (filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER)
    
    app.add_handler(MessageHandler(service_filter, delete_service_message))

    logging.info("บอทเริ่มทำงาน (โหมดความเร็วสูง)...")

    # ปรับแต่งพารามิเตอร์เพื่อความเร็ว
    # poll_interval: ระยะเวลารอระหว่างเช็คข้อความ (0.0 หมายถึงเช็คทันทีที่ทำได้)
    # bootstrap_retries: พยายามเชื่อมต่อใหม่หากเน็ตหลุด
    app.run_polling(poll_interval=0.1, bootstrap_retries=5)
