"""Slackのリアクション・コメントを読み、記事の状態を同期する（案B・API不使用）。

決定論的な処理のみ:
  - approved          → 🗓️付与・予定日コメント・scheduled/へ移動
  - scheduled         → 👍存続を再確認。消えていればキャンセル
  - dropped/expired   → dropped/へ移動
  - 公開URLの人返信を検出 → finalize（✅・published/へ）
  - draft放置          → リマインド1回

修正依頼（revision_requested）は「報告するだけ」。本文の書き直しは
Claude Code / このチャット側で md を編集し、`resolve` コマンドで閉じる。

使い方: python -m scripts.brandri.sync
"""
from __future__ import annotations

from datetime import datetime

from . import articles, state, util
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
    pending_revisions: list[str] = []

    for path, post in articles.iter_active(cfg):
        ts = (post.get("slack") or {}).get("ts")
        if not ts:
            continue
        posted_at = _posted_at(post)
        reactions = slack.get_reactions(channel, ts)
        thread = slack.thread(channel, ts)
        d = state.decide(reactions, thread, cfg, bot_id, posted_at)
        before = post.get("status")

        if d.status == "dropped":
            _save_status(post, "dropped"); articles.save(post, path)
            articles.move(path, cfg.path("dropped"))
        elif d.status == "expired":
            slack.post(channel, f"投稿から{cfg.get('cadence.ttl_days',28)}日経過したため、鮮度切れとして取り下げます。", thread_ts=ts)
            _save_status(post, "expired"); articles.save(post, path)
            articles.move(path, cfg.path("dropped"))
        elif d.status == "revision_requested":
            _save_status(post, "revision_requested"); articles.save(post, path)
            n = len(d.unprocessed_comments)
            pending_revisions.append(f"- {post.get('id')} 「{post.get('title','')[:24]}」 未処理コメント{n}件 → 本文を直して resolve を実行")
        elif d.status == "approved":
            path = _schedule(cfg, slack, channel, path, post, ts)
        elif d.status == "scheduled":
            path = _check_scheduled(cfg, slack, channel, path, post, d, ts)
        elif d.status == "draft":
            _remind_if_stale(cfg, slack, channel, post, ts); _save_status(post, "draft"); articles.save(post, path)
        else:
            _save_status(post, d.status); articles.save(post, path)

        after = articles.load(path).get("status") if path.exists() else d.status
        if before != after:
            report.append(f"| {post.get('id')} | {post.get('title','')[:24]} | {after} | {before}->{after} |")

    _print_report(cfg, report, pending_revisions)


def _posted_at(post) -> datetime:
    p = (post.get("schedule") or {}).get("posted_at")
    if p:
        return datetime.fromisoformat(p)
    ts = (post.get("slack") or {}).get("ts")
    return util.ts_to_dt(ts) if ts else util.now_jst()


def _save_status(post, status):
    post["status"] = status


def _remind_if_stale(cfg, slack, channel, post, ts):
    age = (util.now_jst() - _posted_at(post)).days
    if age >= cfg.get("cadence.reminder_after_days", 4) and not post.get("_reminded"):
        slack.post(channel, "レビュー未着手のままです。👀 で開始してください🙏", thread_ts=ts)
        post["_reminded"] = True


def _schedule(cfg, slack, channel, path, post, ts):
    R = cfg["reactions"]
    sched = post.get("schedule") or {}
    if not sched.get("scheduled_date"):
        dt = util.compute_scheduled_date(
            _posted_at(post), cfg.get("cadence.publish_lead_days", 8), cfg.get("cadence.publish_day", "Thu"))
        sched["scheduled_date"] = dt.date().isoformat()
    post["schedule"] = sched
    if R["scheduled"] not in slack.get_reactions(channel, ts):
        slack.add_reaction(channel, ts, R["scheduled"])
        dt = datetime.fromisoformat(sched["scheduled_date"]).replace(tzinfo=util.JST)
        slack.post(channel, f"公開予定日：{util.jp_date(dt)}", thread_ts=ts)
    _save_status(post, "scheduled"); articles.save(post, path)
    return articles.move(path, cfg.path("scheduled"))


def _check_scheduled(cfg, slack, channel, path, post, d, ts):
    R = cfg["reactions"]
    if d.published_url:
        return _finalize(cfg, slack, channel, path, post, ts, d.published_url)
    if not d.approvers:
        slack.remove_reaction(channel, ts, R["scheduled"])
        sd = (post.get("schedule") or {}).get("scheduled_date", "")
        try:
            label = util.jp_date(datetime.fromisoformat(sd).replace(tzinfo=util.JST))
        except Exception:
            label = sd
        slack.post(channel, f"👍が取り消されたため、{label}の公開予定をキャンセルしました。", thread_ts=ts)
        sched = post.get("schedule") or {}; sched["scheduled_date"] = None; post["schedule"] = sched
        _save_status(post, "reviewing" if R["reviewing"] in slack.get_reactions(channel, ts) else "draft")
        articles.save(post, path)
        return articles.move(path, cfg.path("drafts"))
    _save_status(post, "scheduled"); articles.save(post, path)
    return path


def _finalize(cfg, slack, channel, path, post, ts, url):
    R = cfg["reactions"]
    sched = post.get("schedule") or {}
    sched["published_at"] = util.now_jst().isoformat()
    sched["published_url"] = url
    post["schedule"] = sched
    _save_status(post, "published"); articles.save(post, path)
    slack.add_reaction(channel, ts, R["published"])
    slack.post(channel, f"公開を確認しました：{url}", thread_ts=ts)
    return articles.move(path, cfg.path("published"))


def _print_report(cfg, rows, pending_revisions):
    print(f"## Brandri レビュー同期 {util.jp_date(util.now_jst())}\n")
    if rows:
        print("| ID | タイトル | 状態 | 変化 |")
        print("|---|---|---|---|")
        print("\n".join(rows))
    else:
        print("状態変化なし。")
    if pending_revisions:
        print("\n### 修正待ち（本文を直して resolve を実行してください）")
        print("\n".join(pending_revisions))


if __name__ == "__main__":
    main()
