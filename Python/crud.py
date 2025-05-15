import mysql.connector

def search_patient(search_term):
    """ค้นหาข้อมูลผู้ป่วยจากฐานข้อมูล hosxp"""
    try:
        # เชื่อมต่อกับฐานข้อมูล MySQL
        mydb = mysql.connector.connect(
            host="192.168.10.1",  # แก้ไขเป็นโฮสต์ของคุณ
            user="chondaen",  # แก้ไขเป็นชื่อผู้ใช้ของคุณ
            password="chondaen",  # แก้ไขเป็นรหัสผ่านของคุณ
            database="hosxp"
        )
        mycursor = mydb.cursor()

        # สร้างคำสั่ง SQL สำหรับค้นหาข้อมูล
        sql = "SELECT hn, cid, fname, hometel FROM patient WHERE hn = %s OR cid = %s"
        val = (search_term, search_term)
        mycursor.execute(sql, val)

        # ดึงข้อมูลผลลัพธ์
        result = mycursor.fetchall()

        # แสดงผลลัพธ์
        if result:
            for row in result:
                print("hn:", row[0])
                print("cid:", row[1])
                print("fname:", row[2])
                print("hometel:", row[3])
                print("-" * 20)
        else:
            print("ไม่พบข้อมูล")

    except mysql.connector.Error as err:
        print(f"เกิดข้อผิดพลาด: {err}")

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

# ส่วนของการทำงานหลักของโปรแกรม
if __name__ == "__main__":
    search_term = input("กรุณาใส่ hn หรือ cid ที่ต้องการค้นหา: ")
    search_patient(search_term)