# アーキテクチャ

## 現在と将来の構成

```text
Browser (HTML / CSS / JavaScript)
              ↓ JSON
FastAPI routes + Pydantic validation
              ↓
Application orchestration（MVP予定）
   ├── AI provider adapters → OpenAI / Gemini / Claude
   ├── comparison / synthesis
   ├── cost calculation
   └── storage（必要時）
              ↓
Debate orchestration（将来）
```

現在はブラウザ、FastAPIルート、入力モデルまで実装済みです。図のそれ以外は計画であり、必要になる段階で追加します。

## 層の責務

- フロントエンド: 入力、進行状態、回答、比較、エラーの表示。APIキーを扱わない
- FastAPI: HTTP変換、検証、認証・認可の境界。業務ロジックを抱えない
- AIプロバイダー層: SDK、認証、リクエスト、レスポンス、利用量、エラーの差を吸収
- 比較・要約層: 共通内部モデルの回答だけを受け、比較結果を生成
- コスト計算層: モデルと利用量を価格表へ照合。詳細は [COST_MANAGEMENT](COST_MANAGEMENT.md)
- データ保存層: 履歴要件が確定してから導入し、保存期間と削除を管理
- ディベート層: ラウンド、役割、停止条件、予算を調停。詳細は [DEBATE_SYSTEM](DEBATE_SYSTEM.md)

## ディレクトリ構成

```text
ai-roundtable/
├── app/
│   ├── api/          # HTTPルート
│   ├── models/       # Pydantic境界モデル
│   ├── services/     # AI呼び出し・ユースケース
│   ├── prompts/      # 将来のプロンプト本体
│   ├── config.py     # 環境変数設定
│   └── main.py       # アプリ生成
├── static/           # CSS・ブラウザJavaScript
├── templates/        # Jinja2 HTML
├── tests/            # 自動テスト
├── docs/             # 正本文書
└── README.md
```

`repositories/`、`domain/`、ジョブキュー、データベースは必要性が確認されてから追加します。

## 採用技術

FastAPI、Pydantic、Jinja2、HTML、CSS、JavaScript、Uvicorn、pytestを基本とします。MVPではフロントエンドの大型フレームワークを追加しません。新規依存は解決する課題と代替案を [CONTRIBUTING](CONTRIBUTING.md) に従って説明します。

## 設計方針

- 各社固有データを共通の内部リクエスト・レスポンスへ変換する
- モデルID、価格、利用可否をコードへ散在させず設定で管理する
- 外部クライアントを差し替え、API課金なしでテストできるようにする
- 1社の障害を全体障害にせず、部分成功を状態として扱う
- プロンプトとモデル設定にバージョンを持たせる
- まず単一AIで境界を確認し、3社対応で実証された共通点だけを抽象化する
- DRY、KISS、YAGNI、単一責任を規模に応じて適用する

プロバイダー追加方針は [PLUGIN_SYSTEM](PLUGIN_SYSTEM.md)、判断履歴は [DECISIONS](DECISIONS.md) を正本とします。

## セキュリティ方針

秘密情報はサーバー側の環境変数、本番の秘密情報管理サービスから読みます。入力・AI出力を信用せず、タイムアウト、利用上限、最小権限、安全な描画、ログの秘匿化を実施します。詳細な確認事項は [SECURITY](SECURITY.md) を正本とします。
