# pip install Flask gspread mysql-connector-python pandas oauth2client
from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd
import csv, os
from decimal import Decimal
import scopeconnect  # ใช้ gspread + cred.json ในเครื่อง server เท่านั้น

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    start_date = data['start_date']
    filename = 'pedx'

    try:
        connection = mysql.connector.connect(
            host='192.168.10.1',
            port=3306,
            user='chondaen',
            password='chondaen',
            database='hosxp'
        )
        
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
        df = pd.DataFrame(results, columns=['VN', 'HN', 'AN', 'vstdate', 'vsttime', 'ผู้ซักประวัติ', 'รหัสแพทย์'
                                            , 'ชื่อแพทย์', 'pe', 'diag_text', 'cc', 'hpi', 'pdx', 'dx1', 'dx2', 'dx3'])

        # save to CSV
        df.to_csv(f'{filename}.csv', index=False, encoding='utf-8-sig')

        # upload to Google Sheet
        sheet = scopeconnect.client.open_by_key("1nandm3Rf1zE_SY0coz5mqJgZ-2nLGRF4dY_PsvVd6fw").worksheet("data")

        with open(f"{filename}.csv", "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            data = list(reader)

        sheet.clear()
        sheet.append_rows(data)

        os.remove(f"{filename}.csv")
        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # เปิดให้คนในวง LAN ใช้งานได้ด้วย