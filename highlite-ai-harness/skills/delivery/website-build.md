# Skill: Website Build — フェーズ2（案件獲得後）

## 目的
フェーズ1のPoCを基盤として、より詳細な要件定義・実装・Figma納品物パッケージまでを完成させる。

---

## 前提条件

- `clients/<client-slug>/profile.json` が存在し `_meta.phase` が `"active"` であること
- `clients/<client-slug>/poc/index.html` が存在すること（フェーズ1の成果物）
- キックオフ済みであること（`delivery/kickoff.md` 参照）

---

## フロー

### STEP 1 — 要件定義ヒアリング（詳細版）

PoCレビューを踏まえ、以下を追加ヒアリングする。

**[A] 機能要件**
- 必要なページ数・構成（例：TOP / About / Service × 3 / Blog / Contact）
- フォーム・予約・決済など動的機能の有無
- 多言語対応の有無

**[B] デザイン詳細**
- PoC と変えたい箇所（レイアウト・カラー・トーン）
- 参考サイト（URL × 2〜3件）
- NG表現・避けたい印象

**[C] コンテンツ**
- 確定コピー / 仮コピーの区別
- 写真・動画素材の有無と調達方法
- ロゴデータ形式（SVG推奨）

**[D] 技術・インフラ**
- 希望技術スタック（HTML静的 / CMS / フレームワーク）
- ホスティング先
- SEO・解析要件（GA4 / Search Console など）

**[E] スケジュール**
- ファーストドラフト提示希望日
- 公開希望日

---

### STEP 2 — profile.json の拡張

`profile.json` の `_meta.phase` を `"active"` に更新し、
以下の追加フィールドを書き加える：

```json
{
  "_meta": {
    "phase": "active",
    "pages": [],
    "stack": "",
    "hosting": ""
  },
  "requirements": {
    "dynamic_features": [],
    "languages": ["ja"],
    "seo": true,
    "analytics": "GA4",
    "reference_sites": [],
    "design_notes": "",
    "schedule": {
      "first_draft": "",
      "launch": ""
    }
  }
}
```

---

### STEP 3 — 実装（イテレーション）

1. `clients/<client-slug>/poc/index.html` を `clients/<client-slug>/production/index.html` にコピー
2. 要件に応じてセクション・スタイルを拡張
3. 追加ページは `clients/<client-slug>/production/<page-name>/index.html` として作成
4. 各イテレーション後にレビュー → profile.json 更新 → 再生成のサイクル

---

### STEP 4 — Figma 納品物パッケージ

`figma:figma-generate-design` スキルを使い、完成HTMLからFigmaファイルを生成する。

納品物に含めるもの：

| ファイル | 内容 |
|---|---|
| Figma Design File | 全ページ × PC / SP |
| Design Token Sheet | カラー / タイポ / スペーシング |
| Component Spec | 再利用コンポーネント一覧 |
| Handoff Notes | `delivery/handoff.md` に従って作成 |

---

### STEP 5 — 検収・Crystaへ移行

- 検収完了後 → `biz-mgmt/financial-snapshot.md` の請求フローを起動
- 実績開示可能になり次第 → `internal-marketing/case-study.md` でCrystal化

---

## ファイル構成（完成時）

```
clients/
  <client-slug>/
    profile.json            ← 最終データ（phase: active）
    poc/
      index.html            ← フェーズ1の成果物（保存）
    production/
      index.html            ← 本番HTML
      <page>/
        index.html
    figma/
      design-spec.md        ← Figmaリンク + 仕様メモ
      handoff-notes.md      ← 引き渡しノート
```

---

## 注意事項

- PoCは必ず保存する（クライアントとの合意の証拠）
- デザイン変更の根拠は `profile.json` の `requirements.design_notes` に残す
- Figmaへの書き出しは `figma:figma-use` スキルをロードしてから実行する
