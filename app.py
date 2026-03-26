# Flask & FastAPI バージョン　2026.4.

# Flask
# from flask import Flask, render_template, jsonify

# Fast API
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

# SSE
from fastapi.responses import StreamingResponse
import asyncio  # 非同期処理のためのモジュール

# 現在時刻を取得するためのモジュール
from datetime import datetime, timedelta, timezone


# Flask
# app = Flask(__name__)

# FastAPI
app = FastAPI()


# 1. 最初にページを表示するためのルート

# Flask
# @app.route('/') 

# Fast API
@app.get("/")

def index():
    # Flask: templatesフォルダ内のindex.htmlを探してブラウザに返す
    # return render_template('index.html')

    # FastAPI
    # Flaskの render_template はHTMLの中身を書き換える（レンダリングする）機能があるが、
    # FastAPIで単純なHTMLファイルを送る場合は FileResponse を使うのが手軽
    return FileResponse('templates/index.html')


# SSE用のジェネレータ関数（サーバーからデータを送り続ける仕組み）
async def event_generator():
    while True:
        # 1. 日本標準時（JST）の時刻取得
        jst = timezone(timedelta(hours=9))
        now_time = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
        
        # 2. SSEの形式（"data: メッセージ\n\n"）でデータを送信
        yield f"data: {now_time}\n\n"
        
        # 3. 1秒待機
        await asyncio.sleep(1)

# フロントエンド（JS）から呼ばれる、データを送るためのルート
# Flask
# @app.route('/api/data')    # /api/data というURLにアクセスがあった時に、下の関数を実行するように設定

# FastAPI: FastAPIでは、GETメソッドであることを明示的に書くのが一般的
@app.get("/api/data")
async def get_data():
    # StreamingResponseを使い、media_typeを "text/event-stream" に設定することでSSEとして動作させる
    return StreamingResponse(event_generator(), media_type="text/event-stream")


""" Fetchの場合
@app.get("/api/data")
def get_data():
    # 1. 日本標準時（JST）のタイムゾーンを設定 (UTCから+9時間)
    jst = timezone(timedelta(hours=9))
    
    # 2. JSTでの現在時刻を取得
    now_jst = datetime.now(jst)
    
    # 3. 指定したフォーマットで文字列に変換
    now_time = now_jst.strftime("%Y-%m-%d %H:%M:%S")


    # 世界標準時の場合  
    # 1. 現在時刻を取得し、読みやすい文字列フォーマットに変換
    # now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    # 取得した時刻の文字列をJSON形式で返却
    # Flask
    # return jsonify({"message": now_time})
    
    # FastAPI  FastAPIでは辞書型を返すと自動的にJSONに変換されます
    return {"message": now_time}
"""

"""
    単なる文字列データの送信
    data = {
        "message": "こんにちは！これはPythonバックエンドから送られたメッセージです。",
        "status": "success"
    }
    return jsonify(data)  # JSON形式でフロントに送信
"""

if __name__ == '__main__':
    # サーバを起動
    # Flask     app.run(debug=True)
    # FastAPI
    # FastAPI単体ではサーバー機能を持たないため、uvicorn という高速なサーバーソフトを使って起動。
    # ポート番号を 5000(defaultは8000) に設定することで、Flaskの時と同じURLでアクセスできるようにしています。
    uvicorn.run(app, host="0.0.0.0", port=5000)
    