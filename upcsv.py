import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ขอบเขตการอนุญาต (scope) สำหรับ Google Sheets API
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# ข้อมูลประจำตัวบัญชีบริการ (Service Account)
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\MKDay\OneDrive\MKDay\druguse-ca69ae202a22.json", scope)
client = gspread.authorize(creds)

# เปิด Google Sheet โดยใช้ชื่อหรือ ID
sheet = client.open_by_key("1Za_EK3uLBdAirqrUHilq-kvBsQyF3nIsCrB1ZAub_pc").sheet1

# อ่านข้อมูลจากไฟล์ CSV
data = []
with open("druguse.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

# อัปเดตข้อมูลไปยัง Google Sheet
sheet.clear()  # ล้างข้อมูลที่มีอยู่ (ถ้าต้องการ)
sheet.append_rows(data)  # เพิ่มข้อมูลใหม่