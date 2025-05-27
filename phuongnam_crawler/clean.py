import json
import re

INPUT_FILE = "books_raw.jsonl"
OUTPUT_FILE = "books_clean.jsonl"
EXCHANGE_RATE = 30000  # 1£ = 30,000 VNĐ

def clean_price(price_raw):
    if price_raw is None:
        return None
    price_str = str(price_raw).replace("Â£", "£").strip()
    numeric_part = re.sub(r"[^\d.]", "", price_str)
    try:
        gbp_value = float(numeric_part) if numeric_part else None
        if gbp_value is not None:
            vnd_value = int(gbp_value * EXCHANGE_RATE)
            return vnd_value
        else:
            return None
    except ValueError:
        return None

def clean_rating(rating_raw):
    rating_map = {
        "One": 1.0,
        "Two": 2.0,
        "Three": 3.0,
        "Four": 4.0,
        "Five": 5.0
    }
    if isinstance(rating_raw, str):
        return rating_map.get(rating_raw.strip(), 0.0)
    try:
        return float(rating_raw)
    except:
        return 0.0

def clean_book(book):
    title = book.get("title")
    price_raw = book.get("price")
    rating_raw = book.get("rating")
    url = book.get("url")

    if not title or not price_raw or not url:
        return None

    price_cleaned = clean_price(price_raw)
    rating_cleaned = clean_rating(rating_raw)

    if price_cleaned is None or rating_cleaned == 0.0:
        return None  # Bỏ sách không có giá hoặc rating = 0

    cleaned = dict(book)
    cleaned["price"] = price_cleaned
    cleaned["rating"] = rating_cleaned
    cleaned["title"] = title.strip()

    return cleaned

def load_jsonl(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                print("Bo qua dong loi: ", line)
    return data

def save_jsonl(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def clean_and_deduplicate():
    raw_data = load_jsonl(INPUT_FILE)
    seen_titles = set()
    cleaned = []

    for book in raw_data:
        cleaned_book = clean_book(book)
        if cleaned_book is None:
            continue

        title_lower = cleaned_book["title"].lower()
        if title_lower in seen_titles:
            print("Bo trung lap: ", cleaned_book['title'])
            continue
        seen_titles.add(title_lower)

        cleaned.append(cleaned_book)

    save_jsonl(cleaned, OUTPUT_FILE)
    print("\nDa clean va luu", len(cleaned), "sach vao", OUTPUT_FILE)

if __name__ == "__main__":
    clean_and_deduplicate()
