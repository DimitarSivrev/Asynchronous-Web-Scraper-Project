import sys
import asyncio
import argparse

from crawl import *
from json_report import write_json_report  

async def main():
    print("Hello from python-web-scraper")

    parser = argparse.ArgumentParser(description="Async Web Crawler")
    parser.add_argument("url", help="Base URL to crawl")
    parser.add_argument("--max-concurrency", type=int, default=3, help="Maximum concurrent requests")
    parser.add_argument("--max-pages", type=int, default=10, help="Maximum number of pages to crawl")
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    print(f"starting crawl of: {args.url}")

    page_data = await crawl_site_async(args.url, args.max_concurrency, args.max_pages)
    print(f"Found {len(page_data)} pages.")
    
    
    write_json_report(page_data)
    print("Report saved to report.json")

if __name__ == "__main__":
    asyncio.run(main())
