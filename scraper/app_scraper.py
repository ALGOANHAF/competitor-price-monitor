import time
from dataclasses import dataclass, field
from scraper.base import BaseScraper


@dataclass
class AppProduct:
    name: str
    price: float
    currency: str
    stock_status: str
    product_id: str
    source_app: str
    scraped_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))

    def to_dict(self) -> dict:
        return self.__dict__


class AppScraper(BaseScraper):
    def __init__(self, api_base: str, app_name: str, headers: dict = None, delay: float = 2.0):
        super().__init__(delay)
        self.api_base = api_base.rstrip("/")
        self.app_name = app_name
        if headers:
            self.session.headers.update(headers)
        self.products: list[AppProduct] = []

    def _extract_product(self, raw: dict) -> AppProduct | None:
        try:
            return AppProduct(
                name=raw.get("name") or raw.get("title") or "unknown",
                price=float(raw.get("price") or raw.get("selling_price") or 0),
                currency=raw.get("currency") or raw.get("currency_code") or "USD",
                stock_status=raw.get("stock") or raw.get("availability") or "unknown",
                product_id=str(raw.get("id") or raw.get("product_id") or ""),
                source_app=self.app_name,
            )
        except Exception:
            return None

    def scrape_endpoint(self, endpoint: str, params: dict = None) -> list[AppProduct]:
        url = f"{self.api_base}/{endpoint.lstrip('/')}"
        data = self._json(url, params=params)
        if not data:
            return []

        items = []
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            for key in ["products", "items", "results", "data"]:
                if key in data and isinstance(data[key], list):
                    items = data[key]
                    break

        results = []
        for item in items:
            product = self._extract_product(item)
            if product:
                results.append(product)

        print(f"[app:{self.app_name}] {endpoint} — {len(results)} products")
        return results

    def run(self, endpoints: list[str] = None, params: dict = None) -> list[AppProduct]:
        targets = endpoints or ["/products", "/items"]
        for endpoint in targets:
            batch = self.scrape_endpoint(endpoint, params)
            self.products.extend(batch)
        return self.products

    def filter_by_price(self, max_price: float) -> list[AppProduct]:
        return [p for p in self.products if p.price <= max_price]
