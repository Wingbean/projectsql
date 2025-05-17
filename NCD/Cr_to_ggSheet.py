# correct date time toJson before upload
# pip install mysql-connector-python pandas gspread oauth2client  # หรือ google-auth แทน oauth2client

# ==============
# รัน query --> create df --> change dtatype to str --> upload to ggSheet
# ไม่มี save to csv ก่อน แล้ว upload csv to ggSheet
# ==============

import mysql.connector
import pandas as pd
import csv
import gspread
from mysql.connector import Error
from oauth2client.service_account import ServiceAccountCredentials
from decimal import Decimal
import datetime
from datetime import date

def query_and_upload_to_ggsheet():
    try:
        # เชื่อมต่อกับ MySQL
        connection = mysql.connector.connect(
            host='192.168.10.1',
            port=3306,
            user='chondaen',  # เปลี่ยนเป็น username ของคุณ
            password='chondaen',  # เปลี่ยนเป็น password ของคุณ
            database='hosxp'  # ถ้าคุณต้องการเชื่อมต่อกับ database เฉพาะ
        )

        # วาง qurey
        if connection.is_connected():
            print("Successfully connected to MySQL server")

            query = f"""
            SELECT
                lh.lab_order_number AS order_nunber,
                lh.vn AS vn,
                lh.hn AS hn,
                concat(p.pname, p.fname, " ", p.lname) AS ptname,
                lh.order_date AS order_date,
                lh.order_time AS order_time,
                lo.lab_items_code AS item_code,
                lo.lab_order_result AS Cr
            FROM
                lab_head lh
            LEFT OUTER JOIN
                lab_order lo ON lh.lab_order_number = lo.lab_order_number
            LEFT OUTER JOIN
                patient p ON p.hn = lh.hn
            WHERE
                lh.order_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 90 DAY) AND CURDATE()
                AND lo.lab_items_code = 883
            ORDER BY lh.hn , lh.order_date DESC, lh.order_time DESC
            ;
            """
            
            # รัน query
            cursor = connection.cursor()
            cursor.execute(query) # สั่งให้รัน query
            results = cursor.fetchall()

            # สร้าง DataFrame จากผลลัพธ์
            df = pd.DataFrame(results, columns=['order_no', 'VN', 'HN', 'ptName', 'orderdate', 'ordertime', 'itemCode', 'eGFR'])
            print(df.dtypes)
            
            # แปลงค่า Decimal เป็น str (ถ้ามี)
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].apply(lambda x: str(x) if isinstance(x, Decimal) else x)

            # แปลงคอลัมน์ orderdate เป็น str
            df['orderdate'] = df['orderdate'].astype(str)

            # แปลงคอลัมน์ ordertime เป็น str
            df['ordertime'] = df['ordertime'].astype(str)


            # เพิ่มชื่อคอลัมน์ (หัวตาราง) เข้าไปใน list ของ lists
            data_to_upload = [df.columns.tolist()] + df.values.tolist()

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
            sheet = client.open_by_key("1HqLTFYFXyPtRyNBPAItVbwq19EwdFqIKS24K9YDomJ0").worksheet("cr")

            # เพิ่มข้อมูลเข้าไปใน ggSheet
            sheet.clear()
            sheet.append_rows(data_to_upload)
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

