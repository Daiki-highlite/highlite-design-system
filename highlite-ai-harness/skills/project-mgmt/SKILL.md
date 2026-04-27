---
name: highlite-project-mgmt
description: Highliteのプロジェクト運営の横串スキル群。「進捗まとめて」「Slackから週報作って」「リスクログ更新」などのトリガーで起動。
---

# Project Management — 横串の運営

特定フェーズに紐づかず、**Lite運営全般を支える運用機構**を扱う。デリバリーが回り続けるための「神経系」。

## このスキルが扱う範囲

| 役割 | サブスキル | トリガーフレーズ |
|---|---|---|
| 状況集約 | `status-sync.md` | 「Slack/Zoomから週報まとめて」「進捗サマリ」 |
| リスク管理 | `risk-log.md` | 「リスク追加」「赤信号PJはどれ」 |

## 共通の作法

1. **必ず参照する**: `../../CLAUDE.md` / `../_shared/brand-voice.md` / `../_shared/stakeholder-map.md`
2. **Push先**: `#lite-lapidaristデリバリー-cc`（経営判断が必要なRiskは `@here` 付き）
3. **頻度**: 状況集約は週次、リスクログは即時 + 月次レビュー

## 設計思想

- **PMはオーバーヘッド** — 通知・報告で時間を奪わない設計
- **AIに集約させる、人は判断する** — Slack/Zoomの素材を機械が要約、判断は人
- **Riskは早期警報** — 解決を急がない。**気づくこと** が最初の価値
