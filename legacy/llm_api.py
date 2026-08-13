"""Anthropic API 呼び出し（選定スコアリング・執筆・改稿）。

判断が要る部分だけをここに閉じ込める。状態遷移やSlack入出力はここを通さない。
プロンプトの本体は .claude/agents/brandri-writer.md と skills/_shared/*.md を
そのまま読み込んで system プロンプトに使う（＝運用ドキュメントが唯一の真実）。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import requests

from .config import ROOT, require_env

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"


def _headers() -> dict:
    return {
        "x-api-key": require_env("ANTHROPIC_API_KEY"),
        "anthropic-version": API_VERSION,
        "content-type": "application/json",
    }


def _call(model: str, system: str, user: str, max_tokens: int = 4000) -> str:
    body = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    r = requests.post(API_URL, headers=_headers(), json=body, timeout=180)
    if r.status_code != 200:
        raise RuntimeError(f"Anthropic API error {r.status_code}: {r.text[:500]}")
    data = r.json()
    return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")


def _load_context() -> str:
    """執筆エージェントのプロンプトと共有ナレッジを結合して返す。"""
    parts: list[str] = []
    writer = ROOT / ".claude" / "agents" / "brandri-writer.md"
    if writer.exists():
        parts.append(writer.read_text(encoding="utf-8"))
    shared_dir = ROOT / "skills" / "_shared"
    if shared_dir.exists():
        for md in sorted(shared_dir.glob("*.md")):
            parts.append(f"\n\n=== {md.name} ===\n" + md.read_text(encoding="utf-8"))
    return "\n\n".join(parts) if parts else "あなたはHighliteの視点で記事を書くライターです。"


def _strip_json_fence(text: str) -> str:
    return re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()


# --------------------------------------------------------------------------
# 選定
# --------------------------------------------------------------------------
def select(summaries: list[dict], cfg) -> dict:
    """候補サマリ [{path, text}] をスコアリングし、1本を選ぶ。

    返り値: {"selected": path or None, "score": int, "breakdown": {...},
             "rationale": str, "target_cluster": str, "considered": int,
             "rejected": [{"path":..., "score":..., "reason":...}]}
    None のときは記事化見送り。
    """
    model = cfg.get("llm.selection_model", "claude-sonnet-5")
    clusters = ", ".join(cfg.get("content.target_clusters", []))
    system = _load_context()

    listing = "\n\n".join(
        f"[{i}] path: {s['path']}\n{s['text'][:1500]}" for i, s in enumerate(summaries)
    )
    user = f"""以下は直近のトレンドサマリ候補です。仕様の選定基準（4軸スコアリング）で全候補を評価し、
最高点の1本を選んでください。

軸と配点:
- 独自見解 0-3 / 一次情報の紐付け 0-3 / ターゲット適合 0-2 / 鮮度の持続 0-2
ターゲットクラスタ: {clusters}

選定不可の条件（該当する候補は selected にしない）:
- 合計7点未満
- 一次情報の軸が0点（実案件に紐付かない）

全候補が条件を満たさない場合は selected を null にしてください（記事化見送り）。

出力は JSON のみ。前置き・コードフェンス・説明を一切含めないこと。
形式:
{{"selected": "<path or null>", "score": <int>,
  "breakdown": {{"insight": <int>, "first_party": <int>, "fit": <int>, "freshness": <int>}},
  "rationale": "<なぜこの1本か。紐付く実案件を具体的に>",
  "target_cluster": "<startup|medical|saas|luxury>",
  "considered": <候補数>,
  "rejected": [{{"path": "<path>", "score": <int>, "reason": "<落とした理由>"}}]}}

候補:
{listing}
"""
    raw = _call(model, system, user, max_tokens=2000)
    return json.loads(_strip_json_fence(raw))


# --------------------------------------------------------------------------
# 執筆
# --------------------------------------------------------------------------
def write(summary_text: str, target_cluster: str, cfg) -> dict:
    """記事を執筆する。返り値: {"title": str, "body_markdown": str, "keywords": [str]}"""
    model = cfg.get("llm.writing_model", "claude-opus-4-8")
    system = _load_context()
    min_c = cfg.get("content.min_chars", 1500)
    max_c = cfg.get("content.max_chars", 2800)
    user = f"""次のトレンドサマリを起点に、Brandri掲載用の記事を1本書いてください。
ターゲットクラスタ: {target_cluster}
文字数: {min_c}〜{max_c}字

構成（順番固定・仕様書5.1）:
1. リード 2. 何が起きているか 3. Highliteはこう見る
4. 実務ではこうだった（必須・実案件の具体） 5. 明日できること + CTA

一次情報セクション（4）が書けない場合は、その旨を理由にして body_markdown を空にしてください。

出力は JSON のみ。コードフェンス不要。
{{"title": "<質問形または断定形>",
  "body_markdown": "<本文。見出しはH2/H3。空なら見送り>",
  "keywords": ["<2-4語>", "..."],
  "skip_reason": "<書けない場合のみ理由。書けた場合は空文字>"}}

サマリ:
{summary_text}
"""
    raw = _call(model, system, user, max_tokens=6000)
    return json.loads(_strip_json_fence(raw))


# --------------------------------------------------------------------------
# 改稿
# --------------------------------------------------------------------------
def revise(current_body: str, comments: list[str], cfg) -> dict:
    """レビューコメントを反映する。返り値:
    {"body_markdown": str, "change_summary": str, "needs_clarification": bool,
     "question": str}"""
    model = cfg.get("llm.writing_model", "claude-opus-4-8")
    system = _load_context()
    joined = "\n".join(f"- {c}" for c in comments)
    user = f"""以下の記事に対するレビューコメントを反映してください。
指摘された箇所のみ直し、指摘のない箇所は変えないこと。

コメントが曖昧で判断できない場合は body を変えず needs_clarification=true にし、
question に確認事項を書いてください。

出力は JSON のみ。コードフェンス不要。
{{"body_markdown": "<修正後の本文全体>",
  "change_summary": "<変更点を3行以内>",
  "needs_clarification": <true|false>,
  "question": "<確認が必要な場合のみ>"}}

レビューコメント:
{joined}

現在の本文:
{current_body}
"""
    raw = _call(model, system, user, max_tokens=6000)
    return json.loads(_strip_json_fence(raw))
