import sys
import asyncio
import argparse

from crawl import *
from json_report import write_json_report 

async def main():
    print("Hello from python-web-scraper")

    parser = argparse.ArgumentParser(description="Async Web Crawler")
    parser.add_argument("url", help="Base URL to crawl")
    parser.add_argument("max_concurrency", type=int, nargs='?', default=3, help="Maximum concurrent requests")
    parser.add_argument("max_pages", type=int, nargs='?', default=10, help="Maximum number of pages to crawl")
    
   
    parser.add_argument("--output", "-o", choices=["console", "json"], default="console", 
                        help="Choose output format: 'console' (default) or 'json' (saves to report.json)")
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    print(f"starting crawl of: {args.url}\n")

    page_data = await crawl_site_async(args.url, args.max_concurrency, args.max_pages)
    
   
    if args.output == "json":
   
        write_json_report(page_data)
        print(f"🎉 CRAWL COMPLETE: Found {len(page_data)} pages.")
        print("Report successfully saved to report.json")
        
    else:
   
        print(f"==================================================")
        print(f"🎉 CRAWL COMPLETE: Found {len(page_data)} pages!")
        print(f"==================================================\n")
        
        for url, data in page_data.items():
            title = data.get('heading') or "No Title Found"
            
            print(f"🔹 {title.upper()}")
            print(f"   Link:  {url}")
            
            paragraph = data.get('first_paragraph')
            if paragraph:
                snippet = paragraph[:80] + "..." if len(paragraph) > 80 else paragraph
                print(f"   About: {snippet}")
                
            links_count = len(data.get('outgoing_links', []))
            images_count = len(data.get('image_urls', []))
            print(f"   Stats: {links_count} links | {images_count} images")
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())

