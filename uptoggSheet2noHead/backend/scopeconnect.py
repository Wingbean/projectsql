import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os, sys

# ขอบเขตการอนุญาต (scope) สำหรับ Google Sheets API
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# ข้อมูลประจำตัวบัญชีบริการ (Service Account)
creds = ServiceAccountCredentials.from_json_keyfile_name("druguse-d2f5b849851c.json", scope)
client = gspread.authorize(creds)