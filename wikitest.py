import pyperclip
import webbrowser
import time
import urllib.parse

def search_web(query):
    print(f"「{query}」を検索しています...")
    try:
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://ja.wikipedia.org/w/index.php?search={encoded_query}"
        webbrowser.open_new_tab(search_url)
        print("検索ページをブラウザで開きました。")
    except Exception as e:
        print(f"エラー: ブラウザの起動に失敗しました: {e}")

def main():
    print("クリップボードの監視を開始しました。")
    print("終了するには 'http' とコピーするか、[Ctrl] + [C] を押してください。")
    print("-" * 50)

    try:
        pyperclip.copy("")
        latest_text = ""
    except pyperclip.PyperclipException:
        print("警告: クリップボードへの初回アクセスに失敗しました。続行します。")
        latest_text = pyperclip.paste()

    try:
        while True:
            try:
                current_text = pyperclip.paste()
                if current_text and current_text != latest_text:
                    latest_text = current_text
                    if latest_text.strip().lower() == "http":
                        print("終了コマンド 'http' を検知しました。プログラムを終了します。")
                        break
                    if len(latest_text) <= 20:
                        search_web(latest_text)
                    else:
                        print("文字数が20文字を超えています")

            except pyperclip.PyperclipException:
                pass

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n" + "-" * 50)
        print("プログラムがユーザーによって中断されました。終了します。")

if __name__ == "__main__":
    main()