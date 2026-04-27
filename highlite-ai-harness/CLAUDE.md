# Claude Root Context — Highlite

このファイルはClaude（Cowork / Claude Code）が**最初に読む**ルートコンテキストです。Highliteの全業務を理解する起点として、ここから各スキルへ降りていってください。

## 1. Highliteとは

- **Vision**: 事業に余白を。本当に大切なものへ向き合うために。
- **何をする会社か**: AIを経営の中心に据え、ブランド・デザイン・業務設計を顧客と共に磨く
- **規模感**: 小規模（社員 + 業務委託パートナー）の機動的な体制
- **ロゴ・トーン**: スレートブルー × クリスタルパレット。Optima系の英文 + Noto Sans JP

詳細は `skills/_shared/brand-voice.md` を参照。

## 2. 業務フェーズ（ダッシュボードと共通）

Highliteの業務はすべて **Ore → Lite → Crysta** の循環で動きます。

| フェーズ | 意味 | 主な動き | 対応スキル |
|---|---|---|---|
| **Ore（鉱石）** | リード獲得〜提案 | 接点創出 / インバウンド / BANTC / 提案 | `skills/lead/` |
| **Lite（磨き）** | デリバリー | キックオフ / 定例 / チームビルド / 運営 | `skills/delivery/` |
| **Lite / ブランドデザイン** | 価値定義〜実装連携 | コア価値 → デザインシステム → Figma → 引き継ぎ | `skills/delivery/creative-review.md` |
| **Lite / 請求** | 検収後の専用線 | 請求書 / 入金管理 / 入金確認 | `skills/biz-mgmt/financial-snapshot.md` |
| **Crysta（結晶）** | ナーチャリング | 実績開示 / 共催イベント / ブランド索敵 → Oreに循環 | `skills/internal-marketing/` |

ダッシュボード本体: `../ai-dashboard.html`

## 3. 通知設計（4チャンネル集約）

すべてのPushは以下4チャンネルに集約。新規チャンネルを増やさないこと。

| チャンネル | 集約役割 |
|---|---|
| `#ore-リード・アサイン情報-cc` | Ore全フェーズ + 担当アサイン + SLA超過 |
| `#lite-lapidaristデリバリー-cc` | Lite運用全般（ブランドデザイン・キックオフ・定例・運営・進捗・検収） |
| `#lite-請求・入金-cc` | 請求書発行・入金期日・未入金リマインド |
| `#cry-ナーチャリング・イベント-cc` | Crysta全フェーズ + 月次索敵レポート |

通知ポリシー（小規模組織版）:
- **デイリー通知は廃止**
- **即時通知**は: インバウンド着弾 / SLA超過 / 検収完了 / 高優先度ニーズ検知
- **ウィークリー（金17時）**: PJ進捗サマリ
- **マンスリー（月初9時）**: KPI + Crysta索敵レポート
- **個別リマインダはDM**

## 4. Claudeへのお願い

### 必ずやること
- アウトプット前に `_shared/brand-voice.md` のトーンを通す
- 社内用語は `_shared/glossary.md` に従う（外部に出す時は必ず一般語に置換）
- Push先は4チャンネルから外さない
- フェーズ移行（Ore→Lite, Lite→Crysta）が起きるアクションは、必ずダッシュボード更新タスクを併発

### やらないこと
- 通知チャンネルの新設提案（4本に集約する判断は確定済み）
- 顧客固有名の安易な公開（Crysta 01「実績開示の許可」を経ていないものは伏字）
- メンバーの稼働80%超を承認なしでアサイン

### 迷ったら
- 「これは余白を増やすか？」と自問する。減らすならやらない
- 「Ore / Lite / Crysta のどこにいる？」を最初に判定する
- 担当が分からない時は `_shared/stakeholder-map.md` を見る

## 5. ファイル参照のショートカット

- ブランドトーン: `skills/_shared/brand-voice.md`
- 用語集: `skills/_shared/glossary.md`
- 担当マトリクス: `skills/_shared/stakeholder-map.md`
- リード対応の入口: `skills/lead/SKILL.md`
- デリバリー入口: `skills/delivery/SKILL.md`
- PJ運営入口: `skills/project-mgmt/SKILL.md`
- 経営管理入口: `skills/biz-mgmt/SKILL.md`
- マーケ入口: `skills/internal-marketing/SKILL.md`
- 人事入口: `skills/people-mgmt/SKILL.md`
- 外部ツール参照ルール: `connectors/`
