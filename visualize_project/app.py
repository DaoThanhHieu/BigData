import json
import pandas as pd
from flask import Flask, render_template
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

def load_jsonl(filepath):
    data = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except:
                pass
    return data

def prepare_data(filepath):
    data = load_jsonl(filepath)
    df = pd.DataFrame(data)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    # Lọc dữ liệu hợp lệ
    df = df[(df['price'] > 0) & (df['rating'] >= 0) & (df['rating'] <= 5)]
    return df

def plot_to_img(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return img
    
@app.route("/", methods=["GET", "POST"])
def index():
    tiki_df = prepare_data("data/tiki_book_data_clean.jsonl")
    uk_df = prepare_data("data/books_clean.jsonl")

    plots = {}

    # Biểu đồ 1: Phân bố giá sách
    plt.figure(figsize=(10, 5))
    sns.histplot(tiki_df['price'], bins=30, label='Tiki', color='skyblue', alpha=0.6)
    sns.histplot(uk_df['price'], bins=30, label='UK', color='orange', alpha=0.6)
    plt.title("Phân bố giá sách")
    plt.xlabel("Giá sách (VNĐ)")
    plt.ylabel("Số lượng")
    plt.legend()
    plots['price_distribution'] = plot_to_img(plt)

    # Biểu đồ 2: Số lượng sách theo điểm đánh giá (đã sắp xếp rating tăng dần)
    plt.figure(figsize=(10, 5))
    rating_order = sorted(tiki_df['rating'].dropna().unique())
    sns.countplot(x='rating', data=tiki_df, color='skyblue', alpha=0.6, label='Tiki', order=rating_order)
    sns.countplot(x='rating', data=uk_df, color='orange', alpha=0.6, label='UK', order=rating_order)
    plt.title("Số lượng sách theo điểm đánh giá")
    plt.xlabel("Điểm đánh giá (0 - 5)") 
    plt.ylabel("Số lượng sách")
    plt.legend()
    plots['rating_count'] = plot_to_img(plt)

    # Biểu đồ 3: Biểu đồ tròn so sánh số lượng sách theo nguồn
    plt.figure(figsize=(6,6))
    counts = {'Tiki': len(tiki_df), 'UK': len(uk_df)}
    labels = list(counts.keys())
    sizes = list(counts.values())
    colors = ['skyblue', 'orange']
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title("Tỉ lệ số lượng sách theo nguồn")
    plots['source_pie'] = plot_to_img(plt)

    return render_template("index.html", plots=plots)

if __name__ == "__main__":
    app.run(debug=True)
