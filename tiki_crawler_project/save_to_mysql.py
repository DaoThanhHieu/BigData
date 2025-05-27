import pymysql
import json
from config import MYSQL_CONFIG 
INPUT_FILE = "tiki_book_data_clean.jsonl"

def create_books_tiki_table():
    conn = pymysql.connect(
        host=MYSQL_CONFIG["host"],  
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        database=MYSQL_CONFIG["database"],
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books_tiki (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title TEXT,
            price INT,
            rating FLOAT,
            url TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Đã tạo bảng books_tiki")

def load_jsonl(filepath):
    items = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            try:
                items.append(json.loads(line))
            except:
                pass
    return items

def save_to_books_tiki(data):
    conn = pymysql.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        database=MYSQL_CONFIG["database"],
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO books_tiki (title, price, rating, url)
        VALUES (%s, %s, %s, %s)
    """

    for item in data:
        cursor.execute(insert_query, (
            item.get("title"),
            item.get("price"),
            item.get("rating"),
            item.get("url")
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Đã lưu {len(data)} dòng vào bảng books_tiki")

if __name__ == "__main__":
    create_books_tiki_table()
    data = load_jsonl(INPUT_FILE)
    save_to_books_tiki(data)
