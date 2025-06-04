import os
import configparser
import requests

# โหลด config
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(config_path)

# === BACKEND CONFIG ===
BACKEND_URL = config['backend']['url']

# กำหนด query (สามารถเก็บไว้ในไฟล์ .sql แล้วอ่านเข้ามาก็ได้)
query = """
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
    ,MAX(os.cc) AS 'CC'
    ,MAX(os.hpi) AS 'Hpi'
    ,MAX(v.pdx) AS 'PDx'
    ,MAX(v.dx1) AS 'Dx1'
    ,MAX(v.dx2) AS 'Dx2'
    ,MAX(v.dx3) AS 'Dx3'
FROM ovst o 
LEFT OUTER JOIN opdscreen os ON o.vn = os.vn
LEFT OUTER JOIN doctor d  ON o.doctor = d.code
LEFT OUTER JOIN screen_doctor sd on sd.vn = o.vn
LEFT OUTER JOIN opduser ou on ou.loginname = sd.staff
LEFT OUTER JOIN vn_stat v on v.vn = o.vn
LEFT OUTER JOIN ovst_doctor_diag od on od.vn = o.vn
WHERE o.vstdate BETWEEN '{start_date}' AND CURDATE()
GROUP BY o.vn
ORDER BY MAX(o.vstdate) DESC, MAX(o.vsttime) DESC, MAX(o.doctor) DESC;
"""

def send_query():
    start_date = input("กรุณากรอกวันที่เริ่มต้น (YYYY-MM-DD): ")

    payload = {
        "start_date": start_date,
        "query": query
    }

    try:
        response = requests.post(BACKEND_URL, json=payload)
        if response.status_code == 200:
            print("✅ อัปโหลดสำเร็จ")
        else:
            print(f"❌ อัปโหลดล้มเหลว: {response.status_code}")
            print("รายละเอียด:", response.text)
    except Exception as e:
        print(f"⚠️ เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")


if __name__ == "__main__":
    send_query()