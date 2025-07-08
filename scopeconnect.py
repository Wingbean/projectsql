import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os, sys

# ขอบเขตการอนุญาต (scope) สำหรับ Google Sheets API
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# ตรวจสอบว่าเป็น .exe หรือ .py
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # ที่อยู่ไฟล์เมื่อรันจาก .exe
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # ตอนรันจาก .py

# รวม path ของ json
json_path = os.path.join(base_path, "druguse-d2f5b849851c.json")

# โหลด credentials
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)