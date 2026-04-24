import sqlite3
from pathlib import Path


DB_PATH = Path("data/monitor.db")


class Database:
    def __init__(self, path: Path = DB_PATH):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL,
                    stock TEXT,
                    rating TEXT,
                    url TEXT UNIQUE,
                    category TEXT,
                    source TEXT,
                    scraped_at TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_url TEXT,
                    price REAL,
                    stock TEXT,
                    recorded_at TEXT DEFAULT (datetime('now'))
                )
            """)

    def upsert_product(self, product: dict) -> None:
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT price FROM products WHERE url = ?", (product.get("url"),)
            ).fetchone()

            if existing:
                old_price = existing["price"]
                conn.execute(
                    "UPDATE products SET price=?, stock=?, scraped_at=? WHERE url=?",
                    (product["price"], product.get("stock"), product.get("scraped_at"), product["url"])
                )
                if old_price != product["price"]:
                    conn.execute(
                        "INSERT INTO price_history (product_url, price, stock) VALUES (?, ?, ?)",
                        (product["url"], product["price"], product.get("stock"))
                    )
            else:
                conn.execute(
                    "INSERT INTO products (name, price, stock, rating, url, category, source, scraped_at) VALUES (?,?,?,?,?,?,?,?)",
                    (
                        product.get("name"), product.get("price"), product.get("stock"),
                        product.get("rating"), product.get("url"), product.get("category"),
                        product.get("source_app", "web"), product.get("scraped_at")
                    )
                )

    def get_price_drops(self) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT p.name, p.url, p.price as current_price, h.price as old_price
                FROM products p
                JOIN price_history h ON p.url = h.product_url
                WHERE p.price < h.price
                ORDER BY h.recorded_at DESC
            """).fetchall()
            return [dict(row) for row in rows]

    def get_all(self, category: str = None) -> list[dict]:
        with self._connect() as conn:
            if category:
                rows = conn.execute("SELECT * FROM products WHERE category=?", (category,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM products").fetchall()
            return [dict(row) for row in rows]

    def clear(self) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM products")
            conn.execute("DELETE FROM price_history")
