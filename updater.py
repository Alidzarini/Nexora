import json
import urllib.request
from pathlib import Path

CURRENT_VERSION = "2.1"

# بعداً آدرس فایل version.json مخزن خودمان را اینجا قرار می‌دهیم.
VERSION_URL = "https://raw.githubusercontent.com/Alidzarini/Nexora/main/version.json"


def check_update():
    if not VERSION_URL:
        print("هنوز مخزن آنلاین برای Nexora تنظیم نشده است.")
        print(f"نسخه نصب‌شده: {CURRENT_VERSION}")
        return

    try:
        request = urllib.request.Request(
            VERSION_URL,
            headers={"User-Agent": "Nexora-Updater"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        latest_version = data.get("version")

        if not latest_version:
            print("اطلاعات نسخه آنلاین معتبر نیست.")
            return

        print(f"نسخه نصب‌شده: {CURRENT_VERSION}")
        print(f"آخرین نسخه: {latest_version}")

        if latest_version != CURRENT_VERSION:
            print("نسخه‌ها متفاوت‌اند؛ بررسی تغییرات لازم است.")
        else:
            print("برنامه به‌روز است.")

    except Exception as error:
        print(f"بررسی به‌روزرسانی ناموفق بود: {error}")


if __name__ == "__main__":
    check_update()
