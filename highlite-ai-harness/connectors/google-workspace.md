# Google Workspace — 命名規則と参照ルール

Drive / Calendar / Gmail で「どこに何があるか」が一意に分かる状態を保つ。命名規則がオペレーションの神経系。

## Drive

### トップレベル構造

```
Highlite Drive/
├── 00_Brand/                    # ブランド資産（ロゴ・ガイドライン・テンプレート）
├── 01_Ore/                      # リード関連（提案書・Disco Note）
│   └── [企業名 or YYYYMM-企業名]/
├── 02_Lite/                     # デリバリー関連（PJごと）
│   └── [PJ名]/
│       ├── 01_Kickoff/
│       ├── 02_Cadence/         # 議事録・録画
│       ├── 03_Design/          # Figma出力 / Claude Design出力
│       ├── 04_Deliverables/    # 納品物
│       └── 05_Handoff/
├── 03_Crysta/                   # 完了PJのアーカイブ + 事例素材
│   └── [企業名]/
├── 04_BizOps/                   # 経営管理（請求書 / 契約書 / 財務）
├── 05_People/                   # 人事関連（限定アクセス）
└── 99_Archive/                  # 古いものの保管
```

### 命名規則

**フォルダ名**:
- `00_xxx`, `01_xxx` のように **数字プレフィックス** で順序を制御
- 日本語OK。半角スペース不可（アンダースコア or 全角スペース）

**ファイル名**:
- `YYYYMMDD_案件名_種別_v01.ext`
- 例: `20260427_acme_proposal_v02.pdf`
- バージョンは `v01`, `v02`...（`final`, `latest` は使わない）
- 機密ファイルは末尾に `_confidential` を付与

### アクセス制御

| フォルダ | 社員 | パートナー | 顧客 |
|---|---|---|---|
| `00_Brand/` | 編集 | 閲覧 | — |
| `01_Ore/` | 編集 | アサインPJのみ閲覧 | — |
| `02_Lite/[PJ名]/` | 編集 | アサインPJ編集 | 一部フォルダ閲覧 |
| `03_Crysta/` | 閲覧 | — | — |
| `04_BizOps/` | DH+Lead 編集 | — | — |
| `05_People/` | DH のみ編集 | — | — |
| `99_Archive/` | 閲覧のみ | — | — |

## Calendar

### カレンダー構成

- **個人カレンダー**: 各メンバー（一次予定）
- **Highlite-Internal**: 社内定例 / 1on1 / 全社MTG
- **Highlite-Lite-[PJ名]**: PJ別定例（顧客と共有）
- **Highlite-Marketing**: 発信スケジュール / イベント

### 予定の命名規則

```
[フェーズ] [PJ or 内容] [種別]
```

例:
- `[Lite] AcmeCorp 定例 #04`
- `[Ore] BetaInc 初回MTG`
- `[Internal] 1on1 / DH × 田中`
- `[Crysta] GammaCo 共催ウェビナー打合せ`

### 予定の必須情報

- タイトル: 上記命名規則
- 場所 / Zoom URL
- 参加者
- 説明欄に: アジェンダリンク / 関連Drive folder
- 録画する場合は説明欄に「録画あり / 文字起こし対象」明記

## Gmail

### ラベル運用

```
Ore/
├── Ore/Inbound        # 新規問い合わせ
├── Ore/Discovery      # Discovery進行中
└── Ore/Proposal       # 提案送付済み
Lite/
├── Lite/[PJ名]
└── Lite/Billing       # 請求関連
Crysta/
├── Crysta/Disclosure  # 開示打診中
└── Crysta/Sensing     # ブランド索敵
Internal/
└── Internal/Admin     # 経理 / 法務 / インフラ
```

### 命名・運用ルール

- **ラベル + 既読管理** で処理状態を表現
- 1メールに **複数ラベルOK**（Ore + 該当顧客名 など）
- 返信SLA: Oreインバウンドは24h、それ以外は48h
- スター: 「自分が次に動くべきもの」のみ（量を抑える）

## AIから参照する時のお作法

```
あなたは Highlite のGoogle Workspaceから情報を取りに行きます。
以下のルールに従ってください:

- フォルダ参照: 上記Drive構造に従い、必ずトップレベル → サブの順で辿る
- ファイル特定: 命名規則 [YYYYMMDD_案件名_種別_v01.ext] にマッチしないものは「不明」と返す
- アクセス制御: 「アクセス制御」表で許可されていない領域に入らない
- 参照後のキャッシュ: 機密度の高い情報（05_People / 04_BizOps）はコンテキストに残さない
```

## アンチパターン

- ルートに散らばる無番号フォルダ → 即整理
- `final.docx`, `latest_v3_本当に最終.pdf` などの混乱命名 → バージョン番号統一
- 個人ドライブにPJ資産を置く → Drive中央に集約
- カレンダー予定にアジェンダリンクなし → 情報が散る
- Gmailラベル未付与の重要メール → 検索で迷子になる

## 監査リズム

- 月次: `01_Ore/` `02_Lite/` の構造健全性チェック
- 四半期: `99_Archive/` への移動候補をピックアップ
- 半期: アクセス権限の棚卸し
