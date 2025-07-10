# og69x_reset_bot.py

import asyncio, uuid, string, random, requests, os
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)

# 🔐 Bot Config
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_THREAD_ID = 26  # ✅ Only reply in this topic/thread
CHAT_ID = -1002886524212  # Optional, use if needed

# ✅ /start command
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *OG69x Reset*!\n"
        "Send me an Instagram **username** or **email** \n"
        "⚠️ Warning: Only works in @og69y group.",
        parse_mode="Markdown"
    )

# ✅ /ping command
async def ping(update, context):
    await update.message.reply_text("✅ Bot is working!")

# ✅ /id command
async def get_thread_id(update, context):
    thread_id = update.message.message_thread_id
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"📌 Chat ID: `{chat_id}`\n🧵 Thread ID: `{thread_id}`",
        parse_mode="Markdown"
    )

# 🔁 Handle messages
async def handle_message(update, context):
    thread_id = update.message.message_thread_id

    if thread_id is None or thread_id != TARGET_THREAD_ID:
        print("❌ Ignored: Wrong thread or main group")
        return

    print(f"📩 Message received in correct topic: {thread_id}")
    target = update.message.text.strip()

    sent = await update.message.reply_text("🔁 Starting reset process…")
    await asyncio.sleep(1)
    await sent.edit_text("⬇️ Deleting previous session…")
    await asyncio.sleep(1)
    await sent.edit_text("📡 Sending request to Instagram…")
    await asyncio.sleep(1)

    result = send_password_reset(target)
    final_text = f"{result}\n\n🔚 Powered by [@og69x](https://t.me/og69x)"
    await sent.edit_text(final_text, parse_mode="Markdown", disable_web_page_preview=True)

# 🔐 Reset function
def send_password_reset(target: str) -> str:
    target = target.strip()
    if target.startswith("@"):
        return "❌ Send username without '@'."

    data = {
        "_csrftoken": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
        "guid": str(uuid.uuid4()),
        "device_id": str(uuid.uuid4())
    }
    data["user_email" if "@" in target else "username"] = target

    headers = {
        "user-agent": (
            "Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; "
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))})"
        )
    }

    try:
        res = requests.post(
            "https://i.instagram.com/api/v1/accounts/send_password_reset/",
            headers=headers, data=data, timeout=15
        )
    except Exception as e:
        return f"⚠️ Network error: {e}"

    if res.ok and "obfuscated_email" in res.text:
        return "✅ Password reset link sent!"
    return f"❌ Failed: {res.text}"

# ❗ Error handler
async def error_handler(update, context):
    print(f"❌ Exception: {context.error}")

# 🚀 Start the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("id", get_thread_id))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error_handler)

    print("🤖 OG69x Bot running…")
    app.run_polling()

if __name__ == "__main__":
    main()
