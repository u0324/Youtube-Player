from flask import Flask, request
import re

app = Flask(__name__)

def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    player_content = "URLを入力してください"
    if request.method == 'POST':
        v_id = get_video_id(request.form.get('url', ''))
        if v_id:
            # タグを文字列結合で作成（制限回避）
            src_url = f"https://www.youtube.com/embed/{v_id}?playlist={v_id}&loop=1&autoplay=1"
            player_content = f''
        else:
            player_content = "無効なURLです"

    # 最小限の構成を文字列で結合して返す
    head = ""
    title = "LoopTube Player"
    form = ""
    footer = ""
    
    return head + title + player_content + form + footer

if __name__ == '__main__':
    app.run(debug=True)
