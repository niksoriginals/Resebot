# Original variables and functions (UNCHANGED)
E='STATUS~1'
W='XMLHttpRequest'
V='936619743392459'
U='same-origin'
T='cors'
S='empty'
R='*/*'
Q='x-requested-with'
P='x-ig-www-claim'
O='x-ig-app-id'
N='sec-fetch-site'
M='sec-fetch-mode'
L='sec-fetch-dest'
K='referer'
J='accept-language'
I='accept'
H='email_or_username'
F='csrftoken'
G='User-Agent'
A=print

import os
import asyncio
import requests as C, re, json
from uuid import uuid4
from telegram.ext import Application, CommandHandler, MessageHandler, filters

def X(email_or_username):
    A='https://www.instagram.com/accounts/account_recovery_send_ajax/'
    B={G:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36','Referer':'https://www.instagram.com/accounts/password/reset/','X-CSRFToken':F}
    D={H:email_or_username,'recaptcha_challenge_field':''}
    E=C.post(A,headers=B,data=D)
    return E

def Y(response_text):
    A=re.search('<b>(.*?)</b>',response_text)
    if A:return A.group(1)
    else:return'Unknown'

def Z(username):
    H='gzip'
    F='STATUS~2'
    B=username
    try:B=B.split('@gmail.com')[0]
    except:pass
    D=f"https://www.instagram.com/api/v1/users/web_profile_info/?username={B}"
    E={I:R,'accept-encoding':H,J:'en-US;q=0.9,en;q=0.7',K:f"https://www.instagram.com/{B}",L:S,M:T,N:U,O:V,P:'0',Q:W}
    X=C.get(D,headers=E).json()
    try:Y=X['data']['user']['id']
    except:
        return F, f"-FAILED TO SEND THE PASSWORD RESET TO @{B}"
    D='https://i.instagram.com/api/v1/accounts/send_password_reset/'
    E={G:'Instagram 6.12.1 Android (30/11; 480dpi; 1080x2004; HONOR; ANY-LX2; HNANY-Q1; qcom; ar_EG_#u-nu-arab)','Cookie':'mid=YwsgcAABAAGsRwCKCbYCaUO5xej3; csrftoken=u6c8M4zaneeZBfR5scLVY43lYSIoUhxL','Cookie2':'$Version=1','Accept-Language':'ar-EG, en-US','X-IG-Connection-Type':'MOBILE(LTE)','X-IG-Capabilities':'AQ==','Accept-Encoding':H}
    Z={'user_id':Y,'device_id':str(uuid4())}
    a=C.post(D,headers=E,data=Z).json()
    try:
        b=a['obfuscated_email']
        return F, f"-PASSWORD RESET LINK SENT TO @{B} AT {b}"
    except:
        return F, f"-FAILED TO SEND THE PASSWORD RESET TO @{B}"

def a(username_or_email):
    X='status'
    G='umwHlWf6r3AGDowkZQb47m'
    E='STATUS~3'
    D='message'
    Y='https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/'
    Z={F:G,'datr':'_D1dZ0DhNw8dpOJHN-59ONZI','ig_did':'C0CBB4B6-FF17-4C4A-BB83-F3879B996720','mid':'Z109_AALAAGxFePISIe2H_ZcGwTD','wd':'1157x959'}
    a={I:R,J:'en-US,en;q=0.5','content-type':'application/x-www-form-urlencoded','origin':'https://www.instagram.com','priority':'u=1, i',K:'https://www.instagram.com/accounts/password/reset/?source=fxcal&hl=en','sec-ch-ua':'"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-full-version-list':'"Brave";v="131.0.0.0", "Chromium";v="131.0.0.0", "Not_A Brand";v="24.0.0.0"','sec-ch-ua-mobile':'?0','sec-ch-ua-model':'""','sec-ch-ua-platform':'"Windows"','sec-ch-ua-platform-version':'"10.0.0"',L:S,M:T,N:U,'sec-gpc':'1','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36','x-asbd-id':'129477','x-csrftoken':G,O:V,P:'0','x-instagram-ajax':'1018880011',Q:W,'x-web-session-id':'ag36cv:1ko17s:9bxl9b'}
    b={H:username_or_email,'flow':'fxcal'}
    c=C.post(Y,cookies=Z,headers=a,data=b)
    try:
        B=c.json()
        if B.get(X)=='fail':
            if B.get('error_type')=='rate_limit_error':
                return 'TRY USING VPN. IP LIMITED.'
            elif D in B and isinstance(B[D],list):
                return f'{E}\nCheck the username or email again.'
            else:
                return f'{E}\nError: {B.get(D,"Unknown error")}'
        elif B.get(X)=='ok':
            return f'{E}\nMessage: {B.get(D,"No message provided")}'
        else:
            return f'{E}\nUnexpected response: {B}'
    except json.JSONDecodeError:
        return 'Failed to parse the response as JSON.'
    except Exception as d:
        return f'Unexpected error: {str(d)}'

# TELEGRAM BOT LOGIC

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))
ALLOWED_THREAD_ID = int(os.getenv("THREAD_ID"))

