import json
import re
import shutil
import urllib.request
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/Alidzarini/Nexora/main"
VERSION_FILE = Path("version.json")
MAIN_FILE = Path("main.py")
BACKUP_FILE = Path("main.py.bak")


def fetch(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": "Nexora-Updater"}
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read()


def check_update():
    try:
        current_code = MAIN_FILE.read_text(encoding="utf-8")
        match = re.search(r'^VERSION\s*=\s*["\']([^"\']+)', current_code, re.M)
        if not match:
            print("نسخه فعلی قابل تشخیص نیست.")
            return

        current = match.group(1)
        data = json.loads(fetch(f"{BASE_URL}/version.json").decode("utf-8"))
        latest = data.get("version", "")

        print(f"نسخه نصب‌شده: {current}")
        print(f"آخرین نسخه: {latest}")

        if not latest:
            print("نسخه آنلاین معتبر نیست.")
            return
        if latest == current:
            print("برنامه به‌روز است.")
            return

        answer = input("نسخه جدید دریافت شود؟ (y/n): ").strip().lower()
        if answer != "y":
            print("به‌روزرسانی لغو شد.")
            return

        new_code = fetch(f"{BASE_URL}/main.py").decode("utf-8")
        compile(new_code, "main.py", "exec")

        if f'VERSION = "{latest}"' not in new_code and f"VERSION = '{latest}'" not in new_code:
            print("نسخه داخل main.py با اطلاعات آنلاین هماهنگ نیست.")
            return

        shutil.copy2(MAIN_FILE, BACKUP_FILE)
        MAIN_FILE.write_text(new_code, encoding="utf-8")
        print("به‌روزرسانی انجام شد. نسخه قبلی در main.py.bak ذخیره شد.")

    except Exception as error:
        print(f"به‌روزرسانی ناموفق بود: {error}")


if __name__ == "__main__":
    check_update()
