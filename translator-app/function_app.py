import azure.functions as func
import requests, os, uuid
import json

app = func.FunctionApp()

@app.route(route="translate", auth_level=func.AuthLevel.ANONYMOUS)
def translate_function(req: func.HttpRequest) -> func.HttpResponse:
    # 1. 環境変数から設定を読み込む（AZ-204の重要ポイント）
    # ※後でAzureポータルの「環境変数」に同じ名前で登録します
    api_key = os.environ.get("TRANSLATOR_KEY")
    endpoint = os.environ.get("TRANSLATOR_ENDPOINT")
    region = os.environ.get("TRANSLATOR_REGION")

    # 2. リクエストから翻訳したい文字を取得
    text_to_translate = req.params.get('text')
    if not text_to_translate:
        return func.HttpResponse("textパラメータに翻訳したい文字を入れてください", status_code=400)

    # 3. Translator APIへのリクエスト作成
    path = '/translate?api-version=3.0&from=en&to=ja'
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{'text': text_to_translate}]

    # 4. 実行
    response = requests.post(endpoint + path, headers=headers, json=body)
    
    if response.status_code == 200:
        result = response.json()
        translated = result[0]['translations'][0]['text']
        return func.HttpResponse(f"【翻訳結果】: {translated}")
    else:
        return func.HttpResponse(f"エラーが発生しました: {response.text}", status_code=500)
        