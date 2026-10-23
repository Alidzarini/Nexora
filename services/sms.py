import time
from collections import deque


class SMSService:
    """Base interface for authorized SMS providers."""

    def send(self, recipient, message):
        raise NotImplementedError


class DemoSMSService(SMSService):
    """Safe demo: never sends a real SMS."""

    def send(self, recipient, message):
        print(f"[آزمایشی] گیرنده: {recipient} | متن: {message}")
        return True


def run_demo_queue(messages, delay=1):
    queue = deque(messages)
    service = DemoSMSService()

    while queue:
        recipient, message = queue.popleft()
        service.send(recipient, message)
        if queue:
            time.sleep(delay)

    print("صف آزمایشی تمام شد.")
