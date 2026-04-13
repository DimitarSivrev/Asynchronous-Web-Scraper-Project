# Asynchronous-Web-Scraper-Project
High performance, asynchronous web scraper built to extract and structure data into JSON reports.

*High performance, asynchronous web scraper built to extract and structure data into JSON reports.*

# Tech Stack

- **Language:** Python 3.12+
- **Core Libraries:** `asyncio`, `aiohttp`, `BeautifulSoup4`
- **Testing:** `unittest`

# Overview

This command-line tool asynchronously crawls websites to extract structured page data, including headings, primary paragraphs, outgoing links, and image URLs. It respects domain boundaries, utilizes asynchronous I/O for speed, and exports the gathered data into a clean, hierarchical JSON report

# Biggest Challenge

Initially, I didn't have much experience in asynchronous programming. These are problems I came across:

- Wrapping my head around synchronous blocking code and non-blocking `await` calls.
- Different tasks writing to the `page_data` dictionary simultaneously.
- The `max_pages` limit caused aggressive task cancellations that swallowed the main program execution, raising unhandled `CancelledError` exceptions and crashing the script.

# Overcoming the Challenges 

I paused the development to study the `asyncio` library and the `aiohttp` framework. The changes made include:

- Used `asyncio.Lock` to ensure that only one coroutine modifies the dictionary at a time.
- Used `try/except` blocks to handle the `CancelledError`s.

# Usage

Run the crawler by providing a target URL. You can optionally define the maximum number of concurrent network requests, the total page limit, and your desired output format.

**Command Syntax:**
```bash
uv run main.py <target_url> [max_concurrency] [max_pages] [--output {console,json}]
```
Examples:

Default Crawl (3 concurrent requests, max 10 pages, prints to console):
```Bash
uv run main.py [https://example.com](https://example.com)
```

Custom Limits (5 concurrent requests, max 25 pages):
```Bash
uv run main.py [https://example.com](https://example.com) 5 25
```

Save Report to JSON (Using the -o or --output flag):
```Bash
uv run main.py [https://example.com](https://example.com) 5 25 -o json
```

Arguments & Flags:

- **target_url:** The base URL you want to scrape (required).
- **max_concurrency:** How many pages to fetch at the exact same time (default: 3).
- **max_pages:** The hard limit on how many total pages to process before finishing (default: 10).
- **--output / -o:** Choose the output format. Options are console or json (default: console).

# Example Usage

Input
```bash
uv run main.py https://learnwebscraping.dev/practice/ecommerce/ 3 10
```

Output
```bash

==================================================
🎉 CRAWL COMPLETE: Found 10 pages!
==================================================

🔹 FANTASY ECOMMERCE CATALOG
   Link:  learnwebscraping.dev/practice/ecommerce/
   About: Browse fantasy product listings, category pages, detail pages, prices, rarity, s...
   Stats: 36 links | 0 images
--------------------------------------------------
🔹 FANTASY ECOMMERCE CATEGORIES
   Link:  learnwebscraping.dev/practice/ecommerce/categories/
   About: Browse 6 categories and 36 product pages across the fantasy catalog.
   Stats: 10 links | 0 images
--------------------------------------------------
🔹 KINGSHADE BASTARD SWORD
   Link:  learnwebscraping.dev/practice/ecommerce/products/kingshade-bastard-sword-fan-1002/
   About: A hand-and-a-half sword with a blackened blade and silver runes, prized for its ...
   Stats: 7 links | 1 images
--------------------------------------------------
🔹 MOONLIT TOURNAMENT BLADE
   Link:  learnwebscraping.dev/practice/ecommerce/products/moonlit-tournament-blade-fan-1003/
   About: A polished blade that moves easily from the tournament lists to moonlit monster ...
   Stats: 7 links | 1 images
--------------------------------------------------
🔹 ASHENFANG LONGSWORD
   Link:  learnwebscraping.dev/practice/ecommerce/products/ashenfang-longsword-fan-1001/
   About: A balanced battlefield blade with a smoldering fuller and leather-wrapped grip s...
   Stats: 7 links | 1 images
--------------------------------------------------
🔹 GARRISON OATHBLADE
   Link:  learnwebscraping.dev/practice/ecommerce/products/garrison-oathblade-fan-1004/
   About: A straightforward service blade with excellent balance, easy upkeep, and a broad...
   Stats: 7 links | 1 images
--------------------------------------------------
🔹 VERDANT DUELIST SABER
   Link:  learnwebscraping.dev/practice/ecommerce/products/verdant-duelist-saber-fan-1005/
   About: A slim saber-longsword hybrid with a lively tip and vine-work guard built for qu...
   Stats: 7 links | 1 images
--------------------------------------------------
🔹 SUNSPIRE RELIC BLADE
   Link:  learnwebscraping.dev/practice/ecommerce/products/sunspire-relic-blade-fan-1006/
   About: A consecrated relic sword with gold inlay and a luminous fuller that flashes war...
   Stats: 7 links | 1 images
--------------------------------------------------
🔹 STARWELL APPRENTICE STAFF
   Link:  learnwebscraping.dev/practice/ecommerce/products/starwell-apprentice-staff-fan-1101/
   About: A sturdy beginner staff with a sanded rowan shaft and modest crystal cap tuned f...
   Stats: 7 links | 1 images
--------------------------------------------------
🔹 STORMGLASS CHANNELING STAFF
   Link:  learnwebscraping.dev/practice/ecommerce/products/stormglass-channeling-staff-fan-1102/
   About: A medium-length war staff that amplifies lightning and wind magic while remainin...
   Stats: 7 links | 1 images
```

# Setup

**Prerequisites:**
* Python 3.12 or higher
* [uv](https://github.com/astral-sh/uv) (Extremely fast Python package installer and resolver)

**Step 1: Clone the repository**
```bash
git clone https://github.com/DimitarSivrev/Asynchronous-Web-Scraper-Project.git
cd python-web-scraper
```

**Step 2: Install dependencies**
Using `uv`, you can install the dependencies defined in the `pyproject.toml` file and create a virtual environment in one step:
```bash
uv sync
```

**Step 3: Run the scraper**
```bash
uv run main.py https://learnwebscraping.dev 3 10
```
