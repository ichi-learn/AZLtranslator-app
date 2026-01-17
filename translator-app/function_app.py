import azure.functions as func
import requests, os, uuid
import json
import logging

# アプリ全体の認証レベルを匿名に設定
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="translate", methods=["GET", "POST"])
def translate_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 1. 環境変数から設定を読み込む
    api_key = os.environ.get("TRANSLATOR_KEY")
    endpoint = os.environ.get("TRANSLATOR_ENDPOINT")
    region = os.environ.get("TRANSLATOR_REGION")

    if not all([api_key, endpoint, region]):
        logging.error("不足している環境変数: TRANSLATOR_KEY, TRANSLATOR_ENDPOINT, or TRANSLATOR_REGION")
        return func.HttpResponse(
             "サーバー内部エラー。設定が不足しています。",
             status_code=500
        )

    # 2. リクエストから翻訳したい文字を取得 (GETとPOSTの両対応)
    text_to_translate = req.params.get('text')
    if not text_to_translate:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            text_to_translate = req_body.get('text')

    if not text_to_translate:
        return func.HttpResponse(
             "クエリ文字列かリクエストボディに 'text' パラメータを渡してください。",
             status_code=400
        )

    # 3. Translator APIへのリクエスト作成
    path = '/translate?api-version=3.0&from=en&to=ja'
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{'text': text_to_translate}]

    # 4. 実行とエラーハンドリング
    try:
        response = requests.post(endpoint + path, headers=headers, json=body)
        response.raise_for_status() # HTTPエラーがあれば例外を発生
    except requests.exceptions.RequestException as e:
        logging.error(f"Translator APIへのリクエストが失敗しました: {e}")
        return func.HttpResponse(f"翻訳サービスの呼び出しでエラーが発生しました: {e}", status_code=500)

    # 5. 結果の処理とエラーハンドリング
    try:
        result = response.json()
        translated = result[0]['translations'][0]['text']
        return func.HttpResponse(f"【翻訳結果】: {translated}")
    except (IndexError, KeyError, TypeError) as e:
        logging.error(f"Translator APIからのレスポンス解析に失敗しました: {e}")
        logging.error(f"レスポンスボディ: {response.text}")
        return func.HttpResponse("翻訳サービスからのレスポンス解析でエラーが発生しました。", status_code=500)
