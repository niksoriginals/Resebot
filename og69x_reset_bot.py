import os
import uuid
import string
import random
import requests
import telebot

# === CONFIGURATION ===
BOT_TOKEN = '8165119036:AAF6dkvvJSzF1A-zSrj5dpPnvekEeep1unw'
GROUP_CHAT_ID = -1002886524212   # Replace with your group ID
THREAD_ID = 21898            # Replace with the thread/topic ID

bot = telebot.TeleBot(BOT_TOKEN)

# === IG Reset Request Function ===
def send_reset_request(target):
    headers = {
     "user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)"
        }
 

    data = {
      "_csrftoken": "".join(random.choices(string.ascii_lowercase +
                                                          string.ascii_uppercase + string.digits, k=32)),
                    "_csrftoken": "".join(random.choices(string.ascii_lowercase +
                                                          string.ascii_uppercase + string.digits, k=32)),
                    "username": target,
                    "guid": uuid.uuid4(),
                    "device_id": uuid.uuid4()
    }

    if "@" in target:
        data["user_email"] = target
    else:
        data["username"] = target

    try:
        response = requests.post(
            "https://i.instagram.com/api/v1/accounts/send_password_reset/",
            headers=headers,
            data=data
        )
        json_data = response.json()

        if "obfuscated_email" in json_data:
            return f"✅ *Reset Sent!*\n🔒 `Email`: `{json_data['obfuscated_email']}`"
        elif "message" in json_data:
            return f"❌ *Failed*: {json_data['message']}"
        else:
            return f"⚠️ *Unexpected response*\n```{response.text}```"
    except Exception as e:
        return f"❌ *Error*: {str(e)}"

# === LISTEN ONLY FOR /reset COMMAND IN THREAD ===
@bot.message_handler(commands=['reset'])
def handle_reset_command(message):
    if message.chat.id != GROUP_CHAT_ID or message.message_thread_id != THREAD_ID:
        return  # Ignore messages outside the target thread

    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: `/reset username_or_email`", parse_mode="Markdown")
        return

    target = parts[1].strip()
    response_text = send_reset_request(target)
    bot.reply_to(message, response_text, parse_mode="Markdown")

# === START BOT ===
print("🤖 Bot is running...")
bot.infinity_polling()
