"""毎日: Slackのリアクション・コメントを読み、記事の状態を同期する。

- revision_requested → 改稿・スレッド返信・☑️
- approved          → 🗓️付与・予定日コメント・scheduled/へ移動
- scheduled         → 👍存続を再確認。消えていればキャンセル
- dropped/expired   → dropped/へ移動
- manual公開のURL返信を検出 → finalize（✅・published/へ）

使い方: python -m scripts.brandri.sync
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from . import articles, llm, state, util
from .config import load, require_env
from .slack import Slack


def main() -> None:
    cfg = load()
    channel = cfg.get("slack.channel_id")
    bot_id = cfg.get("slack.bot_user_id")
    if not bot_id or bot_id.startswith("U_BOT_PLACEHOLDER"):
        raise SystemExit("slack.bot_user_id が未設定です。setup/slack-app-setup.md を参照。")

    slack = Slack(require_env("SLACK_BOT_TOKEN"))
    R = cfg["reactions"]
    report: list[str] = []

    for path, post in articles.iter_active(cfg):
        sl = post.get("slack") or {}
        ts = sl.get("ts")
        if not ts:
            continue  # まだ投稿されていない
        posted_at = _posted_at(post)
        reactions = slack.get_reactions(channel, ts)
        thread = slack.thread(channel, ts)
        d = state.decide(reactions, thread, cfg, bot_id, posted_at)

        before = post.get("status")
        handler = {
            "dropped": _on_dropped,
            "expired": _on_expired,
            "revision_requested": _on_revision,
            "approved": _on_approved,
            "scheduled": _on_scheduled,
            "reviewing": _on_simple,
            "draft": _on_draft,
            "published": _on_simple,
        }[d.status]
        path = handler(cfg, slack, channel, path, post, d, ts) or path

        after = articles.load(path).get("status") if path.exists() else d.status
        if before != after:
            report.append(f"| {post.get('id')} | {post.get('title','')[:24]} | {after} | {before}→{after} |")

    _print_report(cfg, report)


# --------------------------------------------------------------------------
def _posted_at(post) -> datetime:
    p = (post.get("schedule") or {}).get("posted_at")
    if p:
        return datetime.fromisoformat(p)
    sl = post.get("slack") or {}
    if sl.get("ts"):
        return util.ts_to_dt(sl["ts"])
    return util.now_jst()


def _set_status(post, status):
    post["status"] = status


def _on_simple(cfg, slack, channel, path, post, d, ts):
    _set_status(post, d.status)
    articles.save(post, path)
    return path


def _on_draft(cfg, slack, channel, path, post, d, ts):
    # リマインド（1回だけ）
    posted = _posted_at(post)
    age = (util.now_jst() - posted).days
    if age >= cfg.get("cadence.reminder_after_days", 4) and not post.get("_reminded"):
        slack.post(channel, "レビュー未着手のままです。👀 で開始してください🙏", thread_ts=ts)
        post["_reminded"] = True
    _set_status(post, "draft")
    articles.save(post, path)
    return path


def _on_dropped(cfg, slack, channel, path, post, d, ts):
    _set_status(post, "dropped")
    articles.save(post, path)
    return articles.move(path, cfg.path("dropped"))


def _on_expired(cfg, slack, channel, path, post, d, ts):
    days = cfg.get("cadence.ttl_days", 28)
    slack.post(channel, f"投稿から{days}日経過したため、鮮度切れとして取り下げます。", thread_ts=ts)
    _set_status(post, "expired")
    articles.save(post, path)
    return articles.move(path, cfg.path("dropped"))


def _on_revision(cfg, slack, channel, path, post, d, ts):
    comments = [c["text"] for c in d.unprocessed_comments]
    result = llm.revise(post.content, comments, cfg)
    R = cfg["reactions"]

    if result.get("needs_clarification"):
        slack.post(channel, f"確認させてください：{result.get('question','')}", thread_ts=ts)
        # ☑️ は付けない（未処理のまま人の回答を待つ）
        _set_status(post, "revision_requested")
        articles.save(post, path)
        return path

    post.content = result["body_markdown"]
    post["version"] = int(post.get("version", 1)) + 1
    rv = post.get("review") or {}
    rv["revision_rounds"] = int(rv.get("revision_rounds", 0)) + 1
    post["review"] = rv
    _set_status(post, "reviewing")
    articles.save(post, path)

    gh = (post.get("slack") or {}).get("permalink", "")
    approved_now = bool(d.approvers)
    msg = f"修正を反映しました（v{post['version']}）\n\n{result.get('change_summary','')}"
    if approved_now and cfg.get("review.notify_on_revision_with_approval", True):
        msg += "\n\n👍がついた状態での修正です。内容を確認し、承認を取り消す場合は👍を外してください"
    slack.post(channel, msg, thread_ts=ts)

    # 処理済みコメントに ☑️
    for c in d.unprocessed_comments:
        slack.add_reaction(channel, c["ts"], R["comment_handled"])
    return path


def _on_approved(cfg, slack, channel, path, post, d, ts):
    R = cfg["reactions"]
    sched = (post.get("schedule") or {})
    scheduled_date = sched.get("scheduled_date")
    if not scheduled_date:
        posted = _posted_at(post)
        dt = util.compute_scheduled_date(
            posted, cfg.get("cadence.publish_lead_days", 8), cfg.get("cadence.publish_day", "Thu"))
        scheduled_date = dt.date().isoformat()
        sched["scheduled_date"] = scheduled_date
        post["schedule"] = sched

    # 🗓️ と予定日コメントは未通知のときだけ
    if R["scheduled"] not in slack.get_reactions(channel, ts):
        slack.add_reaction(channel, ts, R["scheduled"])
        dt = datetime.fromisoformat(scheduled_date)
        slack.post(channel, f"公開予定日：{util.jp_date(dt.replace(tzinfo=util.JST))}", thread_ts=ts)

    _set_status(post, "scheduled")
    articles.save(post, path)
    return articles.move(path, cfg.path("scheduled"))


def _on_scheduled(cfg, slack, channel, path, post, d, ts):
    R = cfg["reactions"]
    # 公開URLが人から貼られていれば finalize（manualモードのクローズ）
    if d.published_url:
        return _finalize_published(cfg, slack, channel, path, post, ts, d.published_url)

    if not d.approvers:  # 👍が取り消された → キャンセル
        slack.remove_reaction(channel, ts, R["scheduled"])
        sd = (post.get("schedule") or {}).get("scheduled_date", "")
        try:
            label = util.jp_date(datetime.fromisoformat(sd).replace(tzinfo=util.JST))
        except Exception:
            label = sd
        slack.post(channel, f"👍が取り消されたため、{label}の公開予定をキャンセルしました。", thread_ts=ts)
        sched = post.get("schedule") or {}
        sched["scheduled_date"] = None
        post["schedule"] = sched
        _set_status(post, "reviewing" if R["reviewing"] in slack.get_reactions(channel, ts) else "draft")
        articles.save(post, path)
        return articles.move(path, cfg.path("drafts"))

    _set_status(post, "scheduled")
    articles.save(post, path)
    return path


def _finalize_published(cfg, slack, channel, path, post, ts, url):
    R = cfg["reactions"]
    sched = post.get("schedule") or {}
    sched["published_at"] = util.now_jst().isoformat()
    sched["published_url"] = url
    post["schedule"] = sched
    _set_status(post, "published")
    articles.save(post, path)
    slack.add_reaction(channel, ts, R["published"])
    slack.post(channel, f"✅ 公開を確認しました：{url}", thread_ts=ts)
    return articles.move(path, cfg.path("published"))


def _print_report(cfg, rows):
    print(f"## Brandri レビュー同期 {util.jp_date(util.now_jst())}\n")
    if rows:
        print("| ID | タイトル | 状態 | 変化 |")
        print("|---|---|---|---|")
        print("\n".join(rows))
    else:
        print("状態変化なし。")


if __name__ == "__main__":
    main()
