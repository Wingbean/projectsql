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
            where o.rxdate between "2023-10-01" and "2023-12-31" and d.tmt_tp_code IN(798783,717021,532586,940556,264414,9092983,666847,9374895,486941,715038)
            group by o.icode order by d.name,d.strength 
            ;
            """
            
            # รัน query
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # สร้าง DataFrame จากผลลัพธ์
            df = pd.DataFrame(results, columns=['รหัสยา', 'TTMT_code', 'Drug', 'Strength', 'Units', 'list', 'Quan', 'unitcost', 'amount'])

            # บันทึก DataFrame เป็น CSV
            df.to_csv('druguse.csv', index=False)
            print("Results saved to druguse.csv")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    query_and_save_to_csv()