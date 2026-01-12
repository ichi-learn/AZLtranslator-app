# 翻訳アプリ

これは、Azure Functions を使用してテキストを翻訳する簡単なアプリケーションです。

## 機能

- HTTPリクエストを介してテキストを受け取ります。
- Microsoft Translator API を使用して、指定された言語にテキストを翻訳します。
- 翻訳されたテキストをHTTPレスポンスで返します。

## セットアップ

1. `local.settings.json` ファイルに、Microsoft Translator API のキー、エンドポイント、およびリージョンを設定します。
2. `pip install -r requirements.txt` を実行して、必要なライブラリをインストールします。
3. `func start` を実行して、ローカルで関数アプリを起動します。