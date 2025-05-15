import tkinter as tk
import mysql.connector

def search_patient():
    search_term = entry_search.get()
    try:
        mydb = mysql.connector.connect(
            host="192.168.10.1",
            user="chondaen",
            password="chondaen",
            database="hosxp"
        )
        mycursor = mydb.cursor()
        sql = "SELECT hn, cid, fname, hometel FROM patient WHERE hn = %s OR cid = %s"
        val = (search_term, search_term)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if result:
            result_text.delete(1.0, tk.END)
            for row in result:
                result_text.insert(tk.END, f"HN: {row[0]}\n")
                result_text.insert(tk.END, f"CID: {row[1]}\n")
                result_text.insert(tk.END, f"ชื่อ: {row[2]}\n")
                result_text.insert(tk.END, f"เบอร์โทร: {row[3]}\n")
                result_text.insert(tk.END, "-" * 20 + "\n")
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "ไม่พบข้อมูล")
    except mysql.connector.Error as err:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"เกิดข้อผิดพลาด: {err}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

# สร้างหน้าต่างหลัก
window = tk.Tk()
window.title("ค้นหาผู้ป่วย")

# สร้าง textbox สำหรับค้นหา
label_search = tk.Label(window, text="HN หรือ CID:")
label_search.pack()
entry_search = tk.Entry(window)
entry_search.pack()

# สร้างปุ่มค้นหา
button_search = tk.Button(window, text="ค้นหา", command=search_patient)
button_search.pack()

# สร้าง textbox สำหรับแสดงผลลัพธ์
result_text = tk.Text(window)
result_text.pack()

# เริ่มต้นลูปหลักของ Tkinter
window.mainloop()