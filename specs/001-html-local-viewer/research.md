# Research: Cloudflare Pages への静的HTML公開

**Date**: 2026-06-19
**Feature**: kgi-sales-tasks.html の外部公開

---

## デプロイアプローチの比較

### 選択肢 A: Wrangler CLI（採用）

- **決定**: `wrangler pages deploy` コマンドで単一コマンドデプロイ
- **理由**:
  - ローカルから即時デプロイ可能
  - ファイル更新も同じコマンドで再デプロイできる
  - npm経由でインストール可能（追加ツール不要）
- **制約**: 初回のみ `wrangler login` でCloudflare認証が必要

### 選択肢 B: Cloudflare Dashboard（手動アップロード）

- **却下理由**: GUIからのファイルアップロードは毎回手動操作が必要で、繰り返し更新に非効率

### 選択肢 C: GitHub連携（自動デプロイ）

- **却下理由**: GitHubリポジトリへのpushが必須となり、今回のスコープ（単体HTMLの公開）に対して過剰

---

## デプロイディレクトリの構成

Cloudflare Pagesはディレクトリ全体を公開する仕組みのため、HTMLファイルを格納した専用ディレクトリを用意する。

```
deploy/
└── index.html   ← kgi-sales-tasks.html をコピー or シンボリックリンク
```

`index.html` という名前にすることで、URLが `/index.html` なしでルートアクセスできる（例: `https://xxx.pages.dev/`）。

---

## Cloudflare Pages 無料枠の制約

| 制限項目 | 無料枠 |
|----------|--------|
| ファイルサイズ上限 | 25MB/ファイル |
| ファイル数上限 | 20,000ファイル/プロジェクト |
| カスタムドメイン | 1つまで |
| デプロイ数 | 500回/月 |

→ 今回の用途（単体HTML）は全制約内に収まる

---

## 結論

- Wrangler CLI を使って `deploy/` ディレクトリをデプロイする
- `kgi-sales-tasks.html` を `deploy/index.html` としてコピーして使用
- 初回: `wrangler login` → `wrangler pages deploy deploy/`
- 更新時: ファイルコピー → `wrangler pages deploy deploy/` の繰り返し
