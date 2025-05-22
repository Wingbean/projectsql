from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd
import csv, os
import scopeconnect  # ใช้ gspread + cred.json ใน backend เท่านั้น

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    start_date = data.get('start_date')
    query_template = data.get('query')

    if not start_date or not query_template:
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

    query = query_template.replace("{start_date}", start_date)

    filename = 'query_results.csv'

    try:
        connection = mysql.connector.connect(
            host='192.168.10.1',
            port=3306,
            user='chondaen',
            password='chondaen',
            database='hosxp'
        )

        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        df = pd.DataFrame(results)  # ไม่มีหัวคอลัมน์
        df.to_csv(filename, index=False, header=False, encoding='utf-8-sig')

        sheet = scopeconnect.client.open_by_key("1nandm3Rf1zE_SY0coz5mqJgZ-2nLGRF4dY_PsvVd6fw").worksheet("data")
        
        # เคลียร์ข้อมูลยกเว้นหัวตาราง
        data_rows = sheet.get_all_values()
        if len(data_rows) > 1:
            sheet.batch_clear([f"A2:Z{len(data_rows)}"])  # ลบจาก row 2 ลงไป

        with open(filename, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            data = list(reader)

        sheet.append_rows(data, value_input_option="USER_ENTERED")

        os.remove(filename)
        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
