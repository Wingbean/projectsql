# pip install tabulate python-dotenv
import requests
import mysql.connector
import pandas as pd
from mysql.connector import Error
from decimal import Decimal
from dotenv import load_dotenv
import os

def query_send_telegram():
    try:
        load_dotenv()

        # ตรวจสอบว่า .env ครบหรือไม่
        required_vars = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_DATABASE", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"Environment variable '{var}' is missing.")

        # เชื่อมต่อกับ MySQL
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv('DB_DATABASE')
        )

        if connection.is_connected():
            print("Successfully connected to MySQL server\nRun query")

            query = """
                SELECT
                    o.hn,
                    MAX(c.regdate)
                FROM ovst o
                LEFT OUTER JOIN clinicmember c ON o.hn = c.hn
                WHERE o.vstdate = CURDATE() AND o.main_dep = '033' AND c.regdate IS NULL
                GROUP BY o.hn;
            """

            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            df = pd.DataFrame(results, columns=['HN', 'Regdate'])

            # Convert Decimal -> str
            for col in df.columns:
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, Decimal) else x)

            # Telegram
            TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
            CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

            if df.empty:
                text = "ไม่พบข้อมูลผู้ป่วยที่เข้าเงื่อนไขในวันนี้"
            else:
                intro_text = 'HN ผู้ป่วยยังไม่มีวันลงทะเบียน\n'
                df_text = df.to_markdown(index=False)
                text = intro_text + '\n' + df_text

            url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
            payload = {
                'chat_id': CHAT_ID,
                'text': text,
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, data=payload)
            print(response.status_code, response.text)

    except Error as e:
        print(f"Database Error: {e}")

    except Exception as ex:
        print(f"Unexpected Error: {ex}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    query_send_telegram()
