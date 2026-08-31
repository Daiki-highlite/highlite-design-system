"""水曜: 直近サマリから1本選定 → 執筆 → Slackへレビュー依頼投稿。

使い方: python -m scripts.brandri.generate [--force]
"""
from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

import frontmatter

from . import articles, llm, util
from .config import load, require_env
from .slack import Slack


def gather_summaries(cfg) -> list[dict]:
    """選定対象: summaries 配下から直近 selection_window_days 日分。
    ファイル名先頭が YYYY-MM-DD 前提。すでに使ったものは source_summaries で除外。"""
    window = cfg.get("cadence.selection_window_days", 7)
    since = util.now_jst() - timedelta(days=window)
    used = _used_summary_paths(cfg)
    out = []
    sdir = cfg.path("summaries")
    for p in sorted(sdir.glob("*.md")):
        # daily サマリのみ対象（brandri/ 配下は除外）
        if "brandri" in p.parts:
            continue
        m = p.name[:10]
        try:
            d = util.datetime.strptime(m, "%Y-%m-%d").replace(tzinfo=util.JST)
        except ValueError:
            continue
        if d < since:
            continue
        rel = str(p.relative_to(cfg.path("summaries").parents[1]))
        if rel in used:
            continue
        out.append({"path": rel, "text": p.read_text(encoding="utf-8")})
    return out


def _used_summary_paths(cfg) -> set[str]:
    used: set[str] = set()
    for key in ("drafts", "scheduled", "published", "dropped"):
        d = cfg.path(key)
        if not d.exists():
            continue
        for p in d.glob("*.md"):
            post = articles.load(p)
            for s in post.get("source_summaries", []) or []:
                used.add(s)
    return used


def main() -> None:
    force = "--force" in sys.argv
    cfg = load()

    now = util.now_jst()
    gen_day = cfg.get("cadence.generation_day", "Wed")
    if not force and not util.is_weekday(now, gen_day):
        print(f"本日は生成日（{gen_day}）ではありません。終了。")
        return

    # 在庫上限チェック
    active = list(articles.iter_active(cfg))
    approved_or_scheduled = [
        p for p in active if p[1].get("status") in ("approved", "scheduled")
    ]
    cap = cfg.get("cadence.max_queue_size", 4)
    if len(approved_or_scheduled) >= cap:
        print(f"公開待ちが上限（{cap}本）に達しています。生成を見送ります。")
        return

    summaries = gather_summaries(cfg)
    if not summaries:
        print("対象サマリがありません。終了。")
        return

    sel = llm.select(summaries, cfg)
    if not sel.get("selected"):
        print("== 記事化見送り ==")
        for r in sel.get("rejected", []):
            print(f"  {r.get('path')}: {r.get('score')} — {r.get('reason')}")
        return

    chosen = next((s for s in summaries if s["path"] == sel["selected"]), None)
    if chosen is None:
        print("選定結果のpathが候補に一致しません。終了。")
        return

    art = llm.write(chosen["text"], sel.get("target_cluster", "startup"), cfg)
    if not art.get("body_markdown"):
        print(f"執筆見送り: {art.get('skip_reason', '一次情報なし')}")
        return

    # --- ドラフト作成 ---
    channel = cfg.get("slack.channel_id")
    posted = now
    scheduled = util.compute_scheduled_date(
        posted, cfg.get("cadence.publish_lead_days", 8), cfg.get("cadence.publish_day", "Thu")
    )
    expires = posted + timedelta(days=cfg.get("cadence.ttl_days", 28))

    post = frontmatter.Post(art["body_markdown"])
    post["id"] = articles.make_id(now)
    post["title"] = art["title"]
    post["status"] = "draft"
    post["version"] = 1
    post["target_cluster"] = sel.get("target_cluster", "startup")
    post["keywords"] = art.get("keywords", [])
    post["selection"] = {
        "score": sel.get("score"),
        "breakdown": sel.get("breakdown", {}),
        "rationale": sel.get("rationale", ""),
        "candidates_considered": sel.get("considered", len(summaries)),
    }
    post["source_summaries"] = [chosen["path"]]
    post["review"] = {"approved_by": [], "revision_rounds": 0}
    post["schedule"] = {
        "posted_at": posted.isoformat(),
        "expires_at": expires.date().isoformat(),
        "scheduled_date": scheduled.date().isoformat(),
        "published_at": None,
        "published_url": None,
    }

    path = articles.new_draft_path(cfg, art["title"], now)
    articles.save(post, path)

    # --- Slack投稿 ---
    slack = Slack(require_env("SLACK_BOT_TOKEN"))
    blocks, text = _build_blocks(cfg, post, art, path, scheduled)
    ts = slack.post(channel, text, blocks=blocks)
    link = slack.permalink(channel, ts)

    post["slack"] = {"channel": channel, "ts": ts, "permalink": link}
    articles.save(post, path)

    _append_selection_log(cfg, now, sel, chosen["path"])

    print(f"投稿完了: {art['title']}")
    print(f"  {link}")
    print(f"  公開予定: {util.jp_date(scheduled)}  スコア {sel.get('score')}/10")


def _build_blocks(cfg, post, art, path: Path, scheduled):
    repo_base = cfg.get("repo.blob_base", "")
    rel = str(path).split("marketing/")[-1]
    gh_url = f"{repo_base}/marketing/{rel}" if repo_base else str(path)
    lead = art["body_markdown"].strip().split("\n\n")[0][:200]
    kw = ", ".join(post.get("keywords", []))
    text = f"📄 今週のBrandri記事ドラフト {post['id']}｜{art['title']}"
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"📄 {art['title']}", "emoji": True}},
        {"type": "context", "elements": [
            {"type": "mrkdwn",
             "text": f"`{post['id']}`  ｜  v{post['version']}  ｜  想定読者: {post['target_cluster']}"}]},
        {"type": "section", "text": {"type": "mrkdwn", "text": lead}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*キーワード*\n{kw}"},
            {"type": "mrkdwn", "text": f"*公開予定*\n{util.jp_date(scheduled)}"}]},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*📝 本文を読む*\n{gh_url}"}},
        {"type": "context", "elements": [
            {"type": "mrkdwn",
             "text": f"*選定* 候補{post['selection']['candidates_considered']}本中 "
                     f"スコア{post['selection']['score']}/10\n{post['selection']['rationale']}"}]},
        {"type": "divider"},
        {"type": "context", "elements": [
            {"type": "mrkdwn",
             "text": ":eyes: レビュー開始 ／ :+1: 承認 ／ :wastebasket: ボツ\n"
                     "修正依頼はこの投稿のスレッドにコメントしてください（反映後 :ballot_box_with_check: を付けます）"}]},
    ]
    return blocks, text


def _append_selection_log(cfg, now, sel, chosen_path):
    log = cfg.path("selection_log")
    log.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"\n## {util.jp_date(now)}\n",
             f"**選定：** {chosen_path}",
             f"スコア {sel.get('score')}/10  {sel.get('rationale','')}\n",
             "**見送り：**"]
    for r in sel.get("rejected", []):
        lines.append(f"- {r.get('path')}（{r.get('score')}）: {r.get('reason')}")
    with open(log, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
