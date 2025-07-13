import os
import asyncio
import uuid
import string
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TARGET_THREAD_ID = int(os.environ.get("TARGET_THREAD_ID", "0"))
CHAT_ID = int(os.environ.get("CHAT_ID", "0"))

def send_instagram_reset(target: str):
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

def send_gmail_reset(email: str):
    if "@gmail.com" not in email:
        return "❌ Not a Gmail address."
    # Dummy simulation since Gmail reset isn't public API-based
    return f"📧 Gmail reset link sent (simulated) to {email}"

def send_hotmail_reset(email: str):
    if "@hotmail.com" not in email and "@outlook.com" not in email and "@live.com" not in email:
        return "❌ Not a valid Hotmail/Outlook email."
    # Dummy simulation since Microsoft reset isn't public API-based
    return f"📧 Hotmail reset link sent (simulated) to {email}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to *OG69x Reset Bot*!\n"
        "• /reset <username/email> - Instagram Reset\n"
        "• /g <gmail> - Gmail Reset\n"
        "• /h <hotmail/outlook> - Hotmail Reset\n"
        "_Only works in @og69y thread/topic._",
        parse_mode="Markdown"
    )

async def reset_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, mode: str):
    if TARGET_THREAD_ID and (update.effective_message.message_thread_id != TARGET_THREAD_ID):
        return

    if not context.args:
        await update.message.reply_text("Usage: /reset <username/email> or /g <gmail> or /h <hotmail>")
        return

    target = " ".join(context.args)
    status = await update.message.reply_text("✅ Got it...")

    await asyncio.sleep(0.5)
    await status.edit_text("⏳ Processing your request...")
    await asyncio.sleep(1)
    await status.edit_text("🚀 *Powered by* [@og69x]", parse_mode="Markdown")
    await asyncio.sleep(1.2)

    if mode == "instagram":
        await status.edit_text("📡 Sending password reset request to Instagram...")
        result = send_instagram_reset(target)
    elif mode == "gmail":
        await status.edit_text("📡 Sending password reset request to Gmail...")
        result = send_gmail_reset(target)
    elif mode == "hotmail":
        await status.edit_text("📡 Sending password reset request to Hotmail...")
        result = send_hotmail_reset(target)
    else:
        result = "❌ Unknown mode."

    await asyncio.sleep(1)
    await status.edit_text(f"{result}\nPowered by [@og69x](https://t.me/og69x)", parse_mode="Markdown", disable_web_page_preview=True)

# Wrappers for command handlers
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reset_handler(update, context, "instagram")

async def gmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reset_handler(update, context, "gmail")

async def hotmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reset_handler(update, context, "hotmail")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("g", gmail))
    app.add_handler(CommandHandler("h", hotmail))
    app.run_polling()

if __name__ == "__main__":
    main()
