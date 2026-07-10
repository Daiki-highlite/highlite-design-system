# Quickstart: Cloudflare Pages デプロイ検証ガイド

**Feature**: kgi-sales-tasks.html の外部公開
**Date**: 2026-06-19

---

## 前提条件

- [ ] Cloudflareアカウントを持っている
- [ ] Node.js がインストールされている（`node -v` で確認）
- [ ] プロジェクトルート（`highlite-design-system/`）にいる

---

## セットアップ（初回のみ）

### 1. Wrangler CLI をインストール

```bash
npm install -g wrangler
```

インストール確認：
```bash
wrangler --version
```

### 2. Cloudflare にログイン

```bash
wrangler login
```

ブラウザが開くので、Cloudflareアカウントでログインして認証を完了する。

---

## デプロイ手順

### 3. deploy ディレクトリを準備

```bash
mkdir -p deploy
cp marketing/kgi_strategy/kgi-sales-tasks.html deploy/index.html
```

### 4. Cloudflare Pages にデプロイ

```bash
wrangler pages deploy deploy/ --project-name highlite-sales-tasks
```

初回実行時はプロジェクトが新規作成される。

### 5. 発行されたURLを確認

デプロイ完了後、ターミナルに以下のようなURLが表示される：

```
✨ Deployment complete! Take a look over at https://xxxxxxxx.highlite-sales-tasks.pages.dev
```

このURLをブラウザで開いて動作確認する。

---

## 動作確認チェックリスト

- [ ] ページが正しく表示される（レイアウト崩れなし）
- [ ] サイドバーのナビゲーションが機能する
- [ ] Google Fontsが適用されている（Noto Sans JP）
- [ ] モバイルブラウザでも表示される

---

## 更新フロー（ファイル変更後の再デプロイ）

```bash
# 1. HTMLファイルを編集（marketing/kgi_strategy/kgi-sales-tasks.html）

# 2. deployディレクトリに反映
cp marketing/kgi_strategy/kgi-sales-tasks.html deploy/index.html

# 3. 再デプロイ
wrangler pages deploy deploy/ --project-name highlite-sales-tasks
```

---

## トラブルシューティング

| 症状 | 対処 |
|------|------|
| `wrangler login` でブラウザが開かない | `wrangler login --browser=false` でトークンを手動コピー |
| フォントが表示されない | インターネット接続を確認（Google Fonts依存） |
| デプロイ後に変更が反映されない | ブラウザのキャッシュをクリア（Ctrl+Shift+R） |
| `wrangler` コマンドが見つからない | `npx wrangler` で代替実行 |
