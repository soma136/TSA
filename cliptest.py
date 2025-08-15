import time
import pyperclip

pyperclip.copy("")
latest_text = ""

while True:    
    try:
        text = str(pyperclip.paste())
        
        if text != latest_text:
            latest_text = text

            if latest_text.strip() == "":
                pass
            else:
                print(f"新しいクリップボードの内容:{latest_text}")
        
        if latest_text.strip().lower() == "http":
            print("exit")
            break

    except pyperclip.PyperclipException as e:
        print(f"クリップボードへのアクセスエラー")
    except Exception as e:
        print(f"予期しないエラー: {e}")
    time.sleep(1)