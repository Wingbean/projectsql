# pip install gspread oauth2client  # หรือ google-auth แทน oauth2client
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ==============
# มีไฟล์ csv --> read csv to list โดยระบุการเข้ารหัส --> upload list to ggSheet
# แบบนี้มีหัว column จาก CSV ไปด้วย
# ==============


# รับค่า input ชื่อไฟล์ CSV
filename = input("Enter filename to save CSV (e.g., druguse.csv): ")

# ขอบเขตการอนุญาต (scope) สำหรับ Google Sheets API
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# ข้อมูลประจำตัวบัญชีบริการ (Service Account)
creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\MKDay\OneDrive\MKDay\druguse-d2f5b849851c.json", scope)
client = gspread.authorize(creds)
"""
# เปิด Google Sheet โดยใช้ชื่อหรือ ID
sheet = client.open_by_key("1Za_EK3uLBdAirqrUHilq-kvBsQyF3nIsCrB1ZAub_pc").sheet1
"""
# เปิด Google Sheet ที่มีอยู่แล้ว ระบุชื่อ worksheet
sheet = client.open_by_key("1Za_EK3uLBdAirqrUHilq-kvBsQyF3nIsCrB1ZAub_pc").worksheet("1_2567")

# อ่านข้อมูลจากไฟล์ CSV โดยระบุการเข้ารหัส
data = []
try:
    with open(f"{filename}.csv", "r", encoding="utf-8") as f:  # ลองใช้ utf-8 ก่อน
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

except UnicodeDecodeError:
    try:
        with open(f"{filename}.csv", "r", encoding="windows-1252") as f: # ถ้า utf-8 ไม่ได้ผล ลอง windows-1252
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
    except UnicodeDecodeError:
        print("ไม่สามารถถอดรหัสไฟล์ CSV ได้")
        exit()
        
# อัปเดตข้อมูลไปยัง Google Sheet
sheet.clear()  # ล้างข้อมูลที่มีอยู่ (ถ้าต้องการ)
sheet.append_rows(data)  # เพิ่มข้อมูลใหม่
