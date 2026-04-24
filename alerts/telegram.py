import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


class TelegramAlert:
    BASE = "https://api.telegram.org/bot"

    def __init__(self, token: str = TELEGRAM_TOKEN, chat_id: str = TELEGRAM_CHAT_ID):
        self.token = token
        self.chat_id = chat_id
        self.url = f"{self.BASE}{self.token}/sendMessage"

    def _send(self, text: str) -> bool:
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        try:
            response = requests.post(self.url, json=payload, timeout=10)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"[telegram] failed — {e}")
            return False

    def send_price_alert(self, name: str, price: float, stock: str, url: str) -> bool:
        text = (
            f"<b>Price Alert</b>\n\n"
            f"<b>{name}</b>\n"
            f"Price: <code>${price}</code>\n"
            f"Stock: {stock}\n"
            f"<a href='{url}'>View Product</a>"
        )
        return self._send(text)

    def send_restock_alert(self, name: str, price: float, url: str) -> bool:
        text = (
            f"<b>Back In Stock</b>\n\n"
            f"<b>{name}</b>\n"
            f"Price: <code>${price}</code>\n"
            f"<a href='{url}'>View Product</a>"
        )
        return self._send(text)

    def send_summary(self, total: int, deals: int, source: str) -> bool:
        text = (
            f"<b>Monitor Summary</b>\n\n"
            f"Source: {source}\n"
            f"Total tracked: {total}\n"
            f"Deals found: {deals}"
        )
        return self._send(text)

    def send_raw(self, message: str) -> bool:
        return self._send(message)
