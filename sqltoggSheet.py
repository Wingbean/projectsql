"""test input"""
import mysql.connector
import pandas as pd
import csv
import gspread
from mysql.connector import Error
from oauth2client.service_account import ServiceAccountCredentials
from decimal import Decimal

def query_and_upload_to_ggsheet():
    try:
        # รับค่า input วันที่เริ่มต้นและสิ้นสุด
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        # รับค่า input ชื่อไฟล์ CSV
        # filename = input("Enter filename to save CSV (e.g., druguse.csv): ")

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
            select
            o.icode as รหัสยา
            ,d.tmt_tp_code as TTMT_code
            ,d.name as Drug
            ,d.strength 
            ,d.units
            ,count(o.icode)as list
            ,sum(o.qty)as quantity_จำนวนสั่ง
            ,d.unitcost as ราคาต่อหน่วย
            ,(sum(o.qty)*d.unitcost)as amount_มูลค่า
            from opitemrece o
            join drugitems d on d.icode=o.icode 
            where o.rxdate between "{start_date}" and "{end_date}" and d.tmt_tp_code IN(798783,717021,532586,940556,264414,9092983,666847,9374895,486941,715038)
            group by o.icode order by d.name,d.strength 
            ;
            """
            
            # รัน query
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # สร้าง DataFrame จากผลลัพธ์
            df = pd.DataFrame(results, columns=['รหัสยา', 'TTMT_code', 'Drug', 'Strength', 'Units', 'list', 'Quan', 'unitcost', 'amount'])

            """
            # แปลงค่า Decimal เป็น float หรือ str
            for col in df.columns:
                if df[col].dtype == 'object': # ตรวจสอบว่าเป็น Object หรือไม่
                    try:
                        df[col] = df[col].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
                    except TypeError:
                        df[col] = df[col].apply(lambda x: str(x) if isinstance(x, Decimal) else x)
            """
            # แปลงค่า Decimal เป็น str เพื่อรักษาความแม่นยำของทศนิยม คุณควรแปลงค่า Decimal เป็น str แทน float 
            # และจัดการการแสดงผลทศนิยมใน Google Sheets แทน
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].apply(lambda x: str(x) if isinstance(x, Decimal) else x)
            """
            # บันทึก DataFrame เป็น CSV
            df.to_csv(f'{filename}.csv', index=False)
            print(f"Results saved to {filename}.csv")
            """
            # ขอบเขตการอนุญาต (scope) สำหรับ Google Sheets API
            scope = ["https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive"]

            # ข้อมูลประจำตัวบัญชีบริการ (Service Account)
            creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\MKDay\OneDrive\MKDay\druguse-d2f5b849851c.json", scope)
            client = gspread.authorize(creds)

            # เปิด Google Sheet ที่มีอยู่แล้ว ระบุชื่อ worksheet
            sheet = client.open_by_key("1Za_EK3uLBdAirqrUHilq-kvBsQyF3nIsCrB1ZAub_pc").worksheet("1_2567")

            sheet.clear()
            sheet.append_rows(df.values.tolist())
            print("Results uploaded to Google Sheets")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    query_and_upload_to_ggsheet()