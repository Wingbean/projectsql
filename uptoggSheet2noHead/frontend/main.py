# pip install requests configparser tkinter
import tkinter as tk
from tkinter import messagebox, scrolledtext, StringVar
import requests
import configparser
import os

# โหลด config
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(config_path)
BACKEND_URL = config['backend']['url']

# กำหนด SQL queries ที่ต้องการให้เลือก
SQL_QUERIES = {"Query A: pedxText": """
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
                WHERE o.vstdate BETWEEN '{start_date}' AND CURDATE()
                GROUP BY o.vn
                ORDER BY MAX(o.vstdate) DESC, MAX(o.vsttime) DESC, MAX(o.doctor) DESC;
"""
}

# ฟังก์ชันเมื่อคลิกปุ่ม
def submit_data():
    start_date = entry_date.get()
    # ดึงค่า query ที่ถูกเลือกจาก Radio Button
    selected_query_key = query_var.get()
    query = SQL_QUERIES.get(selected_query_key, "") # ดึง SQL string จาก dictionary
    # query = text_query.get("1.0", tk.END).strip()

    if not start_date or not query:
        messagebox.showwarning("แจ้งเตือน", "กรุณากรอกวันที่และคำสั่ง SQL")
        return

    try:
        response = requests.post(
            f"{BACKEND_URL}/upload",
            json={"start_date": start_date, "query": query}
        )
        if response.status_code == 200:
            messagebox.showinfo("สำเร็จ", "✅ อัปโหลดข้อมูลสำเร็จ")
        else:
            messagebox.showerror("ผิดพลาด", f"❌ เกิดข้อผิดพลาด: {response.json()}")
    except Exception as e:
        messagebox.showerror("ผิดพลาด", f"❌ ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์\n{e}")

# GUI Layout
root = tk.Tk()
root.title("Upload to Google Sheets")
root.geometry("700x500")
root.option_add("*Font", "Tahoma 14")

tk.Label(root, text="วันที่เริ่มต้น (YYYY-MM-DD):").pack(pady=10)
entry_date = tk.Entry(root, width=30)
entry_date.pack()

#tk.Label(root, text="SQL Query:").pack(pady=10)
#text_query = scrolledtext.ScrolledText(root, width=70, height=10)
#text_query.pack()

# ตัวแปรสำหรับเก็บค่าที่ถูกเลือกจาก Radio Button
query_var = tk.StringVar(value=list(SQL_QUERIES.keys())[0]) # ตั้งค่าเริ่มต้นให้เลือก Query แรกสุด

# สร้าง Frame สำหรับเก็บ Radio Button เพื่อจัดระเบียบ
radio_frame = tk.Frame(root)
radio_frame.pack(pady=5)

# สร้าง Radio Button สำหรับแต่ละ query ใน dictionary
for query_name in SQL_QUERIES:
    tk.Radiobutton(
        radio_frame,
        text=query_name,
        variable=query_var,
        value=query_name
    ).pack(anchor="w") # จัดเรียงชิดซ้ายภายใน Frame

# --- สิ้นสุดส่วนของ Radio Button ---

tk.Button(root, text="ส่งข้อมูล", command=submit_data).pack(pady=20)

root.mainloop()
