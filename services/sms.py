class SMSService:
    """Base interface for authorized SMS providers."""

    def send(self, recipient, message):
        raise NotImplementedError("این سرویس هنوز پیاده‌سازی نشده است.")


class DemoSMSService(SMSService):
    """Safe demo: never sends a real SMS."""

    def send(self, recipient, message):
        print("حالت آزمایشی: هیچ پیامکی ارسال نشد.")
        return False
