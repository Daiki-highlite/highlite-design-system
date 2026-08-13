---
doc_id: brandri-runbook-planB
confidentiality: internal
owner: Yuto Furukawa
purpose: 案B運用手順（Anthropic API課金なし / GitHub Actionsなし）
---

# Brandri 運用手順（案B）

**執筆はProのClaude（Claude Code / チャット）で行い、Slack投稿・レビュー同期・公開だけを
botトークンで動かす。** Anthropic APIの従量課金は発生しない。GitHub Actionsも使わない。

コマンドはすべて Claude Code のターミナル（リポジトリのルート）で実行する。

## 事前準備（初回のみ）

1. botトークンをローカルに置く（gitには載らない）：
   ```
   cp .env.example .env
   # .env を開き SLACK_BOT_TOKEN=xoxb-... を記入
   ```
   トークンは api.slack.com → Brandri Bot → OAuth & Permissions の
   Bot User OAuth Token。

2. 依存をインストール：
   ```
   pip install -r scripts/brandri/requirements.txt
   ```

3. 疎通テスト（任意）：ダミーのドラフトを1本作って post → Slackに出るか確認 →
   👀👍 を押して sync → 🗓️ が付くか確認。確認後 🗑️ で片付け。

## 毎週の流れ

### 水曜：執筆して投稿

Claude Code で：
```
/brandri-draft
```
→ 直近サマリから1本選び、Highlite視点の記事を書いて
   `marketing/articles/brandri/drafts/` に md を保存する（Claude Code自身が執筆。API不要）。

保存されたら投稿：
```
python -m scripts.brandri.post marketing/articles/brandri/drafts/<file>.md
```
→ botが #int-brandri に投稿。公開予定日（翌週木曜）も自動計算される。

コミットも忘れずに：
```
git add marketing/articles/brandri && git commit -m "brandri: draft" && git push
```

### 随時：レビューを同期

古川さん・早川さんが Slack で 👀 / 👍 / 🗑️ / コメントを付ける。
気が向いたタイミングで：
```
python -m scripts.brandri.sync
```
- 👍 → 公開予約（🗓️＋予定日コメント）
- 👍取り消し → キャンセル
- 🗑️ → ボツ
- コメントあり → 「修正待ち」として報告される（自動修正はしない）

### 修正が入ったとき

1. 該当 md を Claude Code で開き、コメント内容を反映して本文を直す
2. Slack側を閉じる：
   ```
   python -m scripts.brandri.resolve marketing/articles/brandri/drafts/<file>.md --note "変更点"
   ```
3. コミット & push

### 木曜：公開

```
python -m scripts.brandri.publish
```
→ 最終確認（その場で👍を再取得）→ 問題なければ公開用原稿をスレッドに出力。
brandri.jp に入稿し、スレッドに公開URLを返信 → 次の `sync` で ✅ が付いて完了。

## GitHub Secrets について

案Bでは GitHub Actions を使わないため、リポジトリの Secrets
（SLACK_BOT_TOKEN / ANTHROPIC_API_KEY）は**不要**。残っていても害はないが、
使われない。botトークンはローカルの `.env` で管理する。

## 将来 案C（完全無人化）に戻す場合

`legacy/` に GitHub Actions ワークフローと API 執筆スクリプトを退避してある。
Anthropic APIに少額チャージして `legacy/` を戻せば、水曜生成〜木曜公開まで無人で回せる。
月あたりの目安は数百円。
EOF
echo ok