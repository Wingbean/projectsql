import mysql.connector
import pandas as pd
import csv
import gspread
from mysql.connector import Error
from oauth2client.service_account import ServiceAccountCredentials
from decimal import Decimal
import os  # Import the os module

def csv_to_ggsheet():
    try:
        
        # รับค่า input วันที่เริ่มต้นและสิ้นสุด
        start_date = input("Enter start date (YYYY-MM-DD): ")

        """
        end_date = input("Enter end date (YYYY-MM-DD): ")
        """

        #รับค่าชื่อ worksheet
        # wksname = input("ใส่ชื่อแผ่นงานใน ggSheet ที่ต้องการ upload: ")
        
        # รับค่า input ชื่อไฟล์ CSV
        
        filename = 'pedx'
        
        #input("Enter filename to save CSV (e.g., druguse.csv): ")
        
        # เชื่อมต่อกับ MySQL
        connection = mysql.connector.connect(
            host='192.168.10.1',
            port=3306,
            user='chondaen',  # เปลี่ยนเป็น username ของคุณ
            password='chondaen',  # เปลี่ยนเป็น password ของคุณ
            database='hosxp'  # ถ้าคุณต้องการเชื่อมต่อกับ database เฉพาะ
        )

        if connection.is_connected():
            print("Successfully connected to MySQL server")

            query = f"""
            SELECT
            o.vn AS 'VN'
            ,MAX(o.hn) AS 'HN' 
            ,MAX(o.an) AS 'AN' 
            ,MAX(o.vstdate) AS 'VstDate'
            ,MAX(o.vsttime) AS 'VstTime'
            ,MAX(ou.name) AS 'ผู้ซักประวัติ'
            ,MAX(o.doctor) AS 'รหัสแพทย์'
            ,MAX(d.name) AS 'ชื่อแพทย์'
            ,MAX(os.pe) AS 'PE'
            ,MAX(od.diag_text) AS 'Dx_Text'
            ,MAX(os.cc) AS 'CC' ,MAX(os.hpi) AS 'Hpi' ,MAX(v.pdx) AS 'PDx',MAX(v.dx1) AS 'Dx1',MAX(v.dx2) AS 'Dx2',MAX(v.dx3) AS 'Dx3'
            FROM ovst o 
            LEFT OUTER JOIN opdscreen os ON o.vn = os.vn
            LEFT OUTER JOIN doctor d  ON o.doctor = d.code
            LEFT OUTER JOIN screen_doctor sd on sd.vn = o.vn
            LEFT OUTER JOIN opduser ou on ou.loginname = sd.staff
            LEFT OUTER JOIN vn_stat v on v.vn = o.vn
            LEFT OUTER JOIN ovst_doctor_diag od on od.vn = o.vn
            WHERE o.vstdate BETWEEN '{start_date}' AND CURDATE() -- o.doctor in ('247', '0086', '0087', '0088', '0089', '0090', '0052', '004', '123')
            GROUP BY o.vn
            ORDER BY MAX(o.vstdate) DESC, MAX(o.vsttime) DESC, MAX(o.doctor) DESC
;
            """
            
            # รัน query
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # สร้าง DataFrame จากผลลัพธ์
            df = pd.DataFrame(results, columns=['VN', 'HN', 'AN', 'vstdate', 'vsttime', 'ผู้ซักประวัติ', 'รหัสแพทย์', 'ชื่อแพทย์', 'pe', 'diag_text', 'cc', 'hpi', 'pdx', 'dx1', 'dx2', 'dx3'])

            # บันทึก DataFrame เป็น CSV
            df.to_csv(f'{filename}.csv', index=False)
            print(f"Results saved to {filename}.csv")
            
            # ขอบเขตการอนุญาต (scope) สำหรับ Google Sheets API
            scope = ["https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive"]

            # ข้อมูลประจำตัวบัญชีบริการ (Service Account)
            creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\MKDay\OneDrive\MKDay\druguse-d2f5b849851c.json", scope)
            client = gspread.authorize(creds)

            # เปิด Google Sheet ที่มีอยู่แล้ว ระบุชื่อ worksheet
            sheet = client.open_by_key("1nandm3Rf1zE_SY0coz5mqJgZ-2nLGRF4dY_PsvVd6fw").worksheet(f"data")

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

            print("Results uploaded to Google Sheets")

            


    except Error as e:
        print(f"Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        
        # ลบไฟล์ CSV หากมีการสร้าง
        if 'filename' in locals() and os.path.exists(f'{filename}.csv'):
            os.remove(f'{filename}.csv')
            print(f"File {filename}.csv has been deleted.")


if __name__ == "__main__":
    csv_to_ggsheet()