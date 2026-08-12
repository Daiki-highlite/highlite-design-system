"""config/brandri-pipeline.config.yaml を読み込む。"""
from __future__ import annotations

import os
from pathlib import Path

import yaml

# リポジトリルート（このファイルは scripts/brandri/config.py）
ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "brandri-pipeline.config.yaml"


class Config:
    def __init__(self, data: dict):
        self._d = data

    def __getitem__(self, key):
        return self._d[key]

    def get(self, path: str, default=None):
        """ドット区切りで入れ子を取得。例: cfg.get('cadence.publish_day')"""
        cur = self._d
        for part in path.split("."):
            if not isinstance(cur, dict) or part not in cur:
                return default
            cur = cur[part]
        return cur

    def path(self, key: str) -> Path:
        """paths.* をリポジトリルート起点の絶対Pathで返す。"""
        rel = self.get(f"paths.{key}")
        if rel is None:
            raise KeyError(f"paths.{key} が config にありません")
        return ROOT / rel


def load() -> Config:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return Config(yaml.safe_load(f))


def require_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        raise SystemExit(f"環境変数 {name} が未設定です")
    return val
