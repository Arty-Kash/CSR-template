from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 1. 最初にページを表示するためのルート
@app.route('/')
def index():
    return render_template('index.html')

# 2. フロントエンド（JS）から呼ばれる、データを送るためのルート
@app.route('/api/data')
def get_data():
    # バックエンドで生成した固定のデータ
    data = {
        "message": "こんにちは！これはPythonバックエンドから送られたメッセージです。あああ",
        "status": "success"
    }
    return jsonify(data)  # JSON形式でフロントに送信

if __name__ == '__main__':
    app.run(debug=True)