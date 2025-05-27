import requests
import json
import time
import config

def crawl_products(page=1):
    url = f"https://tiki.vn/api/personalish/v1/blocks/listings?limit={config.LIMIT}&page={page}&category={config.CATEGORY_ID}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get('data', [])
    except Exception as e:
        print(f"Trang {page} lỗi: {e}")
        return []

def extract_fields(product):
    rating = product.get("rating_average")
    try:
        rating = float(rating) if rating is not None else 0.0
    except (ValueError, TypeError):
        rating = 0.0
    return {
        "title": product.get("name"),
        "price": product.get("price"),
        "rating": rating,
        "url": f"https://tiki.vn/{product.get('url_path')}"
    }

def save_crawled_data():
    total_products = 0

    with open("tiki_book_data.jsonl", "w", encoding="utf-8") as f:
        for page in range(1, config.MAX_PAGE + 1):
            print(f"Đang crawl trang {page}")
            products = crawl_products(page)
            if not products:
                break

            for product in products:
                if total_products >= 1500:
                    break
                item = extract_fields(product)
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                total_products += 1

            if total_products >= 1500:
                break

            time.sleep(1)

    print(f"\nĐã lưu {total_products} sách vào 'tiki_book_data.jsonl'.")

if __name__ == "__main__":
    save_crawled_data()
