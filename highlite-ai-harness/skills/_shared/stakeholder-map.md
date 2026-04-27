# Stakeholder Map — 担当マトリクス

「誰に聞けばいいか」「誰が決めるか」を即座に引けるようにするためのマップ。**変更があったら真っ先にここを更新する**。

## メンバー一覧（プレースホルダー）

実データへの差し替えが必要です。各セルは `[Placeholder]` のまま運用されている可能性があるため、初回アサイン時に必ず最新化してください。

### 社員

| イニシャル | 氏名 | 主ロール | Will（やりたい） | Can（できる） | Must（果たすべき） |
|---|---|---|---|---|---|
| DH | Daiki H. | Founder / CEO | 事業に余白を創る | 戦略・事業設計 | 経営判断 |
| [Placeholder] | Member 02 | Delivery Lead | [TBD] | [TBD] | [TBD] |
| [Placeholder] | Member 03 | AI / Ops | [TBD] | [TBD] | [TBD] |
| [Placeholder] | Member 04 | Sales / BizDev | [TBD] | [TBD] | [TBD] |

### パートナー（業務委託）

| イニシャル | 氏名 | 主ロール | 稼働形態 | 主な担当領域 |
|---|---|---|---|---|
| [Placeholder] | Partner 01 | Designer | スポット | UI/UX |
| [Placeholder] | Partner 02 | Engineer | 月次 | 実装 |
| [Placeholder] | Partner 03 | Writer | スポット | コンテンツ |

## RACIマトリクス（フェーズ別）

### Ore（リード）

| ステップ | 主担当 (R/A) | レビュー (A) | 情報共有 (I) |
|---|---|---|---|
| 接点創出 | DH | — | 全員 |
| インバウンド受付 | DH または BizDev | DH | 全員 |
| BANTC | アサインされた営業 | DH | Delivery Lead |
| 提案 | アサインされた営業 | DH + Delivery Lead | 全員 |

### Lite（デリバリー）

| ステップ | 主担当 (R/A) | レビュー (A) | 情報共有 (I) |
|---|---|---|---|
| キックオフ | Delivery Lead | DH | アサインメンバー全員 |
| 定例セット | Delivery Lead | — | クライアント |
| チームビルド | Delivery Lead | DH | 該当メンバー |
| 運営 | Delivery Lead | DH | クライアント + 全員 |

### Lite / ブランドデザイン

| ステップ | 主担当 (R/A) | レビュー (A) | 情報共有 (I) |
|---|---|---|---|
| コア価値〜ブランド定義 | Delivery Lead | DH | クライアント |
| テイスト〜要素構成 | Designer (パートナー含む) | Delivery Lead | DH |
| Claude Design運用 | Designer + AI/Ops | Delivery Lead | — |
| Figma連携〜引き継ぎ | Designer + Engineer | Delivery Lead | クライアント |

### Lite / 請求

| ステップ | 主担当 (R/A) | レビュー (A) | 情報共有 (I) |
|---|---|---|---|
| 請求書発行〜入金確認 | DH または AI/Ops | DH | Delivery Lead |

### Crysta（ナーチャリング）

| ステップ | 主担当 (R/A) | レビュー (A) | 情報共有 (I) |
|---|---|---|---|
| 実績開示の許可 | Delivery Lead | DH | Marketing |
| 共催イベント | DH | — | 全員 |
| ブランド索敵 | AI/Ops | DH | BizDev |

## エスカレーション経路

```
パートナー → Delivery Lead → DH
社員 → Delivery Lead → DH
顧客クレーム → Delivery Lead → DH（即時）
法務・契約問題 → DH（外部弁護士に相談）
```

## 不在時の代理ルール

- DHが不在: Delivery Lead が暫定判断 → 復帰後にレビュー
- Delivery Lead が不在: 該当PJで最も稼働率が高いメンバーが代理
- 全員不在の緊急: クライアントには「翌営業日の対応」を伝える定型文を返信（`#lite-lapidaristデリバリー-cc` のピン留め参照）

## 更新履歴

このファイルは「現状の写像」。変更があったら以下を必ず更新:
- アサイン変更時 → 該当行を更新
- 新メンバー / パートナー追加時 → 一覧に追記 + ダッシュボードのMemberセクションも更新
- ロール変更時 → ダッシュボードのMember Will/Can/Must も同期
