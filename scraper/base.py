import time
import random
import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import Optional


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


class BaseScraper(ABC):
    def __init__(self, delay: float = 1.5):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _get(self, url: str, params: dict = None) -> Optional[requests.Response]:
        try:
            response = self.session.get(url, params=params, timeout=12)
            response.raise_for_status()
            time.sleep(self.delay + random.uniform(0.2, 0.9))
            return response
        except requests.RequestException as e:
            print(f"[fetch error] {url} — {e}")
            return None

    def _soup(self, url: str) -> Optional[BeautifulSoup]:
        response = self._get(url)
        if response:
            return BeautifulSoup(response.text, "html.parser")
        return None

    def _json(self, url: str, params: dict = None) -> Optional[dict]:
        response = self._get(url, params=params)
        if response:
            try:
                return response.json()
            except Exception:
                return None
        return None

    @abstractmethod
    def run(self) -> list:
        pass
