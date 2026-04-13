from urllib.parse import urlsplit, urljoin, urlparse
from bs4 import BeautifulSoup
import requests
import sys
import asyncio
import aiohttp



def normalize_url(url):

    o = urlsplit(url)
    return "".join((o.netloc, o.path))
    

def get_heading_from_html(html):

    soup = BeautifulSoup(html, 'html.parser')

    for tag_name in ['h1', 'h2', 'h3']:

        tag = soup.find(tag_name)
        if tag:

            return tag.get_text(strip=True)

    return ''

def get_first_paragraph_from_html(html):

    soup = BeautifulSoup(html, 'html.parser')

    main = soup.find('main')

    if main:

        p = main.find('p') 
        if p:
            return p.get_text(strip=True)

    p =  soup.find('p')

    return p.get_text(strip=True) if p else ""

def get_urls_from_html(html, base_url):

    soup = BeautifulSoup(html, 'html.parser')

    a_tags = soup.find_all('a')

    urls = []

    for a_tag in a_tags:

        href = a_tag.get('href')

        if href:

             urls.append(urljoin(base_url, href))
                    
    return urls


def get_images_from_html(html, base_url):

    soup = BeautifulSoup(html, 'html.parser')

    img_tags = soup.find_all('img')

    urls = []

    for img_tag in img_tags:

        src = img_tag.get('src')

        if src:

            urls.append(urljoin(base_url, src))

    return urls


def extract_page_data(html, url):

    res = {}


    res['url'] = url if url else ''
    res['heading'] = get_heading_from_html(html)
    res['first_paragraph'] = get_first_paragraph_from_html(html)
    res['outgoing_links'] =  get_urls_from_html(html, url)
    res['image_urls'] = get_images_from_html(html, url)

    return res



def get_html(url):

    try:
        response = requests.get(url, headers={"User-Agent": "BoootCrawler/1.0"})

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            raise ValueError(f"Expected HTML, but got {content_type}")

        return response.text

    except Exception as e:
        raise e


def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}

    base_url_obj = urlparse(base_url)
    current_url_obj = urlparse(current_url)
    if current_url_obj.netloc != base_url_obj.netloc:
        return page_data

    normalized_url = normalize_url(current_url)

    if normalized_url in page_data:
        return page_data

    print(f"crawling {current_url}")
    html = safe_get_html(current_url)
    if html is None:
        return page_data

    page_info = extract_page_data(html, current_url)
    page_data[normalized_url] = page_info

    next_urls = get_urls_from_html(html, base_url)
    for next_url in next_urls:
        page_data = crawl_page(base_url, next_url, page_data)

    return page_data



def safe_get_html(url):
    try:
        return get_html(url)
    except Exception as e:
        print(f"{e}")
        return None


class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=3, max_pages=10): 

        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()

        self.max_concurrency = 3
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
	    await self.session.close()
		

    async def add_page_visit(self, normalized_url):

        if self.should_stop:
            return False

        async with self.lock:
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Maximum number of pages to craw has been reached")
                for task in self.all_tasks:
                    task.cancel()
                return False

            if normalized_url in self.page_data:
                return False
            else:
                return True
    async def get_html(self, url):
        try:
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as response:
                if response.status > 399:
                    raise Exception(f"got HTTP error: {response.status_code} {response.reason}")

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    raise Exception(f"got non-HTML response: {content_type}")

                return await  response.text()
    
        except Exception as e:
            raise Exception(f"Error fetching {url}: {e}")

    async def crawl_page(self, current_url=None, page_data=None):

        task = asyncio.current_task()
        self.all_tasks.add(task)

        try:
            if self.should_stop:
                return

            current_url_obj = urlparse(current_url)
            if current_url_obj.netloc != self.base_domain:
                return

            normalized_url = normalize_url(current_url)

            is_new = await self.add_page_visit(normalized_url)
            if not is_new:
                return

            async with self.semaphore:
                print(
                    f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
                )
                html = await self.get_html(current_url)
                if html is None:
                    return

                page_info = extract_page_data(html, current_url)
                async with self.lock:
                    self.page_data[normalized_url] = page_info

                next_urls = get_urls_from_html(html, self.base_url)
    
            tasks = []
            for next_url in next_urls:
                tasks.append(asyncio.create_task(self.crawl_page(next_url)))

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

        finally:
            self.all_tasks.discard(task)
    async def crawl(self):
        try:
            await self.crawl_page(self.base_url)

        except asyncio.CancelledError:
            pass
        return self.page_data


async def crawl_site_async(base_url, max_concurrency=3, max_pages=10):
   
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
