# Brandri 記事パイプライン

> **現在の運用モード：案B（Pro執筆・Slack投稿のみ自動化）**
> 記事の選定・執筆はClaude Code/チャットで行い、Anthropic APIは使わない（課金なし）。
> GitHub Actionsも使わない。手順は `docs/runbook-planB.md` を参照。
> API完全無人化（案C）の資材は `legacy/` に退避してある。


デイリーのトレンドサマリから週1本を選び、Highlite視点の記事に仕立て、
Slackレビューを経て brandri.jp に公開する。**GitHub Actions で無人運用**する。

## アーキテクチャ

```
GitHub Actions (cron)                     判断が要る部分だけ Anthropic API
 ├─ brandri-generate  水 09:00 JST         選定スコアリング → 執筆
 ├─ brandri-sync      毎日 3回              （改稿のみ）
 └─ brandri-publish   木 10:00 JST

決定論的な処理（Python・トークン不要）
 ├─ Slack入出力（投稿・リアクション・スレッド）
 ├─ 状態判定（reactions/comments → status）
 ├─ スケジューリング・キャンセル検知
 └─ ファイル移動・front matter更新
```

真実の源は GitHub の md ファイル。Slackは通知と承認のインターフェース。
状態は各記事の front matter（`status` / `slack.ts` / `schedule`）と
ディレクトリ（drafts/scheduled/published/dropped）で表現する。

## 週次サイクル

| 曜日 | ワークフロー | 内容 |
|---|---|---|
| 水 | brandri-generate | 直近7日から1本選定 → 執筆 → Slack投稿 |
| 毎日 | brandri-sync | リアクション同期・改稿・予約・キャンセル検知 |
| 木 | brandri-publish | 最終確認 → 公開 |

投稿の8日後（`publish_lead_days`）の木曜が公開日。
定常運用では毎週水曜に1本出て、翌週木曜に1本公開される。

## ファイル構成

```
scripts/brandri/
  config.py       設定ロード
  slack.py        Slack Web API クライアント（bot token）
  state.py        状態判定（決定論・LLM不使用）★テスト済み
  llm.py          Anthropic API（選定・執筆・改稿）
  articles.py     front matter 読み書き・ディレクトリ移動
  generate.py     水: 選定→執筆→投稿
  sync.py         毎日: 状態同期
  publish.py      木: 公開
.github/workflows/
  brandri-generate.yml / brandri-sync.yml / brandri-publish.yml
config/brandri-pipeline.config.yaml   全設定
docs/
  brandri-article-pipeline.md  技術仕様
  review-operations.md         レビュー運用ルール（人向け）
setup/
  slack-app-manifest.yaml      Slackアプリのマニフェスト
  slack-app-setup.md           bot作成手順
.claude/agents/
  brandri-writer.md       ★実行時にLLMのsystemプロンプトとして読み込まれる
  brandri-review-sync.md  参考資料（ロジックはsync.pyに実装済み）
.claude/commands/         Claude Codeから手動実行したい場合の任意コマンド
templates/slack-post.blocks.json
requirements.txt
```

## セットアップ

### 1. Slackアプリ（bot）を作る
`setup/slack-app-setup.md` の手順に従う。マニフェストを貼って作成 → インストール →
`#int-brandri` に招待 → `bot_user_id` を config に記入。

### 2. GitHub Secrets を登録
リポジトリの Settings → Secrets and variables → Actions に：
- `SLACK_BOT_TOKEN` … botの `xoxb-...`
- `ANTHROPIC_API_KEY` … 執筆・選定用

### 3. config を確認
`config/brandri-pipeline.config.yaml`：
- `slack.bot_user_id` を実値に（必須）
- `slack.channel_id` = `C0BNHP6HU04`（設定済み）
- カデンス・モデル・公開手段を必要に応じて調整

### 4. ディレクトリ
`marketing/articles/brandri/{drafts,scheduled,published,dropped}` は
`.gitkeep` 付きで同梱済み。

### 5. 動作確認
各ワークフローは `workflow_dispatch` で手動実行できる（`force` 入力で曜日ガードを無視）。
まず generate を force 実行 → Slackに投稿されるか確認 → 👀👍を押して sync を実行、の順で通す。

## 選定ルール

7本を4軸（独自見解 / 一次情報 / ターゲット適合 / 鮮度）でスコアリングし最高点を選ぶ。
**一次情報が0点の候補は選ばない。全候補が基準未満の週は見送る。**
見送り理由は `_selection-log.md` に残り、後から配点を検証できる。

## 公開手段（未決）

`publish.mode`：
- `manual`（現状）… 木曜に公開用原稿をSlackスレッドへ出力。人が入稿しURLを返信すると
  次のsyncが ✅ を付けて完了
- `repo_pr` / `cms_api` … 未実装。Brandri側の入稿方法が決まり次第 `publish.py` に追加

## テスト

状態機械（`state.py`）は16パターンのユニットテストで検証済み。
`python -m scripts.brandri.<generate|sync|publish>` で各段を単体実行できる。
