# Webサイト生成システム — 運用ドキュメント

Highliteがクライアント向けWebサイトを作成するための2フェーズ生成システムです。
営業時のPoC（概念実証）から、案件獲得後の本制作・Figma納品まで一貫したプロセスを提供します。

---

## 全体設計

```
フェーズ1（営業時）                フェーズ2（案件獲得後）
─────────────────────────         ────────────────────────────────
ヒアリング                          詳細要件定義
   ↓                                  ↓
profile.json 作成                  profile.json 拡張
   ↓                                  ↓
generate-poc.js 実行              本制作（HTML拡張 + 追加ページ）
   ↓                                  ↓
PoC HTML をクライアントへ提示      Figma 納品物パッケージ作成
```

- **フェーズ1** は `profile.json` の入力と 1コマンドで完結。短時間でPoC提示が可能
- **フェーズ2** はフェーズ1の成果物を土台にしてそのまま拡張できる
- テンプレートを切り替えるだけで、業種に合ったレイアウトを即座に出し分けられる

---

## ファイル構成

```
highlite-design-system/
│
├── website-system/
│   ├── README.md                   ← このドキュメント
│   ├── generate-poc.js             ← PoC生成スクリプト
│   └── templates/
│       ├── poc-template.html       ← corporate テンプレート
│       ├── poc-warmth.html         ← warmth テンプレート
│       └── poc-launch.html         ← launch テンプレート
│
├── clients/
│   ├── _template/
│   │   └── profile.json            ← 新規クライアント用スキーマ（コピー元）
│   ├── _example/
│   │   └── profile.json            ← 記入例（建築事務所）
│   └── <client-slug>/              ← クライアントごとのフォルダ
│       ├── profile.json            ← 入力データ
│       ├── poc/
│       │   └── index.html          ← 生成されたPoC（フェーズ1の成果物）
│       └── production/             ← 本制作データ（フェーズ2）
│           └── index.html
│
└── highlite-ai-harness/
    └── skills/delivery/
        ├── website-poc.md          ← フェーズ1 Claudeスキル
        └── website-build.md        ← フェーズ2 Claudeスキル
```

---

## テンプレート選択ガイド

`profile.json` の `_meta.template` に指定する。指定がない場合は `corporate` が使われる。

| テンプレート名 | 向いている業種 | レイアウトの特徴 |
|---|---|---|
| `corporate` | コンサル・士業・不動産・B2B全般 | 左寄せヒーロー、2カラムAbout、サービスカードグリッド |
| `warmth` | カフェ・飲食・wellness・ライフスタイル | 中央セリフ体ヒーロー、交互フィーチャー行、温かみのあるCTA |
| `launch` | スタートアップ・SaaS・DX・採用 | 分割ヒーロー（コピー左 / カラーパネル右）、統計帯、番号付きサービス |

迷ったときの判断基準:

- 「信頼・実績・専門性」を前面に出したい → **corporate**
- 「世界観・空間・体験・素材へのこだわり」を伝えたい → **warmth**
- 「変化・スピード・成果・数字」で訴求したい → **launch**

---

## フェーズ1 — PoC生成の手順

### Step 1. クライアント情報のヒアリング

以下の情報シートを使ってヒアリングを行い、会話の中で埋めていく。

```
## クライアント情報シート

### [A] 会社基本情報
- 会社名（日本語）:
- 会社名（英語）:
- 業種・業態:
- 会社の説明（2〜3文）:
- タグライン / キャッチコピー（あれば）:

### [B] サイトの目的
- 作る目的（例：問い合わせ増 / 採用 / ブランド認知 / EC）:
- ターゲット（誰に見てほしいか）:
- 訪問者に一番伝えたいこと:

### [C] コンテンツ
- ヒーロー見出し（大きく出るキャッチコピー）:
- ヒーローサブ見出し（補足の一文）:
- ヒーロー説明文（2〜3文）:

- サービス / 強み①  タイトル:  説明:
- サービス / 強み②  タイトル:  説明:
- サービス / 強み③  タイトル:  説明:

- 数字で語れる実績:
  - 数字①  値:  ラベル:
  - 数字②  値:  ラベル:
  - 数字③  値:  ラベル:

### [D] 問い合わせ・CTA
- CTAボタンの文言:
- 問い合わせ先メール:
- 所在地（都市名程度でOK）:

### [E] ブランド（任意）
- メインカラー（HEXまたはイメージ）:
- フォントのイメージ（例：モダン / 伝統的 / カジュアル）:

### [F] 営業メモ（任意）
- 営業背景・経緯:
- クライアントの課題感:
- 次のアクション:
```

