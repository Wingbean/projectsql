#======BACKend ของ ThMedUse=========#
#==Flask รับ request จาก FrontEnd วน loop แล้ว ส่งไฟล์ ที่ save กลับไป folder ที่ frontend เลือกไว้

# pip install Flask mysql-connector-python pandas

from flask import Flask, request, jsonify, send_file
import mysql.connector
import pandas as pd
from mysql.connector import Error
from io import BytesIO

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Flask backend ทำงานได้ปกติ!"})

@app.route('/generate', methods=['POST'])
def generate_csv():
    data = request.json
    start_date = data['start_date']
    end_date = data['end_date']
    filename = data['worksheet']

    try:

        # เชื่อมต่อ MySQL และดึงข้อมูล
        connection = mysql.connector.connect(
            host='192.168.10.1',  # หรือ 127.0.0.1
            user='chondaen',
            password='chondaen',
            database='hosxp'
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
            # บันทึก DataFrame เป็น CSV
            df.to_csv(f"{filename}.csv", index=False)
            
            print("Results saved to result.csv")

            return send_file(f"{filename}.csv", as_attachment=True)
            """
            # บันทึกเป็นไฟล์ CSV ใน memory
            output = BytesIO()
            df.to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)

            # บรรทัดนี้สำคัญ คือการสั่งให้ ส่งไฟล์ที่ save กลับไป
            return send_file(output, mimetype='text/csv', as_attachment=True, download_name=f"{filename}.csv")

    
    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # เปิดให้คนในวง LAN ใช้งานได้ด้วย
