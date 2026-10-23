import json
import re
import shutil
import urllib.request
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/Alidzarini/Nexora/main"

FILES = [
    Path("main.py"),
    Path("updater.py"),
    Path("services/sms.py"),
]


def fetch(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": "Nexora-Updater"}
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def version_tuple(value):
    if not re.fullmatch(r"\d+(\.\d+)*", value):
        raise ValueError("فرمت نسخه معتبر نیست.")
    return tuple(map(int, value.split(".")))


def check_update():
    try:
        current_code = Path("main.py").read_text(encoding="utf-8")
        match = re.search(
            r'^VERSION\s*=\s*["\']([^"\']+)',
            current_code,
            re.M,
        )
        if not match:
            print("نسخه نصب‌شده مشخص نیست.")
            return

        current = match.group(1)
        data = json.loads(
            fetch(f"{BASE_URL}/version.json").decode("utf-8")
        )
        latest = str(data.get("version", ""))

        print(f"نسخه نصب‌شده: {current}")
        print(f"آخرین نسخه: {latest}")

        if version_tuple(latest) <= version_tuple(current):
            print("برنامه به‌روز است.")
            return

        if input("نسخه جدید دانلود و نصب شود؟ (y/n): ").strip().lower() != "y":
            print("به‌روزرسانی لغو شد.")
            return

        downloaded = {}

        for path in FILES:
            content = fetch(f"{BASE_URL}/{path.as_posix()}").decode("utf-8")
            if path.suffix == ".py":
                compile(content, str(path), "exec")
            downloaded[path] = content

        new_main = downloaded[Path("main.py")]
        match = re.search(r'^VERSION\s*=\s*["\']([^"\']+)', new_main, re.M)

        if not match or match.group(1) != latest:
            print("نسخه فایل اصلی با نسخه آنلاین هماهنگ نیست؛ نصب لغو شد.")
            return

        for path, content in downloaded.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                shutil.copy2(path, Path(str(path) + ".bak"))
            temp = Path(str(path) + ".new")
            temp.write_text(content, encoding="utf-8")
            temp.replace(path)

        print(f"Nexora با موفقیت به نسخه {latest} به‌روزرسانی شد.")
        print("نسخه‌های پشتیبان با پسوند .bak ذخیره شدند.")

    except Exception as error:
        print(f"به‌روزرسانی ناموفق بود: {error}")


if __name__ == "__main__":
    check_update()
