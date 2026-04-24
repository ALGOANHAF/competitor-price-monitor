import time
import schedule
from scraper.web_scraper import WebScraper
from scraper.app_scraper import AppScraper
from alerts.telegram import TelegramAlert
from alerts.email_sender import EmailSender
from storage.db import Database
from storage.sheets import SheetsSync
from config import (
    TARGET_URL, PRICE_THRESHOLD, MAX_PAGES,
    SCRAPE_INTERVAL_SECONDS, TELEGRAM_TOKEN,
    SHEETS_WEBHOOK_URL
)


class MonitorScheduler:
    def __init__(self):
        self.db = Database()
        self.telegram = TelegramAlert() if TELEGRAM_TOKEN else None
        self.sheets = SheetsSync() if SHEETS_WEBHOOK_URL else None
        self.email = EmailSender()

    def _run_web_cycle(self) -> None:
        print(f"\n[scheduler] web cycle started — {time.strftime('%Y-%m-%d %H:%M:%S')}")

        scraper = WebScraper(base_url=TARGET_URL)
        products = scraper.run(max_pages=MAX_PAGES)

        for p in products:
            self.db.upsert_product(p.to_dict())

        deals = scraper.filter_by_price(PRICE_THRESHOLD)
        in_stock_deals = [d for d in deals if d.is_in_stock()]

        if self.telegram:
            for deal in in_stock_deals[:5]:
                self.telegram.send_price_alert(
                    name=deal.name,
                    price=deal.price,
                    stock=deal.stock,
                    url=deal.url,
                )
            self.telegram.send_summary(
                total=len(products),
                deals=len(in_stock_deals),
                source=TARGET_URL,
            )

        scraper.export_csv("results.csv")

        if self.sheets:
            self.sheets.push_products([p.to_dict() for p in products])

        if in_stock_deals:
            self.email.send_report(
                csv_path="results.csv",
                source=TARGET_URL,
                deal_count=len(in_stock_deals),
            )

        print(f"[scheduler] cycle done — {len(products)} tracked, {len(in_stock_deals)} deals")

    def _run_price_drop_check(self) -> None:
        drops = self.db.get_price_drops()
        if drops and self.telegram:
            for drop in drops[:3]:
                msg = (
                    f"<b>Price Drop Detected</b>\n\n"
                    f"{drop['name']}\n"
                    f"Was: <s>${drop['old_price']}</s> → Now: <code>${drop['current_price']}</code>\n"
                    f"<a href='{drop['url']}'>View</a>"
                )
                self.telegram.send_raw(msg)

    def start(self, interval_seconds: int = SCRAPE_INTERVAL_SECONDS) -> None:
        print(f"[scheduler] starting — interval {interval_seconds}s")
        self._run_web_cycle()

        schedule.every(interval_seconds).seconds.do(self._run_web_cycle)
        schedule.every(interval_seconds * 2).seconds.do(self._run_price_drop_check)

        while True:
            schedule.run_pending()
            time.sleep(30)
