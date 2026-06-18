from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
import random
import string
import os

TOKEN = "8719632545:AAHQ-ykDu0tOcxpB1BNJMQqUbZ7gY3jV-4U"

NAME, PHONE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Tiger365.pro me aapka swagat hai!\n\n"
        "📝 Kripya apna naam darj kare:"
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        "📱 Ab apna mobile number bhejiye:"
    )
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data["name"]
    phone = update.message.text

    userid = "TG" + str(random.randint(100000, 999999))
    password = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=8
    ))

    await update.message.reply_text(
        f"✅ Account Request Successful\n\n"
        f"👤 Name: {name}\n"
        f"📱 Mobile: {phone}\n\n"
        f"🆔 User ID: {userid}\n"
        f"🔐 Password: {password}\n\n"
        f"💬 Sahayata ke liye:\n"
        f"https://t.me/Shreya_MM"
    )

    # Admin notification
    ADMIN_CHAT_ID ="7038610091"  # apna Telegram ID daalo

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            "🆕 New Lead Received\n\n"
            f"👤 Name: {name}\n"
            f"📱 Mobile: {phone}\n"
            f"🆔 User ID: {userid}\n"
            f"🔐 Password: {password}"
        )
    )

    return ConversationHandler.END

app = Application.builder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
    },
    fallbacks=[],
)

app.add_handler(conv_handler)

print("Bot Started...")
app.run_polling()