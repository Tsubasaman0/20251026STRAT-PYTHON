# AI会議室（AI Roundtable）

同じ質問をOpenAI・Gemini・Claudeなど複数のAIへ送り、回答を比較・要約して、人間の意思決定を支援するWebアプリです。将来はAI同士のレビューと議論を扱う「AI会議室OS」、役割別AIが協働する「AI社員株式会社」、意思決定支援プラットフォームへの発展を構想しています。

AIは最終決定者ではありません。異なる視点、根拠、不確実性を整理し、人間が判断するための材料を提供します。詳しくは [VISION](docs/VISION.md) と [AI憲章](docs/AI_CHARTER.md) を参照してください。

## 現在の開発段階

MVPの第1段階です。質問フォーム、FastAPIへの送信、入力内容をそのまま返すAPI、基本的な入力・通信エラー表示を実装済みです。外部AI APIへの接続、回答比較、コスト計算、データ保存は未実装です。

現在の次タスクは、OpenAI APIをサービス層へ接続し、タイムアウト・失敗表示・モックテストを追加することです。[ロードマップ](docs/ROADMAP.md) に従い、1社ずつ安全に接続します。

## MVP

- 質問入力とFastAPIへの送信
- OpenAI、Gemini、Claudeへの接続
- 3つの回答と部分的な失敗状態の表示
- 回答の比較・要約
- 最低限のエラー処理
- 質問単位の利用料金概算

完成条件は [ROADMAP](docs/ROADMAP.md)、詳細な振る舞いは [SPECIFICATION](docs/SPECIFICATION.md) を正本とします。

## 主な使用技術

- Backend: Python、FastAPI、Pydantic
- Frontend: HTML、CSS、JavaScript、Jinja2
- Server: Uvicorn
- Test: pytest、FastAPI TestClient
- AI APIs（計画）: OpenAI、Gemini、Claude
- Version control: Git、GitHub

MVPでは必要以上に大きなフレームワークを追加しません。

## セットアップと起動

Python 3.11以上を推奨します。

```bash
cd portfolio/ai-roundtable
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

- Web画面: <http://127.0.0.1:8000>
- APIドキュメント: <http://127.0.0.1:8000/docs>
- テスト: `python -m pytest tests`

## セキュリティ上の注意

APIキーはプロジェクト直下の `.env` で管理し、コード、ブラウザ、ログ、Gitへ含めないでください。`.env` は `.gitignore` の対象です。本番では環境変数または秘密情報管理サービスを使用します。詳しくは [SECURITY](docs/SECURITY.md) を参照してください。

## ディレクトリ概要

```text
ai-roundtable/
├── app/          # FastAPI、APIモデル、将来のAIサービス
├── static/       # CSS、ブラウザJavaScript
├── templates/    # Jinja2 HTML
├── tests/        # 自動テスト
├── docs/         # 長期運用向け文書
└── README.md     # プロジェクトの入口
```

詳細は [ARCHITECTURE](docs/ARCHITECTURE.md) を参照してください。

## ドキュメント一覧

| 分類 | ドキュメント | 正本とする内容 |
| --- | --- | --- |
| 理念 | [VISION](docs/VISION.md) | 目的、価値、1・5・10年後の方向 |
| 理念 | [AI_CHARTER](docs/AI_CHARTER.md) | 人間中心の倫理原則 |
| 計画 | [ROADMAP](docs/ROADMAP.md) | 優先順位、段階、完了条件 |
| 仕様 | [SPECIFICATION](docs/SPECIFICATION.md) | 現在・MVP・将来の機能仕様 |
| 設計 | [ARCHITECTURE](docs/ARCHITECTURE.md) | 構成、責務、技術方針 |
| 開発 | [CONTRIBUTING](docs/CONTRIBUTING.md) | 人間向け開発・Git・レビュー規則 |
| 開発 | [AI_GUIDE](docs/AI_GUIDE.md) | AI開発者向け実務規則 |
| 安全 | [SECURITY](docs/SECURITY.md) | 秘密情報、入力、公開前確認 |
| コスト | [COST_MANAGEMENT](docs/COST_MANAGEMENT.md) | 計測、予算、価格改定対応 |
| 発展 | [DEBATE_SYSTEM](docs/DEBATE_SYSTEM.md) | AIディベートの将来仕様 |
| 発展 | [PLUGIN_SYSTEM](docs/PLUGIN_SYSTEM.md) | AI・外部機能の追加境界 |
| AI運用 | [PROMPTS](docs/PROMPTS.md) | プロンプトの管理・評価方針 |
| AI運用 | [MODELS](docs/MODELS.md) | モデル選択と更新可能な管理表 |
| 品質 | [BENCHMARK](docs/BENCHMARK.md) | AI品質・速度・費用の評価計画 |
| 判断 | [DECISIONS](docs/DECISIONS.md) | 設計判断と見直し条件 |
| アイデア | [FUTURE_IDEAS](docs/FUTURE_IDEAS.md) | 未確定案の隔離場所 |
| 履歴 | [CHANGELOG](docs/CHANGELOG.md) | 実際に行った変更 |

文書間で重複した場合はこの表の「正本」を更新し、他文書からリンクしてください。実装済みの振る舞いはコードとテスト、目標仕様は `SPECIFICATION.md` を基準にします。
