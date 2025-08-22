import pyperclip
import webbrowser
import time
import os
import google.generativeai as genai

API_KEY = "YOUR_API_KEY"

PROMPT_TEMPLATE = """
以下の文章から重要と思われる単語を抽出してください
その単語の意味を誰にでもわかりやすく簡潔に日本語で説明してください

結果は以下のフォーマットで、Markdown形式で入力してください
**抽出した単語**: 意味と解説
---
文章:
{text}
"""

def extract_keywords_and_meanings(text_to_analyze):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = PROMPT_TEMPLATE.format(text=text_to_analyze)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini APIエラー: {e}")
        return f"APIの呼び出し中にエラーが発生しました。 \n{e}"
    
def create_and_open_html(original_text, analysis_result):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        html_template_path = os.path.join(script_dir, "TSA.html")
        with open(html_template_path, "r", encoding="utf-8") as file:
            html_content = file.read()
    except FileNotFoundError:
        print("エラー:　TSA.htmlが見つかりません。")
        return

    html_body = analysis_result.replace('**', '<b>').replace('**', '</b>').replace('\n', '<br>')
    original_text_html = original_text.replace('\n', '<br>')

    html_content = html_content.replace("%%ORIGINAL_TEXT%%", original_text_html)
    html_content = html_content.replace("%%ANALYSIS_RESULT%%", html_body)

    try:
        filepath = os.path.join(script_dir, "analysis_result.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        filepath = os.path.join(script_dir, "analysis_result.html")

        webbrowser.open_new_tab(f"file://{filepath}")
        print(f"-> 結果を {os.path.basename(filepath)}に上書き保存し、ブラウザで開きました")
    
    except Exception as e:
        print(f"HTMLファイルの作成または氷人い失敗しました: {e}")

def main():
    print("クリップボードの監視を開始")
    print("終了するには http とコピーするか、ctrl + C を押してください")
    print("-" * 50)

    latest_text = ""
    try:
        while True:
            current_text = pyperclip.paste()
            if current_text and current_text != latest_text:
                latest_text = current_text

                if latest_text.strip().lower() == "http":
                    break
                
                print(f"新しいテキストをコピーしました")
                analysis_result = extract_keywords_and_meanings(latest_text)

                create_and_open_html(latest_text, analysis_result)

            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nプログラムが中断されました")
    
if __name__ == "__main__":
    if API_KEY == 'YOUR_API_KEY':
        print("エラー: コード上部の API_KEYを自身のGeminiAPIキーに置き換えてください")
    else:
        main()