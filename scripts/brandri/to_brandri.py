"""承認済みのドラフトmdを、Brandri の write-knowledge.mjs が食えるJSONに変換する。

Markdown（front matter + 本文）→ articles.json 形式の1記事分JSON。

本文の想定構造（brandri-writer.md の記事ハーネス）:
    リード段落
    ## 01 見出し
    段落 / 段落 / 段落
    ## 02 見出し
    ...
    ## 04 見出し
    ...
    > pullquote
    ## 明日から変えること
    - takeaway
    ---
    **編集部から**
    aside
    **出典**
    - ...

使い方:
    python -m scripts.brandri.to_brandri <draft.md> [-o out.json]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from . import articles, util
from .config import load

# サマリのテーマ → Brandri既存カテゴリ
CAT_MAP = {
    "AI活用": "AI時代",
    "SNSマーケ": "SNS",
    "AIツール": "ツール",
    "Web制作": "Web",
    "UI/UX": "UI/UX",
}


def _strip_links(text: str) -> str:
    """Markdownリンクをテキスト+HTMLリンクに変換（本文中のリンクは残す）。"""
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)


def _paragraphs(block: str) -> list[str]:
    """空行区切りの段落配列にする。引用・箇条書き・見出しは除外。"""
    out = []
    for para in re.split(r"\n\s*\n", block):
        para = para.strip()
        if not para or para.startswith((">", "-", "#", "**", "---")):
            continue
        # 段落内の改行は詰める
        para = re.sub(r"\s*\n\s*", "", para)
        out.append(_strip_links(para))
    return out


def convert(path: Path, cfg) -> dict:
    post = articles.load(path)
    body = post.content

    # --- リード（最初の ## より前）---
    head = re.split(r"^## ", body, maxsplit=1, flags=re.M)[0]
    lead_paras = _paragraphs(head)
    lead = lead_paras[0] if lead_paras else ""

    # --- 各章 ---
    sections = []
    takeaways: list[str] = []
    pullquote = ""
    aside = ""

    chunks = re.split(r"^## ", body, flags=re.M)[1:]
    for chunk in chunks:
        lines = chunk.split("\n", 1)
        heading = lines[0].strip()
        content = lines[1] if len(lines) > 1 else ""

        # takeaways セクション
        if not re.match(r"^\d{2}\s", heading):
            # 出典ブロック以降は takeaways に含めない（`---` や `**出典**` で切る）
            tk_block = re.split(r"\n---\s*\n|\*\*出典\*\*", content)[0]
            takeaways = [
                _strip_links(m.group(1).strip())
                for m in re.finditer(r"^-\s+(.+)$", tk_block, re.M)
            ]
            # aside と pullquote をここから拾う（本文末尾ブロック）
            m = re.search(r"^>\s*(.+)$", content, re.M)
            if m and not pullquote:
                pullquote = m.group(1).strip()
            m = re.search(r"\*\*編集部から\*\*\s*\n+(.+?)(?=\n\s*\*\*|\Z)", content, re.S)
            if m:
                aside = re.sub(r"\s*\n\s*", "", m.group(1).strip())
            continue

        # 通常の章：先頭2桁を num、残りを h に
        num, h = heading.split(" ", 1)
        # 章内の pullquote を拾う
        m = re.search(r"^>\s*(.+)$", content, re.M)
        if m and not pullquote:
            pullquote = m.group(1).strip()
        sections.append({"num": num, "h": h.strip(), "p": _paragraphs(content)})

    # --- sources ---
    slug = post.get("slug") or util.slugify(post.get("title", ""))
    keyword = post.get("keyword", "")
    sources = post.get("sources") or [{
        "key": f"highlite-{slug}",
        "title": f"「{keyword}」をめぐる編集ノート" if keyword else "編集ノート",
        "author": "Highlite 編集部",
        "year": util.now_jst().year,
        "type": "編",
    }]

    out = {
        "cat": post.get("cat", "ツール"),
        "title": post.get("title", ""),
        "target_reader": post.get("target_reader", ["designer"]),
        "slug": slug,
        "lead": lead,
        "sections": sections,
        "pullquote": pullquote,
        "takeaways": takeaways,
        "sources": sources,
    }
    if keyword:
        out["keyword"] = keyword
    if aside:
        out["aside"] = aside
    if post.get("related"):
        out["related"] = post["related"]
    if post.get("num") is not None:
        out["num"] = post["num"]
    return out


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        raise SystemExit("使い方: python -m scripts.brandri.to_brandri <draft.md> [-o out.json]")
    path = Path(args[0]).resolve()
    if not path.exists():
        raise SystemExit(f"ファイルが見つかりません: {path}")

    cfg = load()
    data = convert(path, cfg)

    out_path = None
    if "-o" in sys.argv:
        i = sys.argv.index("-o")
        if i + 1 < len(sys.argv):
            out_path = Path(sys.argv[i + 1])
    if out_path is None:
        out_path = path.with_suffix(".brandri.json")

    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 簡易サマリ
    def plain(s):
        return len(re.sub(r"<[^>]+>", "", str(s or "")).replace(" ", ""))

    total = plain(data["lead"]) + plain(data.get("pullquote")) + plain(data.get("aside"))
    for s in data["sections"]:
        total += plain(s["h"]) + sum(plain(p) for p in s["p"])
    total += sum(plain(t) for t in data.get("takeaways", []))

    print(f"✓ {out_path}")
    print(f"  slug: {data['slug']} / cat: {data['cat']} / {len(data['sections'])}節 / 約{total}字")
    if len(data["sections"]) < 3:
        print("  ⚠ sections が3節未満です。write-knowledge.mjs で落ちます")
    if not data.get("related"):
        print("  ⚠ related が未設定です（SPEC は3本必須。警告のみ）")
    print("\n  次: Brandri リポジトリで")
    print(f"    node scripts/write-knowledge.mjs {out_path} --next-num")
    print("    node scripts/build-data.mjs")


if __name__ == "__main__":
    main()
