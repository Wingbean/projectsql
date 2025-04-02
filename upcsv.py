import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ขอบเขตการอนุญาต (scope) สำหรับ Google Sheets API
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# ข้อมูลประจำตัวบัญชีบริการ (Service Account)
creds = ServiceAccountCredentials.from_json_keyfile_name("your_credentials.json", scope)
client = gspread.authorize(creds)

# เปิด Google Sheet โดยใช้ชื่อหรือ ID
sheet = client.open("Your Sheet Name").sheet1  # หรือใช้ sheet = client.open_by_key("sheet_id").sheet1

# อ่านข้อมูลจากไฟล์ CSV
data = []
with open("your_file.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

# อัปเดตข้อมูลไปยัง Google Sheet
sheet.clear()  # ล้างข้อมูลที่มีอยู่ (ถ้าต้องการ)
sheet.append_rows(data)  # เพิ่มข้อมูลใหม่