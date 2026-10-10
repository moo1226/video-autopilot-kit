#!/usr/bin/env python3
"""用 OpenAI gpt-image 模型生圖，存進「AI生圖」資料夾。

金鑰只從環境變數 OPENAI_API_KEY 讀取，程式不會印出金鑰內容。

用法：
  python3 tools/ai-image/generate.py --check
  python3 tools/ai-image/generate.py "提示詞" --quality low
  python3 tools/ai-image/generate.py "提示詞" --quality high --size 1024x1536
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

API = "https://api.openai.com/v1"
MODEL = "gpt-image-2"
OUT_DIR = Path(__file__).resolve().parents[2] / "AI生圖"


def get_key():
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        sys.exit("找不到環境變數 OPENAI_API_KEY。")
    return key


def call(path, key, payload=None):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST" if payload else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"API 錯誤 {e.code}：{e.read().decode(errors='replace')[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"連不到 api.openai.com：{e.reason}")


def check():
    key = get_key()
    print(f"已讀到 OPENAI_API_KEY（長度 {len(key)}，內容不顯示）")
    ids = {m["id"] for m in call("/models", key).get("data", [])}
    image_models = sorted(i for i in ids if i.startswith("gpt-image"))
    print("可用的 gpt-image 模型：", ", ".join(image_models) or "（無）")


def generate(prompt, quality, size, name):
    key = get_key()
    data = call("/images/generations", key, {
        "model": MODEL, "prompt": prompt, "quality": quality, "size": size, "n": 1,
    })
    OUT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = OUT_DIR / f"{stamp}_{quality}_{name}.png"
    path.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    print(f"已存檔：{path}")
    if "usage" in data:
        print("用量：", json.dumps(data["usage"], ensure_ascii=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("prompt", nargs="?")
    p.add_argument("--quality", default="low", choices=["low", "medium", "high"])
    p.add_argument("--size", default="1024x1024")
    p.add_argument("--name", default="image", help="檔名後綴")
    p.add_argument("--check", action="store_true", help="只確認金鑰與連線")
    a = p.parse_args()
    if a.check:
        check()
    elif a.prompt:
        generate(a.prompt, a.quality, a.size, a.name)
    else:
        p.error("請提供提示詞，或用 --check")
