import pymysql
import json
from config import MYSQL_CONFIG  # database: crawl_data_uk

def create_books_uk_table():
    conn = pymysql.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        database=MYSQL_CONFIG["database"],
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books_uk (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) UNIQUE,
            price INT,
            rating FLOAT,
            url TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Đã tạo bảng books_uk")

def save_to_books_uk(data):
    conn = pymysql.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        database=MYSQL_CONFIG["database"],
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO books_uk (title, price, rating, url) 
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            price = VALUES(price),
            rating = VALUES(rating),
            url = VALUES(url)
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
    print(f"Đã lưu {len(data)} bản ghi vào bảng books_uk")

if __name__ == "__main__":
    create_books_uk_table()
    with open("books_clean.jsonl", "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]
    save_to_books_uk(data)
