from flask import Flask, request
import re

app = Flask(__name__)

# YouTubeのURLから動画ID（v=xxxxの部分）を抜き出す関数
def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    video_id = ""
    player_html = ""

    # ユーザーがURLを送信した場合
    if request.method == 'POST':
        url = request.form.get('url')
        video_id = get_video_id(url)
        if video_id:
            # ここでHTML構造を直接作成（ループ再生用パラメータ付き）
            player_html = f'''
            
                
            
            '''
        else:
            player_html = '有効なURLを入力してください'

    # ブラウザに表示する画面全体（HTML）を文字列として返す
    return f'''
    
    
    
        
        
        
        
    
    
        
            LoopTube Player
            {player_html}
            
            ※再生が始まったら右クリックで「ループ」を選択するか、自動ループ設定を読み込みます
        
    
    
    '''

if __name__ == '__main__':
    app.run(debug=True)
