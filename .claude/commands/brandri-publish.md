---
description: 公開予定日の記事を最終確認して公開する（木曜・manualモード）
---

# /brandri-publish

```
python -m scripts.brandri.publish
```

## 流れ
1. 本日が公開予定日の記事を対象に、**その場で** Slackのリアクションを取り直す
2. 👍 が消えている / 🗑️ が付いていれば公開中止 → drafts/へ戻す
3. OKなら（manualモード）公開用の最終原稿をスレッドに出力し、入稿を促す
4. 人が brandri.jp に入稿 → スレッドに公開URLを返信
5. 次の `sync` がURLを検出して ✅ を付け published/ へ

`publish.mode` を repo_pr / cms_api にすれば自動入稿も可能（未実装・入稿方法確定後に対応）。
