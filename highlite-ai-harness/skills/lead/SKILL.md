---
name: highlite-lead
description: Highlite Oreフェーズ（リード獲得〜提案）のスキル群入口。「リード対応して」「インバウンドが来た」「BANTC埋めて」「提案書ドラフト作って」などのトリガーで起動。
---

# Lead / Oreフェーズ

リード獲得〜受注までを扱う。**鉱石を見つけ、価値を確認し、磨くべきものを選別する**フェーズ。

## このスキルが扱う範囲

ダッシュボード Flowセクションの **ORE レーン**（Step 01〜04）に対応。

| Step | サブスキル | トリガーフレーズ |
|---|---|---|
| 01 接点創出 | （マーケ側 → `internal-marketing/social-post.md`） | — |
| 02 インバウンド受付 | `inbound-triage.md` | 「問い合わせが来た」「初回返信書いて」 |
| 03 ニーズ把握 (BANTC) | `discovery-notes.md` | 「BANTC埋めて」「商談メモ作って」 |
| 04 提案 | `proposal-draft.md` | 「提案書作って」「見積根拠まとめて」 |

## 共通の作法

1. **必ず参照する**: `../../CLAUDE.md` / `../_shared/brand-voice.md` / `../_shared/glossary.md`
2. **Push先**: 全アクションが `#ore-リード・アサイン情報-cc` に集約
3. **担当判定**: アサイン未定の場合は `../_shared/stakeholder-map.md` の Ore RACI を参照
4. **時間制約**: 一次返信SLA = 24時間。これを超えるとエスカレーション

## フェーズ移行の判定

- **Ore → Lite**: 受注（契約書サイン）が確定したら。`../delivery/SKILL.md` に引き継ぐ
- **Ore → Crysta**: BANTC合計 < 8点で「今は買わない」判定の場合、`../internal-marketing/SKILL.md` のナーチャリング対象へ

## AIに最初に投げるテンプレ

```
あなたはHighliteのOreフェーズ担当です。
以下のコンテキストを踏まえて作業してください:

- 顧客: [企業名 or 伏字]
- 段階: [01-04のどれか]
- 直前の状況: [問い合わせ受領 / 初回MTG完了 / etc.]
- 期待するアウトプット: [初回返信 / BANTC評価 / 提案骨子 / etc.]

ブランドトーンは ../_shared/brand-voice.md に従ってください。
完了後、Push文を ../glossary.md のチャンネル定義に合わせて生成してください。
```
