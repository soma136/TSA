import tkinter as tk
from tkinter import scrolledtext
import pyperclip
import google.generativeai as genai
import threading
import time
import os

# --- 設定項目 ---
# 1. Gemini APIキーを設定してください
#    下の 'YOUR_API_KEY' をご自身のAPIキーに書き換えてください。
#    参考: https://ai.google.dev/gemini-api/docs/api-key?hl=ja
API_KEY = 'YOUR_API_KEY'

# 2. Geminiに送るプロンプト（指示文）を編集できます
PROMPT_TEMPLATE = """以下の単語もしくは文章について、初心者にも分かるように簡潔に説明してください。

{text}
"""

# --- アプリケーション本体 ---

class ClipboardSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("簡易検索")
        # ウィンドウの初期サイズと位置
        self.root.geometry("400x250+100+100")
        # 常に最前面に表示
        self.root.wm_attributes("-topmost", 1)

        # 結果表示用のテキストエリアを作成
        self.result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Meiryo UI", 10))
        self.result_text.pack(expand=True, fill='both', padx=10, pady=10)
        self.result_text.insert(tk.END, "テキストをコピーすると、ここに意味が表示されます。")
        self.result_text.config(state='disabled') # 編集不可にする

    def update_result(self, text):
        """ウィンドウのテキストを更新する"""
        self.result_text.config(state='normal') # 編集可能にする
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state='disabled') # 再び編集不可にする

def search_with_gemini(api_key, text_to_search):
    """Gemini APIを使ってテキストの意味を調べる"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        prompt = PROMPT_TEMPLATE.format(text=text_to_search)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini APIエラー: {e}")
        return "エラーが発生しました。APIキーが正しいか、インターネット接続を確認してください。"

def clipboard_monitor(app):
    """クリップボードを監視し、変更があれば検索を実行する"""
    latest_text = pyperclip.paste()
    while True:
        try:
            pasted_text = pyperclip.paste()
            if pasted_text and pasted_text != latest_text:
                latest_text = pasted_text
                print(f"新しいクリップボードの内容: {latest_text}")

                # 検索中は「検索中...」と表示
                app.update_result("検索中...")
                
                # Geminiで検索を実行し、結果をウィンドウに表示
                result = search_with_gemini(API_KEY, latest_text)
                app.update_result(result)

        except pyperclip.PyperclipException:
            print("クリップボードへのアクセスに失敗しました。")
            time.sleep(2) # エラー時は少し長めに待つ
        
        time.sleep(1) # 1秒ごとにチェック

if __name__ == "__main__":
    if API_KEY == 'YOUR_API_KEY':
        print("エラー: コード内の 'YOUR_API_KEY' をご自身のGemini APIキーに書き換えてください。")
    else:
        # GUIウィンドウを作成
        root_window = tk.Tk()
        app = ClipboardSearchApp(root_window)

        # クリップボード監視を別のスレッドで開始
        # daemon=Trueにすることで、メインウィンドウを閉じたら監視スレッドも終了する
        monitor_thread = threading.Thread(target=clipboard_monitor, args=(app,), daemon=True)
        monitor_thread.start()

        # GUIのメインループを開始
        root_window.mainloop()