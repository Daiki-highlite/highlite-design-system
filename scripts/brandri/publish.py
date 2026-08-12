"""木曜: 本日が公開予定日の記事を、最終リアクション確認のうえ公開する。

publish.mode:
  manual   → 公開用原稿をスレッドに出し、人の入稿を促す（✅は付けない。
             入稿後にURLをスレッド返信 → 次のsyncがfinalize）
  repo_pr  → 未実装（プレースホルダ）
  cms_api  → 未実装（プレースホルダ）

使い方: python -m scripts.brandri.publish [--force]
"""
from __future__ import annotations

import sys
from datetime import datetime

from . import articles, util
from .config import load, require_env
from .slack import Slack


def main() -> None:
    force = "--force" in sys.argv
    cfg = load()
    now = util.now_jst()
    pub_day = cfg.get("cadence.publish_day", "Thu")
    if not force and not util.is_weekday(now, pub_day):
        print(f"本日は公開日（{pub_day}）ではありません。終了。")
        return

    channel = cfg.get("slack.channel_id")
    bot_id = cfg.get("slack.bot_user_id")
    slack = Slack(require_env("SLACK_BOT_TOKEN"))
    R = cfg["reactions"]
    mode = cfg.get("publish.mode", "manual")
    today = now.date().isoformat()

    targets = []
    for path, post in articles.iter_active(cfg):
        if post.get("status") != "scheduled":
            continue
        if (post.get("schedule") or {}).get("scheduled_date") == today:
            targets.append((path, post))

    if not targets:
        print("本日の公開対象はありません。")
        return

    for path, post in targets:
        ts = (post.get("slack") or {}).get("ts")
        # --- 最終確認（状態ファイルを信用せず今のリアクションを取り直す）---
        reactions = slack.get_reactions(channel, ts)
        approvers = reactions.get(R["approved"], set()) - {bot_id}
        dropped = bool(reactions.get(R["dropped"]))
        if dropped or not approvers:
            slack.remove_reaction(channel, ts, R["scheduled"])
            slack.post(channel, "👍が取り消されたため、本日の公開をキャンセルしました。", thread_ts=ts)
            sched = post.get("schedule") or {}
            sched["scheduled_date"] = None
            post["schedule"] = sched
            post["status"] = "draft"
            articles.save(post, path)
            articles.move(path, cfg.path("drafts"))
            print(f"キャンセル: {post.get('id')}")
            continue

        if mode == "manual":
            _publish_manual(cfg, slack, channel, post, ts)
            print(f"公開用原稿を提示: {post.get('id')}（入稿後URLをスレッドに返信してください）")
        elif mode == "repo_pr":
            raise SystemExit("publish.mode=repo_pr は未実装です")
        elif mode == "cms_api":
            raise SystemExit("publish.mode=cms_api は未実装です")
        else:
            raise SystemExit(f"未知の publish.mode: {mode}")


def _publish_manual(cfg, slack, channel, post, ts):
    """最終原稿（front matter除去済み）をスレッドに出す。✅ はまだ付けない。"""
    title = post.get("title", "")
    body = post.content.strip()
    header = f"*本日が公開予定日です。以下の原稿で brandri.jp に入稿してください。*\n" \
             f"入稿後、このスレッドに公開URLを返信すると ✅ を付けて完了します。\n\n" \
             f"— — —\n# {title}\n\n"
    # Slackメッセージ長の上限に配慮して分割
    chunk = header + body
    for part in _split(chunk, 3500):
        slack.post(channel, part, thread_ts=ts)


def _split(text: str, size: int):
    lines = text.split("\n")
    buf, cur = [], 0
    for ln in lines:
        if cur + len(ln) + 1 > size and buf:
            yield "\n".join(buf)
            buf, cur = [], 0
        buf.append(ln)
        cur += len(ln) + 1
    if buf:
        yield "\n".join(buf)


if __name__ == "__main__":
    main()
