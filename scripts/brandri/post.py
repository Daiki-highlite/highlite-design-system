"""人（Claude Code / このチャット）が書いたドラフトmdを、botとしてSlackに投稿する。

案B: 記事の選定・執筆はProのClaude側で行い、投稿だけをこのスクリプトが担う。
Anthropic APIは使わない。必要なのは SLACK_BOT_TOKEN のみ。

使い方:
  python -m scripts.brandri.post marketing/articles/brandri/drafts/2026-08-13-xxx.md
"""
from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

from . import articles, util
from .config import load, require_env, ROOT
from .slack import Slack


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("使い方: python -m scripts.brandri.post <draft.md>")
    path = Path(sys.argv[1]).resolve()
    if not path.exists():
        raise SystemExit(f"ファイルが見つかりません: {path}")

    cfg = load()
    channel = cfg.get("slack.channel_id")
    post = articles.load(path)

    if (post.get("slack") or {}).get("ts"):
        raise SystemExit("この記事はすでにSlackへ投稿済みです（front matterにslack.tsあり）")
    if not post.content.strip():
        raise SystemExit("本文が空です。執筆してから投稿してください")
    title = post.get("title")
    if not title:
        raise SystemExit("front matter に title がありません")

    # --- front matter の既定値を補完 ---
    now = util.now_jst()
    post["status"] = "draft"
    if "version" not in post.metadata:
        post["version"] = 1
    if "target_cluster" not in post.metadata:
        post["target_cluster"] = "startup"
    if "keywords" not in post.metadata:
        post["keywords"] = []
    if "review" not in post.metadata:
        post["review"] = {"approved_by": [], "revision_rounds": 0}

    scheduled = util.compute_scheduled_date(
        now, cfg.get("cadence.publish_lead_days", 8), cfg.get("cadence.publish_day", "Thu"))
    sched = post.get("schedule") or {}
    sched.setdefault("posted_at", now.isoformat())
    sched.setdefault("expires_at", (now + timedelta(days=cfg.get("cadence.ttl_days", 28))).date().isoformat())
    sched.setdefault("scheduled_date", scheduled.date().isoformat())
    sched.setdefault("published_at", None)
    sched.setdefault("published_url", None)
    post["schedule"] = sched
    if not post.get("id"):
        post["id"] = articles.make_id(now)

    # --- Slack投稿 ---
    slack = Slack(require_env("SLACK_BOT_TOKEN"))
    blocks, text = build_blocks(cfg, post, path, scheduled)
    ts = slack.post(channel, text, blocks=blocks)
    link = slack.permalink(channel, ts)
    post["slack"] = {"channel": channel, "ts": ts, "permalink": link}
    articles.save(post, path)

    _append_selection_log(cfg, now, post)

    print(f"投稿完了: {title}")
    print(f"  {link}")
    print(f"  公開予定: {util.jp_date(scheduled)}")


def build_blocks(cfg, post, path: Path, scheduled):
    """レビュー依頼の親投稿ブロックを組み立てる。本文全文は載せずGitHubリンクへ誘導。"""
    repo_base = cfg.get("repo.blob_base", "")
    try:
        rel = path.resolve().relative_to(ROOT)
        gh_url = f"{repo_base}/{rel}" if repo_base else str(path)
    except ValueError:
        gh_url = str(path)

    lead = post.content.strip().split("\n\n")[0][:200]
    kw = ", ".join(post.get("keywords", []))
    sel = post.get("selection") or {}
    pid = post.get("id", "")
    text = f"📄 今週のBrandri記事ドラフト {pid}｜{post.get('title','')}"

    sel_line = ""
    if sel:
        considered = sel.get("candidates_considered")
        score = sel.get("score")
        head = "*選定*"
        if considered and score is not None:
            head += f" 候補{considered}本中 スコア{score}/10"
        sel_line = f"{head}\n{sel.get('rationale','')}"

    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"📄 {post.get('title','')}", "emoji": True}},
        {"type": "context", "elements": [
            {"type": "mrkdwn",
             "text": f"`{pid}`  ｜  v{post.get('version',1)}  ｜  想定読者: {post.get('target_cluster','')}"}]},
        {"type": "section", "text": {"type": "mrkdwn", "text": lead}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*キーワード*\n{kw or '—'}"},
            {"type": "mrkdwn", "text": f"*公開予定*\n{util.jp_date(scheduled)}"}]},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*📝 本文を読む*\n{gh_url}"}},
    ]
    if sel_line:
        blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": sel_line}]})
    blocks += [
        {"type": "divider"},
        {"type": "context", "elements": [
            {"type": "mrkdwn",
             "text": ":eyes: レビュー開始 ／ :+1: 承認 ／ :wastebasket: ボツ\n"
                     "修正依頼はこの投稿のスレッドにコメントしてください（反映後 :ballot_box_with_check: を付けます）"}]},
    ]
    return blocks, text


def _append_selection_log(cfg, now, post):
    sel = post.get("selection") or {}
    if not sel:
        return
    log = cfg.path("selection_log")
    log.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"\n## {util.jp_date(now)}",
             f"**選定：** {post.get('id')}  {post.get('title','')}",
             f"スコア {sel.get('score','-')}/10  {sel.get('rationale','')}"]
    rejected = sel.get("rejected") or []
    if rejected:
        lines.append("**見送り：**")
        for r in rejected:
            lines.append(f"- {r.get('path')}（{r.get('score')}）: {r.get('reason')}")
    with open(log, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
