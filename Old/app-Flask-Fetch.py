# Flaskバージョン　2026.3.25

from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta, timezone # 現在時刻を取得するためのモジュールを追加

app = Flask(__name__)

# 1. 最初にページを表示するためのルート
@app.route('/') 
def index():
    # templatesフォルダ内のindex.htmlを探してブラウザに返す
    return render_template('index.html')

# 2. フロントエンド（JS）から呼ばれる、データを送るためのルート
@app.route('/api/data')    # /api/data というURLにアクセスがあった時に、下の関数を実行するように設定
def get_data():


    # 1. 日本標準時（JST）のタイムゾーンを設定 (UTCから+9時間)
    jst = timezone(timedelta(hours=9))
    
    # 2. JSTでの現在時刻を取得
    now_jst = datetime.now(jst)
    
    # 3. 指定したフォーマットで文字列に変換
    now_time = now_jst.strftime("%Y-%m-%d %H:%M:%S")

    """
    世界標準時の場合  
    # 1. 現在時刻を取得し、読みやすい文字列フォーマットに変換
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    """

    # 取得した時刻の文字列をJSON形式で返却
    return jsonify({"message": now_time})


    """　単なる文字列データの送信、　AI Studio 「x CSR → Build」で作成したコード
    data = {
        "message": "こんにちは！これはPythonバックエンドから送られたメッセージです。",
        "status": "success"
    }
    return jsonify(data)  # JSON形式でフロントに送信
    """

if __name__ == '__main__':
    app.run(debug=True)