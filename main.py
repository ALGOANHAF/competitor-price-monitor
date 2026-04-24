from scheduler import MonitorScheduler
from config import SCRAPE_INTERVAL_SECONDS


if __name__ == "__main__":
    monitor = MonitorScheduler()
    monitor.start(interval_seconds=SCRAPE_INTERVAL_SECONDS)
