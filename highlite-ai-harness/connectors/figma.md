# Figma — ファイル構造とライブラリ参照

デザインの中央集権化と、PJ間での再利用を両立させる。Claude Designの出力もFigmaに集約することで、人の判断と機械の生成を一つの場所で扱う。

## ファイル構造

```
Figma Workspace「Highlite」
├── HL-Brand                      # Highlite自社のブランドデザインシステム
│   ├── Tokens                    # Color / Typography / Spacing / Radius / Shadow
│   ├── Foundations               # Logo / Sparkle / Gradients
│   ├── Components                # Button / Card / Modal / Form etc.
│   ├── Patterns                  # Hero / Footer / Navigation etc.
│   └── Templates                 # Slides / Document / SNS素材
├── HL-Internal                   # 社内資料（経営 / 採用 / 提案）
│   ├── Sales-Deck-Master
│   ├── Recruiting-Master
│   └── Internal-OKR
└── Lite-[PJ名] / クライアント別ファイル
    ├── 00_Brief                  # キックオフ資料・スコープ
    ├── 01_Discovery              # 競合分析・ムードボード
    ├── 02_Concept                # コア価値〜要素構成
    ├── 03_Design-System          # PJ固有のトークン・コンポーネント
    ├── 04_Designs                # 提案案 / バリエーション
    ├── 05_Final                  # 確定デザイン（顧客承認済み）
    └── 06_Handoff                # Dev Mode / 引き継ぎ資料
```

## ライブラリ参照ルール

### HL-Brand を必ず参照

すべてのPJファイルは `HL-Brand` をライブラリとして読み込み、以下を参照:
- カラートークン（クリスタルパレット + ベース色）
- タイポグラフィ（Optima / Noto Sans JP）
- スペーシングスケール（4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128）
- スパークルロゴ（4点星のSVG）
- ボタン・カード等の基礎コンポーネント

### PJ固有トークンの作り方

`03_Design-System` 内に PJ専用 Variables を作成し、HL-Brand の Variables を **拡張** する形で運用:

```
PJ-Color-Primary    = HL-Brand-Color-CrystalBlue（同じか上書き）
PJ-Color-Accent     = #XXXXXX（PJ固有）
PJ-Typography-Heading = HL-Brand-Optima-Display
```

PJ完了後、再利用価値のあるパターンが見つかった場合は HL-Brand への昇格を検討（DH + Designer合議）。

## ページ構成（PJファイル内）

各PJファイルは以下のページ構成を標準化:

```
📄 Cover                  # PJ名 / クライアント / 期間 / 担当
📄 00_Brief
📄 01_Discovery
📄 02_Concept
📄 03_Design-System
📄 04_Designs / Variations
📄 05_Final
📄 06_Handoff
📄 99_Archive             # 没案・ボツ要素
```

## 命名規則

### Frame名

- セクション: `[番号]. [意味のある名前]` 例: `01. Hero`, `02. About`
- 状態: `[Component] / [State]` 例: `Button / Hover`, `Card / Disabled`
- バリアント: `[Component] / [Variant]` 例: `Button / Primary`, `Card / Featured`

### コンポーネント Variants（必須プロパティ）

| プロパティ | 値の例 |
|---|---|
| State | default / hover / active / disabled / error |
| Size | sm / md / lg |
| Variant | primary / secondary / tertiary |
| Theme | light / dark（必要時） |

## Claude Design 連携

```
Claude Design 出力
↓
Drive: /Highlite Drive/02_Lite/[PJ名]/03_Design/claude-design/
↓
Figma にインポート → 04_Designs ページの「Claude Origin」セクションへ配置
↓
人による Brand Fit / Craft / Feasibility レビュー
（../skills/delivery/creative-review.md 参照）
↓
採用案を 05_Final へ昇格
```

## AIプロンプト例

### Figmaファイル監査

```
Figmaファイル [URL] を Dev Mode で参照し、以下を監査:

- ページ構成が標準（00_Brief 〜 06_Handoff）に沿っているか
- HL-Brand ライブラリを参照しているか（Variables / Components）
- 命名規則違反（Frame "Frame 23" のような自動命名残り）
- AutoLayout 不適用の手動位置指定セクション
- Variants が状態を網羅していないコンポーネント
- アクセシビリティ要件（コントラスト / フォーカス指示）の欠落

問題は「ページ / Frame / 修正方針」の3列で出力。
```

### Dev Mode から実装ガイド生成

```
Figma Dev Mode のJSON出力 [リンク] から、エンジニア向け実装ガイドを生成:

- デザイントークン → CSS Variables / TS定数
- コンポーネント → React/Vue propsインターフェース案
- レスポンシブ規則 → メディアクエリ仕様
- アニメーション → keyframes/transitionの仕様

../skills/delivery/handoff.md のフォーマットに沿って Markdown で。
```

### ライブラリ昇格判定

```
PJ「[PJ名]」の `03_Design-System` ページ [リンク] の中から、
HL-Brand への昇格候補（汎用性が高く、他PJで再利用できそうなもの）を3つ抽出。
各候補について:
- 抽出元（PJ内のどこ）
- 汎用化のために必要な調整
- 想定される再利用シーン
- 昇格させない場合の理由（現状のままが正しい場合）
```

## アクセス制御

| ファイル | 社員 | パートナー（Designer） | 顧客 |
|---|---|---|---|
| `HL-Brand` | 編集 | 閲覧 | — |
| `HL-Internal` | 編集 | アサインPJのみ閲覧 | — |
| `Lite-[PJ名]` | 編集 | アサインPJ編集 | 閲覧（05_Final / 06_Handoff のみ） |

## Push文テンプレ

```
:art: Figma Update — [PJ名]

▼ ファイル
[Figma URL]

▼ 更新内容
- [ページ名]: [変更概要]

▼ レビュー依頼
- レビュアー: @[名前]
- 観点: Brand Fit / Craft / Feasibility

▼ 関連スキル
../skills/delivery/creative-review.md
```

## 注意

- **HL-Brand の改変は DH + Designer 合議制** — 全PJに影響するため
- **PJ完了後、Lite-[PJ名] ファイルは Archive Project へ移動** — Workspace を肥大化させない
- **顧客とのファイル共有は閲覧権限のみ** — 編集権を渡さない
- **Claude Design 出力は必ず人の手を経由** — 直接顧客に出さない
- **フォント・画像の商用利用ライセンス** を 06_Handoff の前に必ず確認

## アンチパターン

- 自動命名（"Frame 23"）の放置 → AI参照精度が落ちる
- AutoLayout なしの手動位置指定 → レスポンシブ崩壊
- ライブラリ参照なしの色直書き → ブランド破綻
- ページ構成バラバラ → 引き継ぎ困難
- Variants 不完全 → 実装で抜け漏れ発生
