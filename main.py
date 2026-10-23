import time
import json
from pathlib import Path
from datetime import datetime

VERSION = "2.0"
LOG_FILE = Path("history.json")


def simulate():
    try:
        count = int(input("تعداد عملیات آزمایشی (۱ تا ۳۰۰): "))
        delay = float(input("فاصله زمانی (۰ تا ۵ ثانیه): "))

        if not 1 <= count <= 300 or not 0 <= delay <= 5:
            print("مقادیر واردشده معتبر نیستند.")
            return

        print("\nشروع شبیه‌سازی؛ هیچ پیامکی ارسال نمی‌شود.")

        for i in range(1, count + 1):
            percent = i * 100 // count
            print(f"\rپیشرفت: {percent}% ({i}/{count})", end="", flush=True)
            time.sleep(delay)

        print("\nشبیه‌سازی تمام شد.")

        history = []
        if LOG_FILE.exists():
            try:
                history = json.loads(LOG_FILE.read_text())
                if not isinstance(history, list):
                    history = []
            except (json.JSONDecodeError, OSError):
                history = []

        history.append({
            "date": datetime.now().isoformat(timespec="seconds"),
            "count": count,
            "delay": delay
        })

        LOG_FILE.write_text(
            json.dumps(history, ensure_ascii=False, indent=2)
        )

    except ValueError:
        print("\nلطفاً عدد معتبر وارد کن.")
    except KeyboardInterrupt:
        print("\nعملیات متوقف شد.")


def show_history():
    if not LOG_FILE.exists():
        print("هنوز سابقه‌ای ثبت نشده.")
        return

    try:
        history = json.loads(LOG_FILE.read_text())
        for item in history[-10:]:
            print(
                f"{item['date']} | تعداد: {item['count']} | "
                f"فاصله: {item['delay']} ثانیه"
            )
    except (json.JSONDecodeError, OSError, KeyError, TypeError):
        print("خطا در خواندن سابقه.")


def main():
    while True:
        print(f"\n===== AliTools v{VERSION} =====")
        print("1. شروع شبیه‌سازی")
        print("2. نمایش سابقه")
        print("3. اطلاعات برنامه")
        print("4. خروج")

        choice = input("انتخاب: ").strip()

        if choice == "1":
            simulate()
        elif choice == "2":
            show_history()
        elif choice == "3":
            print("AliTools نسخه آزمایشی 2.0")
            print("این نسخه هیچ پیامک واقعی ارسال نمی‌کند.")
        elif choice == "4":
            print("خدانگهدار!")
            break
        else:
            print("گزینه نامعتبر است.")


if __name__ == "__main__":
    main()
