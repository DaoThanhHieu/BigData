import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://books.toscrape.com"
OUTPUT_FILE = "books_raw.jsonl"
BOOKS_TO_CRAWL = 1000
BOOKS_PER_PAGE = 20

RATING_MAP = {
    "One": 1.0,
    "Two": 2.0,
    "Three": 3.0,
    "Four": 4.0,
    "Five": 5.0
}

def get_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_book_info(book_soup):
    rating_str = book_soup.p['class'][1]
    return {
        "title": book_soup.h3.a['title'],
        "price": book_soup.find('p', class_='price_color').text,
        "rating": RATING_MAP.get(rating_str, 0.0),  # Mặc định là 0.0 nếu không có rating hợp lệ
        "url": BASE_URL + "/catalogue/" + book_soup.h3.a['href']
    }

def crawl_books():
    books = []
    total_pages = (BOOKS_TO_CRAWL + BOOKS_PER_PAGE - 1) // BOOKS_PER_PAGE

    for page in range(1, total_pages + 1):
        print(f"Crawling page {page}...")
        url = f"{BASE_URL}/catalogue/page-{page}.html"
        soup = get_page(url)
        articles = soup.find_all('article', class_='product_pod')
        for a in articles:
            if len(books) < BOOKS_TO_CRAWL:
                books.append(extract_book_info(a))
            else:
                break

    return books

def save_to_jsonl(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    books = crawl_books()
    save_to_jsonl(books, OUTPUT_FILE)
    print(f"Crawl xong {len(books)} sách. Đã lưu vào {OUTPUT_FILE}")
