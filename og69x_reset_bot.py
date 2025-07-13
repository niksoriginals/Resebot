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

# Logging for debug
logging.basicConfig(level=logging.INFO)

# Env vars
BOT_TOKEN = os.environ.get("BOT_TOKEN")
TARGET_THREAD_ID = int(os.environ.get("TARGET_THREAD_ID", "0"))
CHAT_ID = int(os.environ.get("CHAT_ID", "0"))

# Sanity check for env vars
if not BOT_TOKEN or CHAT_ID == 0 or TARGET_THREAD_ID == 0:
    print("❌ BOT_TOKEN, CHAT_ID, or TARGET_THREAD_ID is not set properly.")
    exit()

# Terminal header
R = "\033[1;31m"
G = "\033[1;32m"
B = "\033[0;94m"
Y = "\033[1;33m"
CF = render('{Niksoriginals}', colors=['white', 'cyan'], align='center')
print(CF)

# Instagram reset logic
class og69x:
    def __init__(self, target: str):
        self.target = target

        if self.target.startswith("@"):
            self.result = "[ - ] Enter User Without '@'"
            return

        if "@" in self.target:
            self.data = {
                "_csrftoken": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
                "user_email": self.target,
                "guid": str(uuid.uuid4()),
                "device_id": str(uuid.uuid4())
            }
        else:
            self.data = {
                "_csrftoken": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
                "username": self.target,
                "guid": str(uuid.uuid4()),
                "device_id": str(uuid.uuid4())
            }

        self.result = self.send_password_reset()

    def send_password_reset(self):
        head = {
            "user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/"
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)"
        }
        req = requests.post(
            "https://i.instagram.com/api/v1/accounts/send_password_reset/",
            headers=head,
            data=self.data)

        if "obfuscated_email" in req.text:
            return f"[ + ] Powered by OG69X"
        else:
            return f"[ - ] {req.text}"

# Telegram command handler
async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message is None:
            return

        if update.message.chat.id != CHAT_ID:
            return

        if update.message.message_thread_id != TARGET_THREAD_ID:
            return

        if not context.args:
            await update.message.reply_text("❌ Use `/reset email_or_username`", parse_mode='Markdown')
            return

        user_input = context.args[0]
        result = og69x(user_input).result
        await update.message.reply_text(f"Result for `{user_input}`:\n\n{result}", parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"❌ Error occurred: {str(e)}")

# Main runner
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("reset", reset_command))
    print(G + "[+] Bot is running..." + B)
    await app.run_polling()

# Run it
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

