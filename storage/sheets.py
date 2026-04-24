import csv
import time
import requests
from pathlib import Path
from config import SHEETS_WEBHOOK_URL


class SheetsSync:
    def __init__(self, webhook_url: str = SHEETS_WEBHOOK_URL):
        self.webhook_url = webhook_url

    def _post(self, payload: dict) -> bool:
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=12)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"[sheets] failed — {e}")
            return False

    def push_products(self, products: list[dict]) -> bool:
        if not products:
            print("[sheets] nothing to push.")
            return False
        payload = {
            "action": "upsert",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "rows": products,
        }
        result = self._post(payload)
        if result:
            print(f"[sheets] pushed {len(products)} rows.")
        return result

    def push_csv(self, csv_path: str) -> bool:
        path = Path(csv_path)
        if not path.exists():
            print(f"[sheets] file not found — {csv_path}")
            return False
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return self.push_products(rows)

    def push_alert(self, name: str, price: float, stock: str, url: str) -> bool:
        payload = {
            "action": "alert",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "price": price,
            "stock": stock,
            "url": url,
        }
        return self._post(payload)
