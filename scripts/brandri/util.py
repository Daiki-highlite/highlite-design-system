"""日付・スケジュール・文字列ユーティリティ。すべてJST基準。"""
from __future__ import annotations

import re
import unicodedata
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=9))

_WEEKDAY = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}


def now_jst() -> datetime:
    return datetime.now(JST)


def ts_to_dt(ts: str) -> datetime:
    """Slackの ts（'1786000068.011519'）をJSTのdatetimeに変換。"""
    return datetime.fromtimestamp(float(ts), JST)


def weekday_name(dt: datetime) -> str:
    for name, idx in _WEEKDAY.items():
        if idx == dt.weekday():
            return name
    return "Mon"


def is_weekday(dt: datetime, name: str) -> bool:
    return dt.weekday() == _WEEKDAY[name]


def next_weekday_on_or_after(base: datetime, target: str) -> datetime:
    """base以降で最初に来る target 曜日の日付（00:00 JST）を返す。"""
    target_idx = _WEEKDAY[target]
    d = base.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = (target_idx - d.weekday()) % 7
    return d + timedelta(days=delta)


def compute_scheduled_date(posted_at: datetime, lead_days: int, publish_day: str) -> datetime:
    """投稿日 + lead_days 以降で最初の publish_day を公開予定日とする。"""
    earliest = posted_at + timedelta(days=lead_days)
    return next_weekday_on_or_after(earliest, publish_day)


def jp_date(dt: datetime) -> str:
    """2026-08-20（木）形式。"""
    wd = ["月", "火", "水", "木", "金", "土", "日"][dt.weekday()]
    return f"{dt:%Y-%m-%d}（{wd}）"


def slugify(text: str, maxlen: int = 40) -> str:
    """タイトルからファイル名用スラグを作る。日本語はローマ字化せず英数記号のみ抽出、
    残らなければ日付側で一意性を担保する前提で 'article' を返す。"""
    text = unicodedata.normalize("NFKC", text)
    ascii_part = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    if ascii_part:
        return ascii_part[:maxlen].strip("-")
    return "article"


def contains_url(text: str) -> str | None:
    m = re.search(r"https?://[^\s|>]+", text or "")
    return m.group(0) if m else None
