# pip install mysql-connector-python pandas

# ==============
# รัน query --> create df --> save to csv
# ==============

import mysql.connector
import pandas as pd
from mysql.connector import Error

def query_and_save_to_csv():
    try:
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

            query = """
            SELECT vn, main_dep, vstdate
            FROM ovst
            WHERE vstdate = '2024-10-10' AND main_dep = '033'
            """
            
            # รัน query
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # สร้าง DataFrame จากผลลัพธ์
            df = pd.DataFrame(results, columns=['vn', 'main_dep', 'vstdate'])

            # บันทึก DataFrame เป็น CSV
            df.to_csv('result.csv', index=False, encoding='utf-8-sig')
            print("Results saved to result.csv")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    query_and_save_to_csv()
