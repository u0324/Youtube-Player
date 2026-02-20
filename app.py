from flask import Flask, request
import re
import os

app = Flask(__name__)

def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    is_loop_checked = "checked" 
    v_id = ""
    current_url = ""

    if request.method == 'POST':
        if 'delete' in request.form:
            v_id = ""
            current_url = ""
        else:
            current_url = request.form.get('url', '')
            v_id = get_video_id(current_url)
            is_loop_checked = "checked" if "loop" in request.form else ""

    loop_js_flag = "true" if is_loop_checked else "false"

    head = f"""
    <html><head><title>YT-Player</title>
    <style>
        body {{ text-align:center; padding:40px 20px; background:#1a1a1a; color:#eee; font-family: sans-serif; }}
        h1 {{ margin-bottom: 30px; font-weight: 300; letter-spacing: 2px; }}
        .controls {{ margin-top: 30px; background: #2a2a2a; padding: 20px; border-radius: 12px; display: inline-block; }}
        input[type='text'] {{ width:400px; padding:12px; border:none; border-radius:6px; background:#333; color:#fff; margin-bottom: 15px; }}
        button {{ padding:12px 25px; cursor:pointer; border-radius:6px; border:none; font-weight:bold; transition: 0.3s; }}
        .btn-play {{ background:#007bff; color:white; }}
        .btn-delete {{ background:#444; color:#ccc; margin-left:10px; }}
        label {{ cursor: pointer; font-size: 14px; color: #bbb; }}
        #player-wrapper {{ max-width:800px; margin:0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border-radius: 8px; overflow: hidden; background:#000; }}
    </style>
    
    <script src="https://www.youtube.com/iframe_api"></script>
    
    <script>
        let player;
        const videoId = "{v_id}";
        const loopEnabled = {loop_js_flag};

        function onYouTubeIframeAPIReady() {{
            if (!videoId) return;
            player = new YT.Player('main-player', {{
                events: {{
                    'onStateChange': onPlayerStateChange
                }}
            }});
        }}

        function onPlayerStateChange(event) {{
            if (event.data === YT.PlayerState.ENDED && loopEnabled) {{
                player.playVideo();
            }}
        }}

        window.addEventListener('keydown', function(e) {{
            if (!player || typeof player.getPlayerState !== 'function') return;
            if (e.keyCode === 32 || e.keyCode === 75) {{
                if (document.activeElement.tagName === 'INPUT') return;
                e.preventDefault(); 
                const state = player.getPlayerState();
                if (state === 1 || state === 3) {{
                    player.pauseVideo();
                }} else {{
                    player.playVideo();
                }}
            }}
        }});
    </script>
    </head><body>
    """

    if v_id:
        player_content = f"""
        <div id="player-wrapper">
            <iframe id="main-player" 
                    width="100%" height="450" 
                    src="https://www.youtube.com/embed/{v_id}?enablejsapi=1&autoplay=1&rel=0" 
                    frameborder="0" 
                    allow="autoplay; encrypted-media" 
                    allowfullscreen></iframe>
        </div>
        """
    else:
        player_content = "<div style='color:#666;'>URLを入力してPLAYを押してください</div>"
    
    form = f"""
    <div class='controls'>
        <form method='POST' style='margin:0;'>
            <input type='text' name='url' value='{current_url}' placeholder='動画URLをペースト' autocomplete='off'><br>
            <label><input type='checkbox' name='loop' {is_loop_checked}> ループ再生</label>
            <div style='margin-top:15px;'>
                <button type='submit' class='btn-play'>PLAY</button>
                <button type='submit' name='delete' class='btn-delete'>DELETE</button>
            </div>
        </form>
    </div>
    """
    
    return head + "<h1>YT Player</h1>" + player_content + form + "</body></html>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
