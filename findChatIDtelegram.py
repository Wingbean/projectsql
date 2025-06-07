import requests
from dotenv import load_dotenv
import os
import pandas as pd
from tabulate import tabulate
import json

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates')
#print(response.json())

data = response.json()

# ตรวจสอบว่าการตอบกลับสำเร็จหรือไม่
if not data.get("ok"):
    print("Error: Failed to get updates")
    exit()

# เตรียมข้อมูลให้อ่านง่าย
rows = []
for item in data['result']:
    chat = None
    if 'message' in item:
        chat = item['message']['chat']
    elif 'my_chat_member' in item:
        chat = item['my_chat_member']['chat']
    
    if chat:
        rows.append({
            "chat_id": chat.get("id"),
            "chat_type": chat.get("type"),
            "title": chat.get("title", ""),
            "username": chat.get("username", "")
        })

# แสดงตารางแบบอ่านง่าย
if rows:
    print(tabulate(rows, headers="keys", tablefmt="grid"))
else:
    print("No chat updates found.")