### Step 2. profile.json の作成

```bash
# テンプレートをコピーして新クライアント用ファイルを作成
cp clients/_template/profile.json clients/<client-slug>/profile.json
```

`client_slug` の命名規則: 小文字英数字 + ハイフン（例: `nextstride`, `cafe-komorebi`）

ヒアリング内容をもとに `profile.json` の各フィールドを埋め、
業種に合った `_meta.template` を指定する。

```json
{
  "_meta": {
    "template": "launch",
    "client_slug": "nextstride",
    ...
  }
}
```

### Step 3. PoC生成

```bash
node website-system/generate-poc.js <client-slug>
```

**出力先:** `clients/<client-slug>/poc/index.html`
ブラウザで直接開いてクライアントへ画面共有またはメール添付で提示できる。

### Step 4. 調整・再生成

`profile.json` を直接編集して同じコマンドを再実行するだけで更新される。

```bash
# 例：カラーやコピーを修正後に再生成
node website-system/generate-poc.js cafe-komorebi
```

---

## フェーズ2 — 本制作への移行

### 移行のタイミング

- 案件獲得・契約締結後
- キックオフ完了後（`skills/delivery/kickoff.md` 参照）

### Step 1. profile.json のフェーズ更新

`_meta.phase` を `"poc"` → `"active"` に変更し、詳細要件フィールドを追加する。

```json
{
  "_meta": {
    "phase": "active",
    "template": "launch"
  },
  "requirements": {
    "pages": ["top", "about", "service", "contact"],
    "dynamic_features": ["問い合わせフォーム"],
    "languages": ["ja"],
    "seo": true,
    "analytics": "GA4",
    "reference_sites": [],
    "design_notes": "",
    "schedule": {
      "first_draft": "YYYY-MM-DD",
      "launch": "YYYY-MM-DD"
    }
  }
}
```

### Step 2. PoCをベースに本制作

```bash
# PoCを保存しつつ本制作フォルダへコピー
cp -r clients/<client-slug>/poc/index.html clients/<client-slug>/production/index.html
```

PoCは **必ず保存する**（クライアントとの合意の証拠）。

### Step 3. Figma納品物の作成

`figma:figma-generate-design` スキルを使い、完成HTMLからFigmaファイルを生成する。

納品物セット:

| ファイル | 内容 |
|---|---|
| Figma Design File | 全ページ × PC / SP |
| Design Token Sheet | カラー / タイポ / スペーシング |
| Component Spec | 再利用コンポーネント一覧 |
| Handoff Notes | `skills/delivery/handoff.md` に従って作成 |

---

## よく使うコマンド

```bash
# PoC生成
node website-system/generate-poc.js <client-slug>

# テンプレートを変えて比較（profile.jsonのtemplateを書き換えてから）
node website-system/generate-poc.js <client-slug>

# 既存クライアント一覧を確認
ls clients/
```

---

## profile.json フィールド早見表

| フィールド | 必須 | 説明 |
|---|---|---|
| `_meta.template` | ○ | `corporate` / `warmth` / `launch` |
| `_meta.phase` | ○ | `poc`（フェーズ1）/ `active`（フェーズ2） |
| `_meta.client_slug` | ○ | フォルダ名と一致させる |
| `brand.color_primary` | ○ | メインカラー（HEX）|
| `brand.font_heading` | ○ | 見出しフォント |
| `content.hero.*` | ○ | ヒーローセクションの全コンテンツ |
| `content.about.stats` | 推奨 | 実績数字（最大3つ）|
| `content.services.items` | ○ | サービス・強み（2〜4項目推奨）|
| `website_goal.key_message` | launch必須 | Aboutハイライトに使用 |
| `poc_notes.*` | 推奨 | 営業背景・課題・次アクション |

---

## 実績クライアント

| slug | テンプレート | 業種 |
|---|---|---|
| `nextstride` | launch | ITコンサルティング / DX伴走支援 |
| `cafe-komorebi` | warmth | 自家焙煎コーヒー・オーガニックカフェ |

---

*最終更新: 2026-05-23*
