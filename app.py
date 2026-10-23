from flask import Flask, render_template_string
import csv
import random
import os

app = Flask(__name__)

# CSVファイルからデータを読み込む関数
def load_vocabulary():
    rows = []
    file_path = "JLPT N4 語彙.csv"
    if os.path.exists(file_path):
        with open(file_path, mode="r", encoding="cp932") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    rows.append(row)
    return rows

@app.route("/")
def index():
    rows = load_vocabulary()
    if not rows:
        return "<h1>エラー: 語彙データが見つかりません。</h1>"
    
    # ランダムに1つ選ぶ（または全表示など）
    item = random.choice(rows)
    word = item[0] if len(item) > 0 else ""
    meaning = item[1] if len(item) > 1 else ""

    html = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>JLPT N4 語彙 フラッシュカード</title>
        <style>
            body {{ font-family: sans-serif; text-align: center; margin-top: 100px; background-color: #f4f4f9; }}
            .card {{ background: white; padding: 40px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            h1 {{ font-size: 48px; color: #333; }}
            p {{ font-size: 24px; color: #666; }}
            button {{ padding: 10px 20px; font-size: 18px; cursor: pointer; background: #007BFF; color: white; border: none; border-radius: 5px; }}
            button:hover {{ background: #0056b3; }}
        </style>
    </head>
    <body>
        <div class="card">
            <p>JLPT N4 語彙</p>
            <h1>{word}</h1>
            <p>意味: {meaning}</p>
            <br>
            <button onclick="location.reload()">次の単語へ</button>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)