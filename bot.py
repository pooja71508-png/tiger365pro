from telegram import Update, ReplyKeyboardRemove
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

TOKEN = "XXXXXX"
ADMIN_CHAT_ID = "XXXXXX"

NAME, MOBILE = range(2)

WELCOME_MESSAGE = """
🎉 Welcome to Tiger365.pro 🎉

🏆 Premium Gaming Experience
⚡ Fast Registration
🔐 Secure Account Access
💎 Exclusive Member Benefits

Please enter your Full Name to continue.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📱 Please enter your Mobile Number:")
    return MOBILE

async def get_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data["name"]
    mobile = update.message.text

    user_id = "TG" + "".join(random.choices(string.digits, k=6))
    password = "".join(random.choices(string.ascii_letters + string.digits, k=8))

    await update.message.reply_text(
        f"✅ Registration Successful\\n\\n👤 Name: {name}\\n📱 Mobile: {mobile}\\n\\n🆔 User ID: {user_id}\\n🔐 Password: {password}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"New Registration\\n\\nName: {name}\\nMobile: {mobile}\\nUser ID: {user_id}\\nPassword: {password}"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registration Cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            MOBILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_mobile)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
