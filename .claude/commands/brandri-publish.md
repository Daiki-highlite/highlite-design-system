---
description: 承認済み記事をBrandriのarticles.jsonに投入して公開する（木曜）
---

# /brandri-publish

承認された記事を Brandri（別リポジトリ）に投入し、ビルドして公開する。

## 前提

Brandri リポジトリがローカルにあること。既定の想定パス：
`/Users/toto/Documents/vscode/Brandri`

## 手順

### 1. 公開対象を確認

```
python -m scripts.brandri.publish
```
本日が公開予定日で、👍が残っている記事を確認する。
👍が取り消されていればここでキャンセルされる。

### 2. Brandri形式のJSONに変換

```
python -m scripts.brandri.to_brandri marketing/articles/brandri/scheduled/<file>.md
```
→ 同じ場所に `<file>.brandri.json` が出力される。

出力時に警告が出たら対処する：
- `sections が3節未満` → 投入時に落ちる。本文の章立てを直す
- `related が未設定` → 警告のみ。3本入れておくのが望ましい

### 3. Brandri に投入

```
cd /Users/toto/Documents/vscode/Brandri
node scripts/write-knowledge.mjs <上で出力したjsonのパス> --next-num
```
`--next-num` で第3トラック（401〜）の次番号が自動採番される。

検証に落ちた場合 articles.json は一切変更されない。エラーを直して再実行する。

### 4. ビルドして公開

```
node scripts/build-data.mjs
git add -A && git commit -m "brandri: add article" && git push
```

### 5. Slackに公開URLを返信

公開されたURL（`https://brandri.jp/articles/<slug>.html`）を、
該当記事のSlackスレッドに返信する。

次の `sync` がURLを検出して ✅ を付け、`published/` へ移動して完了。

## 取り下げる場合の片付け

投入後にボツにするときは、以下をセットで行う：

1. `articles.json` から該当記事を削除（または `git checkout`）
2. `node scripts/build-data.mjs` で再ビルド（記事HTMLは自動削除される）
3. **`project/assets/thumbs/j-<slug>.svg` を手動削除**
   （再ビルドでは消えないため、放置すると孤児ファイルが溜まる）
