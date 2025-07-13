import os
import uuid
import string
import random
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

try:
    from cfonts import render
except ImportError:
    os.system('pip install python-cfonts')
    from cfonts import render

# Setup
R = "\033[1;31m"
G = "\033[1;32m"
B = "\033[0;94m"
Y = "\033[1;33m"
CF = render('{Niksoriginals}', colors=['white', 'cyan'], align='center')
print(CF)

# Logging
logging.basicConfig(level=logging.INFO)

# Env vars
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID", "0"))
TARGET_THREAD_ID = int(os.environ.get("TARGET_THREAD_ID", "0"))

if not BOT_TOKEN or CHAT_ID == 0 or TARGET_THREAD_ID == 0:
    print("❌ BOT_TOKEN, CHAT_ID, or TARGET_THREAD_ID not set properly.")
    exit()

# Core reset class (from your original)
class og69x:
    def __init__(self, target: str):
        self.target = target

        if self.target.startswith("@"):
            self.result = "[ - ] Enter User Without '@'"
            return

        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        guid = str(uuid.uuid4())
        device = str(uuid.uuid4())

        if "@" in self.target:
            self.data = {
                "_csrftoken": token,
                "user_email": self.target,
                "guid": guid,
                "device_id": device
            }
        else:
            self.data = {
                "_csrftoken": token,
                "username": self.target,
                "guid": guid,
                "device_id": device
            }

        self.result = self.send_password_reset()

    def send_password_reset(self):
        ua = f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; " + \
             f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/" + \
             f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; " + \
             f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; " + \
             f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; " + \
             f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)"

        head = {
            "user-agent": ua
        }

        req = requests.post(
            "https://i.instagram.com/api/v1/accounts/send_password_reset/",
            headers=head,
            data=self.data
        )

        if "obfuscated_email" in req.text:
            return f"[ + ] {req.text}"
        else:
            return f"[ - ] {req.text}"

# Telegram handler
async def gmail_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message is None:
            return
        if update.message.chat.id != CHAT_ID:
            return
        if update.message.message_thread_id != TARGET_THREAD_ID:
            return

        if not context.args:
            await update.message.reply_text("❌ Usage: /g email_or_username", parse_mode="Markdown")
            return

        target = context.args[0]
        result = og69x(target).result
        await update.message.reply_text(f"Result for `{target}`:\n\n{result}", parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# Optional: get group/thread ID
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        chat_id = update.message.chat_id
        thread_id = update.message.message_thread_id
        await update.message.reply_text(
            f"Chat ID: `{chat_id}`\nThread ID: `{thread_id}`", parse_mode="Markdown"
        )

# Runner
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("g", gmail_reset))
    app.add_handler(CommandHandler("info", info))
    print(G + "[+] Bot is running..." + B)
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
