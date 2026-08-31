---
description: 修正依頼を本文に反映した後、Slackのレビューを閉じる（version+1・☑️付与）
---

# /brandri-resolve

修正依頼コメントを本文（md）に反映し終えたら実行する。Slack側の後処理だけを行う。

```
python -m scripts.brandri.resolve marketing/articles/brandri/drafts/<file>.md --note "②の切り口を差し替え、③をリアリス案件に変更"
```

- version を +1
- スレッドに「修正を反映しました（v{n}）」を返信（--note があれば変更点を添える）
- 👍が付いた状態なら「承認を取り消す場合は👍を外してください」を添える
- 未処理の人コメントすべてに ☑️ を付ける（次回syncで再検出されない）

**先に本文mdを直しておくこと。** このコマンドは本文を書き換えない。
