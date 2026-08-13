---
description: 直近サマリから1本選び、Highlite視点の記事を執筆してドラフトmdを作る（Claude Codeで実行・API不使用）
---

# /brandri-draft

**案B：執筆はClaude Code自身が行う（Anthropic API課金なし）。**
このコマンドはClaude Code上で動かす。

## 手順

1. `config/brandri-pipeline.config.yaml` と、`skills/_shared/` の共有ナレッジ、
   `.claude/agents/brandri-writer.md`（執筆方針）を読む
2. `marketing/articles/` の直近7日分のデイリーサマリを読む。
   `marketing/articles/brandri/_selection-log.md` を見て使用済みは除外
3. `brandri-writer` の選定基準（4軸スコアリング）で全候補を評価し、最高点の1本を選ぶ
   - 合計7点未満、または一次情報が0点なら選定しない
   - 全候補が基準未満なら「今週は見送り」と報告して終了
4. `brandri-writer` の構成・文体で記事を執筆する（5ブロック構成・一次情報必須）
5. `marketing/articles/brandri/drafts/YYYY-MM-DD-{slug}.md` に保存。
   front matter に title / target_cluster / keywords / source_summaries /
   selection（score, breakdown, rationale, candidates_considered, rejected）を入れる
6. 保存後、次のコマンドでSlackへ投稿するよう促す：
   ```
   python -m scripts.brandri.post marketing/articles/brandri/drafts/YYYY-MM-DD-{slug}.md
   ```
   （SLACK_BOT_TOKEN は .env かシェルの export で設定済みであること）

## 注意
- 記事本文はClaude Code（Pro/Max枠）が書く。Anthropic APIキーは不要
- 一次情報（実務ではこうだった）が書けない題材は選定段階で落とす
