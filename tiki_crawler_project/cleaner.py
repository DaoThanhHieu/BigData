import json
import re

INPUT_FILE = "tiki_book_data.jsonl"
OUTPUT_FILE = "tiki_book_data_clean.jsonl"

def clean_price(price):
    if price is None:
        return None
    price_str = re.sub(r"[^\d]", "", str(price))
    if not price_str:
        return None
    return int(price_str)

def clean_rating(rating):
    try:
        r = float(rating)
        if 0 < r <= 5:  # loại bỏ rating = 0
            return r
        else:
            return None
    except:
        return None

def clean_and_deduplicate():
    seen_titles = set()
    clean_data = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                item = json.loads(line)
                title = item.get("title")
                price = clean_price(item.get("price"))
                rating = clean_rating(item.get("rating"))
                url = item.get("url")

                if not title or price is None or rating is None or not url:
                    continue

                if title.lower() in seen_titles:
                    continue
                seen_titles.add(title.lower())

                item["price"] = price
                item["rating"] = rating

                clean_data.append(item)

            except:
                continue

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        for item in clean_data:
            f_out.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"{len(clean_data)} sản phẩm còn lại sau khi làm sạch.")

if __name__ == "__main__":
    clean_and_deduplicate()
