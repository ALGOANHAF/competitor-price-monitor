import time
import csv
from dataclasses import dataclass, field
from typing import Optional
from scraper.base import BaseScraper


@dataclass
class Product:
    name: str
    price: float
    stock: str
    rating: str
    url: str
    category: str = "general"
    scraped_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))

    def is_in_stock(self) -> bool:
        return "in stock" in self.stock.lower()

    def to_dict(self) -> dict:
        return self.__dict__


class WebScraper(BaseScraper):
    RATING_MAP = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}

    def __init__(self, base_url: str, delay: float = 1.5):
        super().__init__(delay)
        self.base_url = base_url.rstrip("/")
        self.products: list[Product] = []

    def _clean_price(self, raw: str) -> float:
        for char in ["£", "$", "€", "Â", ","]:
            raw = raw.replace(char, "")
        try:
            return float(raw.strip())
        except ValueError:
            return 0.0

    def _parse_card(self, card, category: str) -> Optional[Product]:
        try:
            name = card.h3.a["title"]
            price = self._clean_price(card.select_one("p.price_color").text)
            stock = card.select_one("p.availability").text.strip()
            rating = self.RATING_MAP.get(card.p["class"][1], "0")
            href = card.h3.a["href"].replace("../../../", "")
            url = f"{self.base_url}/catalogue/{href}"
            return Product(name=name, price=price, stock=stock, rating=rating, url=url, category=category)
        except Exception:
            return None

    def scrape_page(self, url: str, category: str = "general") -> list[Product]:
        soup = self._soup(url)
        if not soup:
            return []
        results = []
        for card in soup.select("article.product_pod"):
            product = self._parse_card(card, category)
            if product:
                results.append(product)
        return results

    def run(self, max_pages: int = 3, category: str = "general") -> list[Product]:
        for page in range(1, max_pages + 1):
            url = (
                f"{self.base_url}/catalogue/index.html"
                if page == 1
                else f"{self.base_url}/catalogue/page-{page}.html"
            )
            batch = self.scrape_page(url, category)
            if not batch:
                break
            self.products.extend(batch)
            print(f"[web] page {page} — {len(batch)} products")
        return self.products

    def filter_by_price(self, max_price: float) -> list[Product]:
        return [p for p in self.products if p.price <= max_price]

    def filter_in_stock(self) -> list[Product]:
        return [p for p in self.products if p.is_in_stock()]

    def sort_by_price(self, ascending: bool = True) -> list[Product]:
        return sorted(self.products, key=lambda p: p.price, reverse=not ascending)

    def export_csv(self, filename: str = "results.csv") -> None:
        if not self.products:
            print("[export] nothing to write.")
            return
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.products[0].to_dict().keys())
            writer.writeheader()
            writer.writerows(p.to_dict() for p in self.products)
        print(f"[export] {len(self.products)} products → {filename}")
