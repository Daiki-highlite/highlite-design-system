"""修正依頼の反映後に、Slack側のレビューを閉じる（案B）。

本文の書き直しは Claude Code / このチャット側で md を直接編集して済ませておく。
このスクリプトは Slack の後処理だけを行う:
  - version を +1
  - スレッドに「修正を反映しました（v{n}）」を返信（--note で変更点を添えられる）
  - 未処理の人コメントすべてに ☑️ を付ける（次回syncで再検出されないように）

使い方:
  python -m scripts.brandri.resolve <draft.md> --note "②の切り口を差し替え"
"""
from __future__ import annotations

import sys
from pathlib import Path

from . import articles
from .config import load, require_env
from .slack import Slack


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    note = ""
    if "--note" in sys.argv:
        i = sys.argv.index("--note")
        if i + 1 < len(sys.argv):
            note = sys.argv[i + 1]
    if not args:
        raise SystemExit("使い方: python -m scripts.brandri.resolve <draft.md> [--note '変更点']")

    path = Path(args[0]).resolve()
    if not path.exists():
        raise SystemExit(f"ファイルが見つかりません: {path}")

    cfg = load()
    channel = cfg.get("slack.channel_id")
    bot_id = cfg.get("slack.bot_user_id")
    R = cfg["reactions"]

    post = articles.load(path)
    ts = (post.get("slack") or {}).get("ts")
    if not ts:
        raise SystemExit("この記事はまだSlack未投稿です")

    slack = Slack(require_env("SLACK_BOT_TOKEN"))
    reactions = slack.get_reactions(channel, ts)
    thread = slack.thread(channel, ts)

    # 未処理コメント（bot以外・☑️なし・URLでない）
    parent_ts = thread[0]["ts"] if thread else None
    pending = []
    for m in thread:
        if m["ts"] == parent_ts or m["user"] == bot_id:
            continue
        if R["comment_handled"] in m["reactions"]:
            continue
        pending.append(m)

    # version 更新
    post["version"] = int(post.get("version", 1)) + 1
    rv = post.get("review") or {}
    rv["revision_rounds"] = int(rv.get("revision_rounds", 0)) + 1
    post["review"] = rv
    post["status"] = "reviewing"
    articles.save(post, path)

    # スレッド返信
    msg = f"修正を反映しました（v{post['version']}）"
    if note:
        msg += f"\n\n{note}"
    approved = bool(reactions.get(R["approved"], set()) - {bot_id})
    if approved and cfg.get("review.notify_on_revision_with_approval", True):
        msg += "\n\n👍がついた状態での修正です。内容を確認し、承認を取り消す場合は👍を外してください"
    slack.post(channel, msg, thread_ts=ts)

    # ☑️
    for m in pending:
        slack.add_reaction(channel, m["ts"], R["comment_handled"])

    print(f"修正を反映済みにしました: {post.get('id')}  v{post['version']}")
    print(f"  ☑️ を付けたコメント: {len(pending)}件")


if __name__ == "__main__":
    main()
