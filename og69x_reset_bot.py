
import os
import uuid
import string
import random
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# --- Config from environment variables (set these in Railway/Render) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
TARGET_THREAD_ID = int(os.environ.get("TARGET_THREAD_ID", "0"))
CHAT_ID = int(os.environ.get("CHAT_ID", "0"))

def send_password_reset(target: str):
    """Send Instagram password reset request."""
    target = target.strip()
    if target.startswith("@"):
        return "🚫 Please send username without '@'"
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
            return f"✅ Reset link sent successfully!"
        else:
            return f"❌ Failed to send reset: {resp.text}"
    except Exception as e:
        return f"❌ Error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *OG69x Reset Bot*!
"
        "Use the command:
"
        "`/reset <username/email>`
"
        "to request a password reset.

"
        "🔒 Works only in @og69y group/topic.",
        parse_mode="Markdown"
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Restrict to specific thread/topic
    if TARGET_THREAD_ID and (update.effective_message.message_thread_id != TARGET_THREAD_ID):
        return
    if CHAT_ID and (update.effective_chat.id != CHAT_ID):
        return
    if not context.args:
        await update.message.reply_text("📌 Usage:
`/reset <username or email>`", parse_mode="Markdown")
        return

    target = " ".join(context.args)

    # Auto-delete user command message for clean look
    try:
        await update.message.delete()
    except:
        pass  # ignore if bot lacks permission

    # Progress message
    status_message = await update.effective_chat.send_message("✅ Got it...")

    await asyncio.sleep(1.2)
    await status_message.edit_text("⏳ Processing your request...")

    await asyncio.sleep(1.5)
    await status_message.edit_text("🚀 *Powered by* [@og69x]")

    await asyncio.sleep(1.8)
    await status_message.edit_text("📡 Sending password reset request to Instagram...")

    result = send_password_reset(target)

    await asyncio.sleep(1.2)
    await status_message.edit_text(
        f"{result}

🚀 *Powered by* [@og69x](https://t.me/og69x)",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.run_polling()

if __name__ == "__main__":
    main()

