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

**現在の運用：キーワード記事（経営者トラック）を週1本。**

Claude Code で：
```
/brandri-draft
```
→ `marketing/keyword-progress.md` の上から未着手のキーワードを1つ選び、
   経営者トラックの規範で執筆して `drafts/` に保存する。

**⚠ 投稿の前に、必ずコミット & push すること。**
Slackの「本文を読む」リンクが branch_yuto を指すため、push前だと404になる。

```
git add marketing && git commit -m "brandri: draft" && git push
python -m scripts.brandri.post marketing/articles/brandri/drafts/<file>.md
```

書いたら `keyword-progress.md` の status を更新する。

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

1. 公開対象と👍の最終確認
   ```
   python -m scripts.brandri.publish
   ```
2. Brandri形式に変換
   ```
   python -m scripts.brandri.to_brandri marketing/articles/brandri/scheduled/<file>.md
   ```
3. Brandri に投入（別リポジトリ）
   ```
   cd /Users/toto/Documents/vscode/Brandri
   node scripts/write-knowledge.mjs <出力された.brandri.json> --next-num
   node scripts/build-data.mjs
   git add -A && git commit -m "brandri: add article" && git push
   ```
4. 公開URL（`https://brandri.jp/articles/<slug>.html`）をSlackスレッドに返信
   → 次の `sync` で ✅ が付いて完了

**取り下げる場合の片付け：** articles.json を戻す → 再ビルド →
`project/assets/thumbs/j-<slug>.svg` を手動削除（再ビルドでは消えない）。

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

### 公開予定日を過ぎた記事の扱い（自動ボツ / missed）

レビューが間に合わず公開予定日（木曜）を過ぎた記事は、次の sync / publish で
**自動的にボツ（missed）**になる。案3（鮮度重視）の仕様。
- 予定日**当日**は生存（その日の publish で公開可能）。翌日以降は missed
- 落ちた記事は消えず `marketing/articles/brandri/dropped/` に残り、
  front matter に `drop_reason: missed_publish_window` が付く
- `marketing/articles/brandri/_dropped-log.md` に日付・ID・理由・予定だった日が追記される
- Slack投稿には 🗑️ が付き、スレッドに見送りコメントが残る

「落ちすぎる」と感じたらレビュー体制を見直す。レビュー期間（publish_lead_days=8）は固定運用。

## 2つのトラック

書く記事によって規範が違う。**禁止語が逆転しているので混同しないこと。**

| | 経営者トラック | デザイナートラック |
|---|---|---|
| ネタ源 | `marketing/branding_seo_keywords_50.md` | `marketing/articles/` の日次サマリ |
| 規範 | `brandri-writer-executive.md` | `brandri-writer-designer.md` |
| 字数 | 1,800〜2,400字 | 2,000〜2,600字 |
| 構成 | 症状→構造→解の名前→明日の一歩 | 制作の型→分かれ目→ブランド逆算→AIとの分業 |
| 最重要 | **03章まで「ブランディング」を出さない** | 03章でブランドに接続 |
| target_reader | `["executive"]` | `["designer"]` |

`write-knowledge.mjs` は `target_reader` を見て、字数・related本数の
しきい値を自動で切り替える。front matter に必ず指定すること。

### キーワード記事の進め方

早川さんの推奨順：
1. Tier 1「インナーブランディング」「リブランディング」クラスタ（準ビッグ×競合低）
2. 急伸中の「ブランディング 会社」「採用ブランディング」「webブランディング」「広報ブランディング」
3. Tier 4 の業種特化で商談導線

