<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=28&pause=1000&color=1D9E75&center=true&vCenter=true&width=700&lines=Competitor+Price+%26+Stock+Monitor;Web+%2B+App+Automation+System;24%2F7+Real-Time+Tracking+Engine" alt="Typing SVG" />

<br/>

[![Fiverr](https://img.shields.io/badge/Hire_Me-Fiverr-1DBF73?style=for-the-badge&logo=fiverr&logoColor=white)](https://www.fiverr.com/s/pdKd8Rl)
[![Telegram](https://img.shields.io/badge/Message_Me-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/anhafxd)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **Automated competitor intelligence — prices, stock, and reviews tracked 24/7 across websites and mobile apps.**

</div>

---

## What This Does

This is a demo of the core engine behind my Fiverr service. It scrapes live product data from competitor sites, processes it, and delivers structured output — ready to pipe into Telegram alerts, Google Sheets, or email reports.

Built for e-commerce owners, dropshippers, and pricing teams who need real data without manual work.

---

## Features

<img align="right" src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=13&pause=2000&color=1D9E75&vCenter=true&width=280&lines=Price+dropped+%E2%86%93+%2418.50;Stock+low+%E2%80%94+restock+alert+sent;New+review+detected+%E2%80%94+logged" alt="Live demo" />

- Tracks prices across **websites and mobile apps**
- Detects stock changes and fires **instant alerts**
- Runs on **custom intervals** — hourly, daily, or real-time
- Delivers reports via **Telegram, Email, Google Sheets**
- Handles **protected platforms** via reverse engineering
- Exports clean **CSV / JSON** output

<br clear="right"/>

---

## Stack

<div align="center">

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![aiohttp](https://img.shields.io/badge/-aiohttp-2C5BB4?style=flat-square)
![BeautifulSoup](https://img.shields.io/badge/-BeautifulSoup4-59666C?style=flat-square)
![Playwright](https://img.shields.io/badge/-Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![Telegram](https://img.shields.io/badge/-Telegram_Bot-2CA5E0?style=flat-square&logo=telegram&logoColor=white)
![Google Sheets](https://img.shields.io/badge/-Google_Sheets-34A853?style=flat-square&logo=googlesheets&logoColor=white)
![SQLite](https://img.shields.io/badge/-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

</div>

---

## Project Structure

```
competitor-monitor/
├── scraper/
│   ├── base.py          # Abstract scraper base class
│   ├── web_scraper.py   # Website price & stock extractor
│   └── app_scraper.py   # Mobile app API extractor
├── alerts/
│   ├── telegram.py      # Telegram alert dispatcher
│   └── email_sender.py  # Email report sender
├── storage/
│   ├── db.py            # SQLite persistence layer
│   └── sheets.py        # Google Sheets sync
├── scheduler.py         # Interval-based automation runner
├── main.py              # Entry point
├── config.py            # Platform targets & thresholds
└── requirements.txt
```

---

## Quick Look

```python
from scraper.web_scraper import WebScraper

scraper = WebScraper(url="https://example-store.com/products")
results = scraper.run()

# Output
# [
#   { "name": "Product A", "price": 29.99, "stock": "In Stock" },
#   { "name": "Product B", "price": 18.50, "stock": "Low Stock" },
# ]
```

---

## What I Build For Clients

| Package | Coverage | Alerts | Price |
|---|---|---|---|
| Starter Monitor | 1 website | CSV report | $80 |
| Web + App Pro | 3 sites or 1 app + 1 site | Telegram | $200 |
| Full Intel System | 6 sites + 2 apps | Telegram + Email | $380 |

Every delivery includes clean, documented source code and deployment support.

---

## Want This For Your Store?

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=16&pause=1500&color=1D9E75&center=true&vCenter=true&width=600&lines=Message+me+on+Telegram+%40anhafxd;Or+order+directly+on+Fiverr;Free+feasibility+check+before+you+order" alt="CTA" />

<br/><br/>

[![Order on Fiverr](https://img.shields.io/badge/Order_Now-Fiverr-1DBF73?style=for-the-badge&logo=fiverr&logoColor=white&labelColor=0D0D0D)](https://www.fiverr.com/s/pdKd8Rl)
&nbsp;&nbsp;
[![Chat on Telegram](https://img.shields.io/badge/Chat_Now-@anhafxd-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white&labelColor=0D0D0D)](https://t.me/anhafxd)

<br/><br/>

*Message me first — I'll confirm your platform is feasible before you spend a cent.*

</div>

---

<div align="center">
<sub>Built by <a href="https://t.me/anhafxd">@anhafxd</a> · <a href="https://www.fiverr.com/s/pdKd8Rl">Fiverr Profile</a></sub>
</div>
