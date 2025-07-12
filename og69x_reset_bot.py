import os
import asyncio
import uuid
import string
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Config from environment variables (set these in Railway/Render) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
TARGET_THREAD_ID = int(os.environ.get("TARGET_THREAD_ID", "0"))
CHAT_ID = int(os.environ.get("CHAT_ID", "0"))

def send_password_reset(target: str):
    """Send Instagram password reset request."""
    target = target.strip()
    if target.startswith("@"):
        return "Send username without @"
    data = {
        "user_email": target if "@" in target else "",
        "username": target if "@" not in target else "",
        "_csrftoken": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
        "guid": str(uuid.uuid4()),
        "device_id": str(uuid.uuid4())
    }
    headers = {
        "user-agent": (
            "Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; "
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))})"
        )
    }
    try:
        resp = requests.post(
            "https://i.instagram.com/api/v1/accounts/send_password_reset/",
            headers=headers,
            data=data,
            timeout=10
        )
        if resp.status_code == 200 and "obfuscated_email" in resp.text:
            return f"✅ Success"
        else:
            return f"❌ Failed: {resp.text}"
    except Exception as e:
        return f"❌ Error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to *OG69x Reset*!\n"
        "Send /reset <username/email> to use the reset function.\n"
        "Works only in @og69y group/topic.",
        parse_mode="Markdown"
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Restrict to specific thread/topic if set
    if TARGET_THREAD_ID and (update.effective_message.message_thread_id != TARGET_THREAD_ID):
        return
    # Restrict to specific chat if set
    # if CHAT_ID and (update.effective_chat.id != CHAT_ID):
    #     return
    if not context.args:
        await update.message.reply_text("Usage: /reset <username or email>")
        return
    target = " ".join(context.args)
    # Step 1: Send initial message
    status_message = await update.message.reply_text("✅ Got it...")

    # Step 2: Simulate progress with edits
    await asyncio.sleep(.5)
    await status_message.edit_text("⏳ Processing your request...")
    
    await asyncio.sleep(1)
    await status_message.edit_text("🚀 *Powered by* [@og69x]")

    await asyncio.sleep(1.2)
    await status_message.edit_text("📡 Sending password reset request to Instagram...")

    # Step 3: Perform actual reset
    result = send_password_reset(target)
    await asyncio.sleep(1)
    await status_message.edit_text(f"{result}\nPowered by [@og69x](https://t.me/og69x)", parse_mode="Markdown", disable_web_page_preview=True)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.run_polling()

if __name__ == "__main__":
    main()
