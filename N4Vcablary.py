import csv
import random
import tkinter as tk
from tkinter import messagebox

class SequentialFlashcardApp:
    def __init__(self, root, file_path):
        self.root = root
        self.root.title("JLPT N4 語彙 フラッシュカード")
        
        # データの読み込み
        self.rows = self.load_data(file_path)
        if not self.rows:
            messagebox.showerror("エラー", "データを読み込めませんでした。")
            self.root.destroy()
            return
            
        random.shuffle(self.rows)  # ランダムにシャッフル
        self.row_index = 0
        self.step = 0  # 0: 漢字, 1: 見出し語, 2: 例文, 3: クリア画面
        self.total = len(self.rows)

        # ウィンドウサイズを設定し画面中央に配置 (900x650)
        self.center_window(900, 650)
        
        # UIの構築
        self.create_widgets()
        
        # 最初の有効な表示までセットアップ
        self.show_step()

    def center_window(self, width, height):
        """ウィンドウを画面の中央に配置する"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_data(self, file_path):
        """CSVファイルを読み込む"""
        try:
            with open(file_path, mode='r', encoding='cp932') as f:
                reader = csv.reader(f)
                next(reader)  # ヘッダー行をスキップ
                # [見出し語(col1), 漢字表記(col2), 例文(col3)]
                return [[row[1].strip(), row[2].strip(), row[3].strip()] for row in reader if len(row) >= 4]
        except Exception as e:
            print(f"ファイル読み込みエラー: {e}")
            return []

    def create_widgets(self):
        """画面パーツのレイアウト作成"""
        # 上部：進行状況表示
        self.progress_label = tk.Label(self.root, text="", font=("Helvetica", 14), fg="gray")
        self.progress_label.pack(pady=(15, 5))

        # 中央：メイン表示エリア（クリック可能）
        self.card_frame = tk.Frame(self.root, bd=2, relief="groove", bg="#ffffff", cursor="hand2")
        self.card_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # 項目ラベル（「漢字」「見出し語」「例文」）
        self.category_label = tk.Label(
            self.card_frame, text="", font=("Helvetica", 16, "bold"), 
            bg="#ffffff", fg="#888888"
        )
        self.category_label.pack(pady=(20, 0))

        # 48pt メイン表示ラベル
        self.main_label = tk.Label(
            self.card_frame, text="", font=("Helvetica", 48, "bold"), 
            bg="#ffffff", fg="#1a0dab", wraplength=800, justify="center"
        )
        self.main_label.pack(expand=True, fill="both", padx=20, pady=20)

        # 下部：ボタンを並べるフレーム
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=(5, 20))

        # 戻るボタン
        self.btn_prev = tk.Button(
            btn_frame, text="◀ 戻る (← / b)", font=("Helvetica", 14, "bold"), 
            bg="#757575", fg="white", padx=15, pady=10, command=self.prev_action
        )
        self.btn_prev.pack(side="left", padx=10)

        # 次へボタン
        self.btn_next = tk.Button(
            btn_frame, text="進む (Space / Enter / クリック) ▶", font=("Helvetica", 14, "bold"), 
            bg="#4CAF50", fg="white", padx=20, pady=10, command=self.next_action
        )
        self.btn_next.pack(side="left", padx=10)

        # クリック／キーボードバインド
        self.card_frame.bind("<Button-1>", lambda event: self.next_action())
        self.main_label.bind("<Button-1>", lambda event: self.next_action())
        self.category_label.bind("<Button-1>", lambda event: self.next_action())
        
        # 進む操作（Space / Enter）
        self.root.bind("<space>", lambda event: self.next_action())
        self.root.bind("<Return>", lambda event: self.next_action())
        
        # 戻る操作（Left矢印キー / bキー）
        self.root.bind("<Left>", lambda event: self.prev_action())
        self.root.bind("<b>", lambda event: self.prev_action())

    def next_action(self):
        """進む（データがないステップは自動スキップ）"""
        if self.row_index >= self.total:
            return

        while True:
            self.step += 1
            if self.step > 3:  # クリア画面の次は次の行へ
                self.step = 0
                self.row_index += 1

            if self.row_index >= self.total:
                break

            row = self.rows[self.row_index]
            midashi, kanji, reibun = row[0], row[1], row[2]

            if self.step == 0 and kanji:
                break
            elif self.step == 1 and midashi:
                break
            elif self.step == 2 and reibun:
                break
            elif self.step == 3:
                break

        if self.row_index < self.total:
            self.show_step()
        else:
            self.category_label.config(text="")
            self.main_label.config(text="すべての行を表示しました！", font=("Helvetica", 36, "bold"), fg="#333333")
            self.progress_label.config(text=f"[{self.total} / {self.total}]")
            self.btn_next.config(state="disabled", text="表示完了")

    def prev_action(self):
        """戻る（データがないステップは自動スキップ）"""
        # 一番最初（1件目のステップ0）の場合は戻らない
        if self.row_index == 0 and self.step == 0:
            return

        # 表示完了後の復帰処理
        if self.row_index >= self.total:
            self.btn_next.config(state="normal", text="進む (Space / Enter / クリック) ▶")

        while True:
            self.step -= 1
            if self.step < 0:  # 漢字の前のステップは「前の行のクリア画面」へ
                self.step = 3
                self.row_index -= 1

            if self.row_index < 0:
                self.row_index = 0
                self.step = 0
                break

            row = self.rows[self.row_index]
            midashi, kanji, reibun = row[0], row[1], row[2]

            if self.step == 0 and kanji:
                break
            elif self.step == 1 and midashi:
                break
            elif self.step == 2 and reibun:
                break
            elif self.step == 3:
                break

        self.show_step()

    def show_step(self):
        """現在のステップに応じてカードを表示"""
        row = self.rows[self.row_index]
        midashi, kanji, reibun = row[0], row[1], row[2]

        self.progress_label.config(text=f"[{self.row_index + 1} / {self.total}]")

        if self.step == 0:
            # 3列目（漢字表記）
            self.category_label.config(text="【 漢字 】")
            self.main_label.config(text=kanji, fg="#2c3e50", font=("Helvetica", 48, "bold"))

        elif self.step == 1:
            # 2列目（見出し語／読み）
            self.category_label.config(text="【 見出し語（読み） 】")
            self.main_label.config(text=midashi, fg="#1a0dab", font=("Helvetica", 48, "bold"))

        elif self.step == 2:
            # 4列目（例文）
            self.category_label.config(text="【 例文 】")
            self.main_label.config(text=reibun, fg="#d35400", font=("Helvetica", 36 if len(reibun) > 20 else 48, "bold"))

        elif self.step == 3:
            # 画面クリア
            self.category_label.config(text="")
            self.main_label.config(text="")

if __name__ == "__main__":
    file_name = 'JLPT N4 語彙.csv'
    root = tk.Tk()
    app = SequentialFlashcardApp(root, file_name)
    root.mainloop()
