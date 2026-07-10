# Implementation Plan: Cloudflare Pages HTML 外部公開

**Branch**: `001-html-cloudflare-deploy` | **Date**: 2026-06-19 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-html-local-viewer/spec.md`

## Summary

`kgi-sales-tasks.html` を Cloudflare Pages に Wrangler CLI でデプロイし、パブリックURLで外部公開できる状態を構築する。デプロイ用の `deploy/` ディレクトリを用意し、HTMLをそこにコピーして単一コマンドで公開・更新できる仕組みを作る。

## Technical Context

**Language/Version**: なし（静的HTML）

**Primary Dependencies**: Wrangler CLI（Cloudflare公式CLI）、Node.js（Wrangler実行に必要）

**Storage**: N/A

**Testing**: ブラウザによる手動確認

**Target Platform**: Cloudflare Pages（グローバルCDN）

**Project Type**: 静的サイトホスティング

**Performance Goals**: Cloudflare CDNデフォルト（グローバル低レイテンシ）

**Constraints**: 無料枠内（25MB/ファイル、500デプロイ/月）

**Scale/Scope**: 単体HTMLファイル1つの公開

## Constitution Check

*構成ファイル（constitution.md）未定義のためスキップ*

全要件が静的ファイルのみで完結するため、セキュリティ・プライバシー・スケーラビリティ上の懸念なし。

## Project Structure

### Documentation (this feature)

```text
specs/001-html-local-viewer/
├── spec.md           ✅ 完了
├── plan.md           ✅ このファイル
├── research.md       ✅ 完了
├── quickstart.md     ✅ 完了
└── tasks.md          → speckit-tasks で生成
```

### Source Code（追加ファイル）

```text
deploy/
└── index.html        ← kgi-sales-tasks.html のコピー（デプロイ対象）
```

**Structure Decision**: プロジェクトルートに `deploy/` ディレクトリを作成し、HTMLファイルをそこに配置してCloudflare Pagesのデプロイ対象とする。既存の `marketing/kgi_strategy/` 構造はそのまま維持する。

## 実装ステップ概要

### Step 1: Node.js 確認（前提）
- Node.js がインストール済みであることを確認（`node -v`）

### Step 2: Wrangler CLI セットアップ
- `npm install -g wrangler` でWrangler CLIをインストール
- `wrangler login` でCloudflareアカウントに認証

### Step 3: deploy ディレクトリ準備
- プロジェクトルートに `deploy/` ディレクトリを作成
- `kgi-sales-tasks.html` を `deploy/index.html` としてコピー

### Step 4: 初回デプロイ
- `wrangler pages deploy deploy/ --project-name highlite-sales-tasks` を実行
- 発行されたURLを確認

### Step 5: 更新フロー（再デプロイ）
- HTMLファイルを編集後、`deploy/index.html` を上書きコピー
- `wrangler pages deploy deploy/ --project-name highlite-sales-tasks` を再実行

## Complexity Tracking

制約違反なし。
