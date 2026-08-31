"""Slack Web API クライアント（bot token 使用）。

決定論的に叩くだけの薄いラッパー。エラーは即例外にする。
"""
from __future__ import annotations

import time
from typing import Any

import requests

API = "https://slack.com/api"


class SlackError(RuntimeError):
    pass


class Slack:
    def __init__(self, token: str):
        self._h = {"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json; charset=utf-8"}

    # --- 内部 ---
    def _post(self, method: str, payload: dict) -> dict:
        for attempt in range(4):
            r = requests.post(f"{API}/{method}", headers=self._h, json=payload, timeout=30)
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", "2")))
                continue
            data = r.json()
            if not data.get("ok"):
                raise SlackError(f"{method} failed: {data.get('error')}")
            return data
        raise SlackError(f"{method}: rate limited too many times")

    def _get(self, method: str, params: dict) -> dict:
        for attempt in range(4):
            r = requests.get(f"{API}/{method}", headers=self._h, params=params, timeout=30)
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", "2")))
                continue
            data = r.json()
            if not data.get("ok"):
                raise SlackError(f"{method} failed: {data.get('error')}")
            return data
        raise SlackError(f"{method}: rate limited too many times")

    # --- 認証 ---
    def whoami(self) -> str:
        return self._get("auth.test", {})["user_id"]

    # --- 投稿 ---
    def post(self, channel: str, text: str, blocks: list | None = None,
             thread_ts: str | None = None) -> str:
        payload: dict[str, Any] = {"channel": channel, "text": text}
        if blocks:
            payload["blocks"] = blocks
        if thread_ts:
            payload["thread_ts"] = thread_ts
        return self._post("chat.postMessage", payload)["ts"]

    def permalink(self, channel: str, ts: str) -> str:
        return self._get("chat.getPermalink",
                         {"channel": channel, "message_ts": ts})["permalink"]

    # --- リアクション ---
    def add_reaction(self, channel: str, ts: str, name: str) -> None:
        try:
            self._post("reactions.add", {"channel": channel, "timestamp": ts, "name": name})
        except SlackError as e:
            if "already_reacted" not in str(e):
                raise

    def remove_reaction(self, channel: str, ts: str, name: str) -> None:
        try:
            self._post("reactions.remove", {"channel": channel, "timestamp": ts, "name": name})
        except SlackError as e:
            if "no_reaction" not in str(e):
                raise

    def get_reactions(self, channel: str, ts: str) -> dict[str, set[str]]:
        """親メッセージのリアクションを {emoji_name: {user_id,...}} で返す。"""
        data = self._get("reactions.get", {"channel": channel, "timestamp": ts, "full": "true"})
        msg = data.get("message", {})
        out: dict[str, set[str]] = {}
        for r in msg.get("reactions", []):
            out[r["name"]] = set(r.get("users", []))
        return out

    # --- スレッド ---
    def thread(self, channel: str, ts: str) -> list[dict]:
        """親＋返信を配列で返す。各要素は {ts, user, text, reactions:{name:set}}。"""
        out: list[dict] = []
        cursor = None
        while True:
            params = {"channel": channel, "ts": ts, "limit": 200}
            if cursor:
                params["cursor"] = cursor
            data = self._get("conversations.replies", params)
            for m in data.get("messages", []):
                reactions = {r["name"]: set(r.get("users", [])) for r in m.get("reactions", [])}
                out.append({"ts": m.get("ts"), "user": m.get("user"),
                            "text": m.get("text", ""), "reactions": reactions})
            if data.get("has_more") and data.get("response_metadata", {}).get("next_cursor"):
                cursor = data["response_metadata"]["next_cursor"]
            else:
                break
        return out
