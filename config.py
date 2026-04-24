import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Email
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASS = os.getenv("EMAIL_PASS", "")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "")

# Google Sheets
SHEETS_WEBHOOK_URL = os.getenv("SHEETS_WEBHOOK_URL", "")

# Scraper targets
TARGET_URL = os.getenv("TARGET_URL", "https://books.toscrape.com")
PRICE_THRESHOLD = float(os.getenv("PRICE_THRESHOLD", 20.0))
MAX_PAGES = int(os.getenv("MAX_PAGES", 3))
SCRAPE_INTERVAL_SECONDS = int(os.getenv("SCRAPE_INTERVAL_SECONDS", 3600))
