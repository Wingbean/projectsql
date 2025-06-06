#======frontend ของ ThMedUse=========#
#=เป็น GUI กด แล้ว จะดึง data ผ่าน SQL ใน backend แล้ว save เป็น file csv=#
#=ไม่มีการอัปโหลดขึ้น cloud ไหน=#

import tkinter as tk
import requests
from tkinter import messagebox, filedialog

def run_script():
    # กำหนดช่วงเวลาแบบลูปเหมือนโค้ดเดิม
    rounds = [
        {"start_date": "2023-10-01", "end_date": "2023-12-31", "wksname": "1_2567"},
        {"start_date": "2024-01-01", "end_date": "2024-03-31", "wksname": "2_2567"},
        {"start_date": "2024-04-01", "end_date": "2024-06-30", "wksname": "3_2567"},
        {"start_date": "2024-07-01", "end_date": "2024-09-30", "wksname": "4_2567"},
        {"start_date": "2024-10-01", "end_date": "2024-12-31", "wksname": "1_2568"},
        {"start_date": "2025-01-01", "end_date": "2025-03-31", "wksname": "2_2568"},
        {"start_date": "2025-04-01", "end_date": "2025-06-30", "wksname": "3_2568"},
        {"start_date": "2025-07-01", "end_date": "2025-09-30", "wksname": "4_2568"},
    ]

    save_path = filedialog.askdirectory(title="เลือกโฟลเดอร์บันทึกไฟล์ CSV")
    if not save_path:
        return

    for r in rounds:
        payload = {
            "start_date": r["start_date"],
            "end_date": r["end_date"],
            "worksheet": r["wksname"]
        }
        try:
            response = requests.post("http://127.0.0.1:5000/generate", json=payload)
            if response.status_code == 200:
                with open(f"{save_path}/{r['wksname']}.csv", "wb") as f:
                    f.write(response.content)
            else:
                messagebox.showerror("Error", f"Failed for {r['wksname']}")
        except Exception as e:
            messagebox.showerror("Exception", str(e))
    
    messagebox.showinfo("สำเร็จ", "โหลดข้อมูลครบทุกช่วงเวลาแล้ว!")

if __name__ == "__main__":
   # GUI
   window = tk.Tk()
   window.title("CSV Generator")
   window.geometry("300x150")

   label = tk.Label(window, text="กดปุ่มเพื่อดึงข้อมูลจาก server", font=("Tahoma", 14))
   label.pack(pady=10)
   btn = tk.Button(window, text="ดึงข้อมูล", font=("Tahoma", 14), command=run_script)
   btn.pack(pady=20)

   window.mainloop()
