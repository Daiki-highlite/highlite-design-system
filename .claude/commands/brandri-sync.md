---
description: Slackのリアクション・コメントを同期する（承認→予約、キャンセル、公開URL確定、修正待ちの報告）
---

# /brandri-sync

Slackのbotトークンで状態を同期する決定論的スクリプトを実行する。

```
python -m scripts.brandri.sync
```

## やること（API不使用・Slackのみ）
- 👍 が付いた記事 → 🗓️ を付けて公開予定日をスレッドにコメント → scheduled/へ
- 予約済みで 👍 が消えた → 公開キャンセル
- 🗑️ → dropped/へ、鮮度切れ → 取り下げ
- 公開URLが人から返信された → ✅ を付けて published/へ
- 未着手の放置 → リマインド1回

## 修正依頼について
スレッドにコメントが付いた記事は「修正待ち」として**報告されるだけ**。
本文の書き直しは Claude Code で行う：

1. 該当mdを開き、スレッドのコメント内容を反映して本文を直す（/brandri-draft の文体・構成に従う）
2. 反映できたら Slack 側を閉じる：
   ```
   python -m scripts.brandri.resolve marketing/articles/brandri/drafts/<file>.md --note "変更点"
   ```
   → version+1、スレッドに反映報告、コメントに ☑️ が付く
