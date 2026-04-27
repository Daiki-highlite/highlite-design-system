# Highlite AI Harness

> 事業に余白を。本当に大切なものへ向き合うために。

Highliteの全社オペレーションをAIに伴走させるための「ハーネス」です。スキル・コンテキスト・コネクタを一箇所に集約し、Claude（Code / Cowork）が一貫したトーンとフレームワークで動けるようにします。

## このリポジトリの位置付け

- **AI-Centered Management Dashboard**（`ai-dashboard.html`）が「見るための地図」だとすれば、本ハーネスは「動くための足場」
- ダッシュボードのフェーズ定義（**Ore / Lite / Crysta**）を、スキル群の動作原則として継承
- すべての成果物は4チャンネル設計（`#ore-リード・アサイン情報-cc` ほか）に Push される前提で書かれる

## 全体マップ

```
highlite-ai-harness/
├── README.md                          ← いまここ
├── CLAUDE.md                          ← Claudeがまず読むルートコンテキスト
├── skills/
│   ├── _shared/                       ← 全スキルが参照する共通リソース
│   │   ├── brand-voice.md             ← トーン&マナー
│   │   ├── glossary.md                ← 社内用語・略語
│   │   └── stakeholder-map.md         ← 担当マトリクス
│   ├── lead/                          ← Oreフェーズ（受注前）
│   ├── delivery/                      ← Liteフェーズ（受注後）
│   ├── project-mgmt/                  ← PJ運営の横串
│   ├── biz-mgmt/                      ← 経営管理
│   ├── internal-marketing/            ← Crysta起点の発信
│   └── people-mgmt/                   ← メンバーの Will/Can/Must 運用
└── connectors/                        ← 外部ツールの参照ルール
    ├── google-workspace.md
    ├── slack.md
    ├── zoom.md
    └── figma.md
```

## 使い方

### Claude（Cowork / Code）から呼び出す

1. リポジトリをローカルに置く（既にこの位置にあります）
2. 各スキルの `SKILL.md` 冒頭の frontmatter（`name` / `description`）に従って Claude が自動で関連スキルを参照
3. 共通文脈（`_shared/`）と コネクタ規約（`connectors/`）は、各スキルから参照される

### 人間が手で参照する

- 新メンバー: まず `_shared/glossary.md` → `_shared/stakeholder-map.md` の順で読む
- 商談前: `lead/SKILL.md` から該当ステップを開く
- デリバリー中: `delivery/SKILL.md` を起点に、現在のフェーズに応じたサブスキルへ
- 1on1前: `people-mgmt/1on1-prep.md`
- 月次の振り返り: `biz-mgmt/pipeline-review.md` + `biz-mgmt/financial-snapshot.md`

## ダッシュボードとの対応

| ダッシュボードのフェーズ | 本ハーネスのスキル |
|---|---|
| Ore（鉱石） | `skills/lead/` |
| Lite（磨き / メイン） | `skills/delivery/` |
| Lite（磨き / ブランドデザイン） | `skills/delivery/creative-review.md` |
| Lite（請求） | `skills/biz-mgmt/financial-snapshot.md` |
| Crysta（結晶 / ナーチャリング） | `skills/internal-marketing/` |

## 設計原則

1. **AIを共同経営者として扱う** — タスクの委譲ではなく、共に問いを立てる相手として
2. **小規模組織に最適化** — 通知は最小限、4チャンネルに集約
3. **ブランドトーンを最優先** — 全アウトプットは `_shared/brand-voice.md` を経由
4. **Crysta → Ore のループを忘れない** — 終わりを次の始まりに繋げる構造を内包
5. **余白を残す** — テンプレートは骨格だけ。書き込みすぎず、人の判断を消さない

## 更新の流儀

- スキル追加: 該当ディレクトリに `.md` を作成 → 親の `SKILL.md` のリストに追記
- 用語追加: `_shared/glossary.md` に追記（重複チェックを忘れず）
- 担当変更: `_shared/stakeholder-map.md` を真っ先に更新
- コネクタ追加: `connectors/` に新規 `.md` → 本READMEの「全体マップ」を更新
