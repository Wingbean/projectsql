# pip install requests configparser tkinter
import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import configparser
import os

# โหลด config
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(config_path)
BACKEND_URL = config['backend']['url']

# ฟังก์ชันเมื่อคลิกปุ่ม
def submit_data():
    start_date = entry_date.get()
    query = text_query.get("1.0", tk.END).strip()

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

tk.Label(root, text="SQL Query:").pack(pady=10)
text_query = scrolledtext.ScrolledText(root, width=70, height=10)
text_query.pack()

tk.Button(root, text="ส่งข้อมูล", command=submit_data).pack(pady=20)

root.mainloop()
