from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    video_id = "uQpKzPCBqc4"
    start = 0.5
    end = 20.0
    return render_template('index.html', video_id=video_id, start=start, end=end)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
