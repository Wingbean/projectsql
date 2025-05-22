# pip install Flask mysql-connector-python pandas

from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Flask backend ทำงานได้ปกติ!"})

@app.route('/generate', methods=['POST'])
def generate_csv():
    data = request.json
    start_date = data['start_date']
    end_date = data['end_date']
    filename = data['filename']

    # เชื่อมต่อ MySQL และดึงข้อมูล
    connection = mysql.connector.connect(
        host='localhost',  # หรือ 127.0.0.1
        user='youruser',
        password='yourpass',
        database='hosxp'
    )
    query = f"""
    SELECT * FROM some_table
    WHERE rxdate BETWEEN '{start_date}' AND '{end_date}'
    """
    df = pd.read_sql(query, connection)
    df.to_csv(filename, index=False)

    return jsonify({"status": "success", "message": f"{filename} saved"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # เปิดให้คนในวง LAN ใช้งานได้ด้วย
