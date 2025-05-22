# pip install requests configparser
import requests
import configparser
import os

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(config_path)

BACKEND_URL = config['backend']['url']

def main():
    start_date = input("Enter start date (YYYY-MM-DD): ")

    response = requests.post(
        f"{BACKEND_URL}/upload",
        json={"start_date": start_date}
    )

    if response.status_code == 200:
        print("✅ อัปโหลดข้อมูลสำเร็จ")
    else:
        print("❌ เกิดข้อผิดพลาด:", response.json())

if __name__ == "__main__":
    main()
