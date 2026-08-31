"""記事mdの読み書きと、drafts/scheduled/published/dropped 間の移動。"""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

import frontmatter

from . import util


def load(path: Path) -> frontmatter.Post:
    return frontmatter.load(str(path))


def save(post: frontmatter.Post, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # 日本語を \uXXXX に潰さないよう allow_unicode で書き出す
    text = frontmatter.dumps(post, allow_unicode=True, sort_keys=False)
    path.write_text(text, encoding="utf-8")


def iter_active(cfg):
    """drafts/ と scheduled/ の記事を (path, post) で返す。"""
    for key in ("drafts", "scheduled"):
        d = cfg.path(key)
        if not d.exists():
            continue
        for p in sorted(d.glob("*.md")):
            yield p, load(p)


def move(path: Path, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / path.name
    if dest.resolve() != path.resolve():
        shutil.move(str(path), str(dest))
    return dest


def new_draft_path(cfg, title: str, when: datetime | None = None) -> Path:
    when = when or util.now_jst()
    slug = util.slugify(title)
    return cfg.path("drafts") / f"{when:%Y-%m-%d}-{slug}.md"


def make_id(when: datetime | None = None) -> str:
    when = when or util.now_jst()
    return f"br-{when:%Y-%m-%d}"
