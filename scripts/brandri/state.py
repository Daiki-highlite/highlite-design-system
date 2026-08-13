"""記事の状態を、Slackのリアクションとスレッドコメントから決定論的に判定する。

判定は上から順に評価し、最初に一致したもので確定する（仕様書 3.2）。
LLMは一切使わない。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from . import util


@dataclass
class Decision:
    status: str
    # revision_requested のとき、未処理コメント [{ts, text}]
    unprocessed_comments: list[dict] = field(default_factory=list)
    # 承認者（bot以外の +1 を押したユーザーID）
    approvers: set[str] = field(default_factory=set)
    # manual公開の finalize 用：スレッドに現れた公開URL（人が貼ったもの）
    published_url: str | None = None


def decide(parent_reactions: dict[str, set[str]],
           thread: list[dict],
           cfg,
           bot_user_id: str,
           posted_at: datetime,
           now: datetime | None = None,
           scheduled_date: str | None = None) -> Decision:
    now = now or util.now_jst()
    R = cfg["reactions"]

    def reacted(name: str) -> set[str]:
        return parent_reactions.get(name, set())

    # bot以外の承認
    approvers = reacted(R["approved"]) - {bot_user_id}

    # 未処理コメント：親を除く返信のうち、bot投稿でなく ☑️ が付いていないもの
    parent_ts = thread[0]["ts"] if thread else None
    unprocessed = []
    published_url = None
    for m in thread:
        if m["ts"] == parent_ts:
            continue
        if m["user"] == bot_user_id:
            continue
        handled = R["comment_handled"] in m["reactions"]
        # 公開URLを含む人の返信は finalize シグナル（manualモード）
        url = util.contains_url(m["text"])
        if url and not handled:
            published_url = url
        if not handled and not url:
            unprocessed.append({"ts": m["ts"], "text": m["text"]})

    age_days = (now - posted_at).days

    # 1. ボツ
    if reacted(R["dropped"]):
        return Decision("dropped", approvers=approvers)
    # 2. 公開済み
    if reacted(R["published"]):
        return Decision("published", approvers=approvers)
    # 3. 鮮度切れ
    if age_days > cfg.get("cadence.ttl_days", 28):
        return Decision("expired", approvers=approvers)
    # 4. 公開機会を逃した（案A: 予定日当日は生かす → 予定日を過ぎたら missed）
    if scheduled_date:
        try:
            sd = datetime.fromisoformat(scheduled_date).date()
            if now.date() > sd:
                return Decision("missed", approvers=approvers)
        except ValueError:
            pass
    # 5. 未処理コメント
    if unprocessed:
        return Decision("revision_requested", unprocessed_comments=unprocessed,
                        approvers=approvers)
    # 6/7. 承認あり
    if approvers:
        if reacted(R["scheduled"]):
            return Decision("scheduled", approvers=approvers, published_url=published_url)
        return Decision("approved", approvers=approvers, published_url=published_url)
    # 8. レビュー中
    if reacted(R["reviewing"]):
        return Decision("reviewing")
    # 9. 未着手
    return Decision("draft")
