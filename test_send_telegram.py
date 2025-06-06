# pip install tabulate
import requests
import mysql.connector
import pandas as pd
from mysql.connector import Error
from decimal import Decimal

# Pull SQL

def query_send_telegram():
    try:
        
        # เชื่อมต่อกับ MySQL
        connection = mysql.connector.connect(
            host='192.168.10.1',
            port=3306,
            user='chondaen',
            password='chondaen',
            database='hosxp'
        )

        if connection.is_connected():
            print("Successfully connected to MySQL server\nRun query")

            query = f"""
                select
                o.hn
                ,MAX(c.regdate)
                FROM ovst o
                LEFT OUTER JOIN clinicmember c ON o.hn = c.hn
                WHERE o.vstdate = CURDATE() AND o.main_dep = '033' AND c.regdate IS NULL
                GROUP BY o.hn
                ;
            """
            
            # รัน query
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # สร้าง DataFrame จากผลลัพธ์
            df = pd.DataFrame(results, columns=['HN', 'Regdate'])

            print(df)

            # COnfig telegram

            TELEGRAM_BOT_TOKEN = 
            CHAT_ID = '-1002594018313'

            # check chat id
            #response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates')
            #print(response.json())

            intro_text = 'HN ผู้ป่วยยังไม่มีวันลงทะเบียน\n'
            df_text = df.to_markdown(index=False)
            text = intro_text + '\n' + df_text
            
            # ====== ส่งเป็นข้อความ (วิธีที่ 1) ======
            url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
            payload = {
                'chat_id': CHAT_ID,
                'text': text,
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, data=payload)
            print(response.status_code, response.text)    


    except Error as e:
        print(f"Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    query_send_telegram()
