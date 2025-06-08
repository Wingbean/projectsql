import requests
from dotenv import load_dotenv
import os
import pandas as pd
from tabulate import tabulate
import json
from datetime import datetime


# โหลด .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ขอข้อมูลจาก Telegram
response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates')
data = response.json()

# แสดง JSON แบบอ่านง่าย
print("\n📦 JSON ตอบกลับจาก Telegram (แบบอ่านง่าย):")
print(json.dumps(data, indent=4, ensure_ascii=False))

# ตรวจสอบว่า ok หรือไม่
if not data.get("ok"):
    print("❌ Error: Failed to get updates")
    exit()

# เตรียมข้อมูลเก็บ
rows = []

for item in data['result']:
    chat = None
    text = ""
    username = ""
    timestamp = None
    readable_date = ""

    # หากมีข้อความ
    if 'message' in item:
        chat = item['message']['chat']
        text = item['message'].get('text', '')
        username = item['message'].get('from', {}).get('username', '')
        timestamp = item['message'].get('date')
    elif 'my_chat_member' in item:
        chat = item['my_chat_member']['chat']
        username = item['my_chat_member'].get('from', {}).get('username', '')
        timestamp = item['my_chat_member'].get('date')

    if timestamp:
        readable_date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    if chat:
        rows.append({
            "chat_id": chat.get("id"),
            "chat_type": chat.get("type"),
            "title": chat.get("title", ""),
            "username": username,
            "text": text,
            "date": readable_date
        })


# แสดงผลลัพธ์
if rows:
    df = pd.DataFrame(rows)
    print("\n📊 ตารางข้อมูล Telegram Updates:")
    print(tabulate(df, headers="keys", tablefmt="grid", showindex=True))
else:
    print("ℹ️ No chat updates found.")

# แสดง df
print("\n✅ View df:")
print(df)