async def start(update, context):
    await update.message.reply_text("Send me an Instagram username or email to attempt a password reset.\nOr use /reset <username_or_email>.\nType /exit to end.")

async def handle_input(update, context):
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return
    if update.message.message_thread_id != ALLOWED_THREAD_ID:
        return

    B = update.message.text.strip()
    if B.lower() == 'exit':
        await context.bot.send_message(chat_id=ALLOWED_CHAT_ID, message_thread_id=ALLOWED_THREAD_ID, text="Exiting session.")
        return

    # ✅ Try STATUS~1
    D = X(B)
    if D.status_code == 200:
        b = Y(D.text)
        await context.bot.send_message(chat_id=ALLOWED_CHAT_ID, message_thread_id=ALLOWED_THREAD_ID, text=f"Form Handler\n-PASSWORD RESET LINK SENT TO @{B}")
        return

    # ✅ Try STATUS~2
    status2, msg2 = Z(B)
    if "PASSWORD RESET LINK SENT" in msg2:
        await context.bot.send_message(chat_id=ALLOWED_CHAT_ID, message_thread_id=ALLOWED_THREAD_ID, text=f"{status2}\n{msg2}")
        return

    # ✅ Try STATUS~3
    msg3 = a(B)
    if "PASSWORD RESET" in msg3 or "Message:" in msg3:
        await context.bot.send_message(chat_id=ALLOWED_CHAT_ID, message_thread_id=ALLOWED_THREAD_ID, text=msg3)

async def reset_command(update, context):
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return
    if update.message.message_thread_id != ALLOWED_THREAD_ID:
        return

    args = context.args
    if not args:
        await update.message.reply_text("Usage: /reset <username_or_email>")
        return

    B = args[0].strip()

    # ✅ Try STATUS~1
    D = X(B)

    if D.status_code == 200:
        b = Y(D.text)
        await context.bot.send_message(chat_id=ALLOWED_CHAT_ID, message_thread_id=ALLOWED_THREAD_ID, text=f"STATUS~1\n-PASSWORD RESET LINK SENT TO @{B} TO {b}")
        return

    # ✅ Try STATUS~2
    status2, msg2 = Z(B)
    if "PASSWORD RESET LINK SENT" in msg2:
        await context.bot.send_message(chat_id=ALLOWED_CHAT_ID, message_thread_id=ALLOWED_THREAD_ID, text=f"{status2}\n{msg2}")
        return

    # ✅ Try STATUS~3
    msg3 = a(B)
    if "PASSWORD RESET" in msg3 or "Message:" in msg3:
        await context.bot.send_message(chat_id=ALLOWED_CHAT_ID, message_thread_id=ALLOWED_THREAD_ID, text=msg3)
    else:
        await context.bot.send_message(chat_id=ALLOWED_CHAT_ID, message_thread_id=ALLOWED_THREAD_ID, text="All methods failed or unexpected error.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    application.run_polling()

if __name__ == '__main__':
    main()
