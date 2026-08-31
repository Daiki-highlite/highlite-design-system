---
description: キーワード記事を1本執筆してドラフトmdを作る（週1本・Tier1から順に消化・API不使用）
---

# /brandri-draft

**執筆はClaude Code自身が行う（Anthropic API課金なし）。**
**現在の運用：キーワード記事（経営者トラック）に集中。週1本。**

---

## 手順

### 1. 規範とキーワードを読む

- `.claude/agents/brandri-writer-executive.md` ← 執筆規範。**必ず読む**
- `marketing/keyword-progress.md` ← 消化管理表。次に書くキーワードを決める
- `marketing/branding_seo_keywords_50.md` ← キーワード全体像
- `skills/_shared/` の共有ナレッジ

### 2. キーワードを1つ選ぶ

`keyword-progress.md` の上から、status が `未着手` のものを選ぶ。
第1クラスタ（インナーブランディング）→ 第2クラスタ（リブランディング）→ 急伸中の4語、の順。

選んだら status を `執筆中` に更新する。

### 3. 痛みを特定する

**そのキーワードで検索する経営者は、何に困っているのか。**
ここが記事の入口になる。キーワードそのものをタイトルにしない。

例：
- 「インナーブランディング」→ 理念が現場に届いていない／営業ごとに言うことが違う
- 「リブランディング」→ 社名やロゴを変えたいが、何から手をつけるか分からない
- 「ブランディング 会社」→ どこに頼むか決めきれない／失敗したくない

### 4. 4章構成で書く

| 章 | 役割 | 字数 |
|---|---|---|
| lead | 経営者の独白から。**ブランディング不使用** | 80〜120字 |
| 01 症状 | 痛みの言語化。「うちのことだ」と思わせる | 400〜500字 |
| 02 構造 | なぜ起きるか。**まだブランディングと言わない** | 450〜550字 |
| 03 解の名前 | **ここで初めて**「それをブランディングと呼ぶ」 | 450〜550字 |
| 04 明日の一歩 | 実務の初手＋内部導線 | 350〜450字 |

**全体1,800〜2,400字。** 1段落140〜170字が目安。

### 5. 必ず守ること

- **title・lead・01・02 に「ブランディング」を出さない**（03で初出）
- 禁止語を使わない：世界観／トンマナ／クリエイティブ／アートディレクション／
  パーパス／ナラティブ／エンゲージメント／バズる／認知度アップ／フォロワー／映え／
  おしゃれ・かっこいい・素敵／デザイン思考／DX／イノベーション
- 「リブランディング」は**見出し禁止**（本文では「作り直す」「定義し直す」）
- 英字の全大文字を使わない（頭字語のみ例外）
- 実在確認できない固有名詞・数値・引用を書かない

### 6. 保存

`marketing/articles/brandri/drafts/YYYY-MM-DD-{slug}.md`

front matter に必ず含める：
```yaml
title: （痛み語の見出し）
cat: 経営          # 経営/定義論/採用/インナー/計測/フェーズ別/運用
target_reader:
  - executive      # ← 必須。しきい値判定に使われる
slug: inner-branding
keyword: インナーブランディング
related:           # 2〜3本
  - t: 診断
    href: index.html#diagnostic
  - t: ブランドとは
    href: basics/what-is-brand.html
sources:
  - key: highlite-inner-branding
    title: 「インナーブランディング」をめぐる編集ノート
    author: Highlite 編集部
    year: 2026
    type: 編
```

### 7. push してから post（順序厳守）

```
git add marketing && git commit -m "brandri: draft" && git push
python -m scripts.brandri.post marketing/articles/brandri/drafts/YYYY-MM-DD-{slug}.md
```

push 前に post すると、Slackの「本文を読む」リンクが404になる。

---

## トレンド記事を書きたい場合

デザイナートラックの規範に切り替える：`.claude/agents/brandri-writer-designer.md`
ネタ源は `marketing/articles/` の日次サマリ。
**禁止語が逆転している**（デザイン用語が解禁）ので注意。
front matter は `target_reader: ["designer"]`。
