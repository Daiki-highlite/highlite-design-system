---
name: highlite-delivery
description: Highlite Liteフェーズ（受注後デリバリー）のスキル群入口。「キックオフ準備」「クリエイティブレビュー」「引き継ぎ資料作って」などのトリガーで起動。
---

# Delivery / Liteフェーズ

受注した鉱石を磨き、結晶へ向かわせるフェーズ。**lapidarist（宝石研磨師）の比喩で動く**。

## このスキルが扱う範囲

ダッシュボード Flowセクションの **LITE レーン全般**（メイン4ステップ + ブランドデザイン10ステップ）に対応。請求関連は経営管理側へ委譲。

| Step | サブスキル | トリガーフレーズ |
|---|---|---|
| 01 キックオフ | `kickoff.md` | 「キックオフ資料作って」「初回MTG準備」 |
| 02 定例セット | （`project-mgmt/status-sync.md` と連携） | 「アジェンダ作って」 |
| 03 チームビルド | （`people-mgmt/onboarding.md` と連携） | 「アサイン提案して」 |
| 04 運営 | （`project-mgmt/status-sync.md`） | 「進捗まとめて」 |
| ブランドデザイン全工程 | `creative-review.md` | 「デザイン案レビュー」「Figma整理」 |
| 10 引き継ぎ | `handoff.md` | 「エンジニア向け仕様書」「先方への引き渡し資料」 |

## 共通の作法

1. **必ず参照する**: `../../CLAUDE.md` / `../_shared/brand-voice.md` / `../_shared/glossary.md` / `../_shared/stakeholder-map.md`
2. **Push先**: 全アクションが `#lite-lapidaristデリバリー-cc` に集約（請求関連のみ `#lite-請求・入金-cc`）
3. **顧客連絡**: 既存メール or 顧客側Slackをそのまま使う。PJ専用チャンネルは作らない
4. **進捗サマリ**: 毎週金曜17時に自動投稿（`project-mgmt/status-sync.md` 参照）

## フェーズ移行の判定

- **Lite → 請求**: 検収完了で `biz-mgmt/financial-snapshot.md` の請求タスクへ
- **Lite → Crysta**: 入金確認完了で `internal-marketing/case-study.md` の実績開示打診へ

## デリバリー全体のチェックポイント

各PJの開始時、Delivery Lead は以下を必ず確認:
- [ ] スコープ・成功基準・体制が明文化されているか（キックオフ資料）
- [ ] 定例MTG・アジェンダテンプレが共有されているか
- [ ] アサインメンバーの稼働率が80%超になっていないか
- [ ] 検収基準が「測定可能な形」で定義されているか
- [ ] 顧客側との緊急時連絡ルートが決まっているか

## AIに最初に投げるテンプレ

```
あなたはHighliteのLiteフェーズ担当（lapidarist）です。
以下の状況で作業します:

- PJ: [名称]
- 顧客: [企業名 or 伏字]
- フェーズ: [01 Kickoff / 02 Cadence / 03 Team Build / 04 Operations / Brand Design 0X]
- 直前の状況: [契約締結 / キックオフ完了 / 定例N回目 / etc.]
- 期待するアウトプット: [...]

ブランドトーン: ../_shared/brand-voice.md
担当判定: ../_shared/stakeholder-map.md の Lite RACI
完了後、Push文を `#lite-lapidaristデリバリー-cc` 向けに生成してください。
```
