import unittest
from crawl import *


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html(self):
        input_html ="""<html>
              <body>
                    <h1>Welcome to Boot.dev</h1>
                    <main>
                          <p>Learn to code by building real projects.</p>
                          <p>This is the second paragraph.</p>
                    </main>
              </body>
            </html>"""
        actual = get_heading_from_html(input_html)
        expected = "Welcome to Boot.dev"  
        self.assertEqual(actual, expected)        

    def test_get_first_paragraph_from_html(self):
        input_body = '''<html><body>
        <p>Outside paragraph.</p>
        <main>
            <p>Main paragraph.</p>
        </main>
    </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
        
    def test_get_images_from_html_no_image(self):
        input_url = "https://crawler-test.com"
        input_body = '<html></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_href(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a>Just an anchor</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)    


    def test_get_images_from_html_empty_src(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="" alt="empty image"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)


    def test_get_first_paragraph_from_html_no_p_in_main(self):
        input_body = '''<html><body>
        <main>
            <div>Just a div, no paragraphs here.</div>
            <span>Another element</span>
        </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "" 
        self.assertEqual(actual, expected)
            
    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/about">About Us</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about"]
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_missing_elements(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><div>Just an empty container without our target tags.</div></body></html>'
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "", 
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)


    def test_extract_page_data_multiple_elements(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>First Heading</h1>
            <h1>Second Heading</h1>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
            <a href="/link1">Link 1</a>
            <a href="https://other.com/link2">Link 2</a>
            <img src="/img1.png">
            <img src="/img2.png">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "First Heading",
            "first_paragraph": "First paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1", "https://other.com/link2"],
            "image_urls": ["https://crawler-test.com/img1.png", "https://crawler-test.com/img2.png"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_nested_elements(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <div><article>
                <header><h1>Deep Title</h1></header>
                <main><div><p>Deep paragraph.</p></div></main>
                <footer><a href="/nested">Nested Link</a></footer>
            </article></div>
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Deep Title",
            "first_paragraph": "Deep paragraph.",
            "outgoing_links": ["https://crawler-test.com/nested"],
            "image_urls": []
        }
        self.assertEqual(actual, expected)


    def test_extract_page_data_empty_attributes(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>Valid Title</h1>
            <p>Valid paragraph.</p>
            <a href="">Empty Link</a>
            <img src="" alt="Empty Image">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Valid Title",
            "first_paragraph": "Valid paragraph.",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)


    def test_extract_page_data_whitespace_handling(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>
                Messy Title
            </h1>
            <p>
                Messy paragraph with newlines.
            </p>
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Messy Title",
            "first_paragraph": "Messy paragraph with newlines.",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)

if __name__ =="__main__":
    unittest.main()
