import os
import uuid
import string
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

try:
    from cfonts import render
except ImportError:
    os.system('pip install python-cfonts')
    from cfonts import render

# Banner (optional)
CF = render('OG69X Reset', colors=['white', 'cyan'], align='center')
print(CF)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID", "0"))
TARGET_THREAD_ID = int(os.environ.get("TARGET_THREAD_ID", "0"))

def is_allowed(update: Update) -> bool:
    # Only allow in the specified group/thread
    if update.effective_chat.id != CHAT_ID:
        return False
    if update.effective_message.message_thread_id and update.effective_message.message_thread_id != TARGET_THREAD_ID:
        return False
    return True

def base_reset_logic(target):
    # === YAHI AAPKA BASE CODE HAI, KUCH NA BADLA ===
    if target.startswith("@"):
        return "[ - ] Enter User Without '@'"

    if "@" in target:
        data = {
            "_csrftoken": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
            "user_email": target,
            "guid": str(uuid.uuid4()),
            "device_id": str(uuid.uuid4())
        }
    else:
        data = {
            "_csrftoken": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
            "username": target,
            "guid": str(uuid.uuid4()),
            "device_id": str(uuid.uuid4())
        }
    head = {
        "user-agent": (
            "Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; "
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/"
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)"
        )
    }
    try:
        req = requests.post(
            "https://i.instagram.com/api/v1/accounts/send_password_reset/",
            headers=head,
            data=data,
            timeout=10
        )
        if "obfuscated_email" in req.text:
            return f"[ + ] {req.text}"
        elif "wait a few minutes" in req.text:
            return "❌ Failed: wait a few minutes before you try again."
        else:
            return f"[ - ] {req.text}"
    except Exception as e:
        return f"[ ! ] Error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 OG69X Reset Bot!\n"
        "Use /reset <username/email> to send Instagram reset."
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    args = context.args
    if not args:
        await update.message.reply_text("❗ Usage:\n/reset <username/email>")
        return
    target = args[0]
    msg = await update.message.reply_text("⏳ Sending Instagram reset request...")
    result = base_reset_logic(target)
    await msg.edit_text(result)

def main():
    try:
        print(f"BOT_TOKEN: {BOT_TOKEN}")
        print(f"CHAT_ID: {CHAT_ID}")
        print(f"TARGET_THREAD_ID: {TARGET_THREAD_ID}")
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("reset", reset))
        app.run_polling()
    except Exception as e:
        print(f"Startup Error: {e}")

if __name__ == "__main__":
    main()
