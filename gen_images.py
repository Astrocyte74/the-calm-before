#!/usr/bin/env python3
"""Generate a cohesive painterly image set via OpenAI gpt-image-2.

Sources the key from /Users/markdarby/projects/glm/.env (OPEN_AI_API_KEY).
Runs all generations concurrently. Defensive about quality param and response shape.
"""
import base64
import json
import os
import sys
import urllib.request
import concurrent.futures
from pathlib import Path

ENV = Path("/Users/markdarby/projects/glm/.env")
OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

def load_key():
    key = None
    for line in ENV.read_text().splitlines():
        line = line.strip()
        if line.startswith("OPEN_AI_API_KEY="):
            key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        sys.exit("OPEN_AI_API_KEY not found in .env")
    return key

KEY = load_key()
URL = "https://api.openai.com/v1/images/generations"

# Cohesive visual language appended to every prompt for consistency.
LANG = (
    "Soft painterly gouache and watercolor illustration, warm muted palette of "
    "cream paper, sage green, dusty terracotta clay, soft dusty blue and deep "
    "warm ink. Gentle hand-painted texture with subtle paper grain, lots of "
    "negative space, calm meditative editorial mood. NO text, NO words, "
    "NO letters, NO watermark."
)

JOBS = [
    ("hero-dawn.png",
     "A serene minimalist painterly illustration of softly layered misty hills "
     "at dawn, a pale gentle sun low on the horizon, luminous calm sky filling "
     "the upper two-thirds with generous empty space, tiny solitary figure "
     "silhouette on a ridge far below.",
     "1024x1536", "high"),
    ("head-quiet.png",
     "An abstract painterly illustration of a calm human head in profile facing "
     "right, dissolving into gentle flowing organic lines and soft translucent "
     "neural waves inside, suggesting quiet, untroubled cognition. Minimal, "
     "centered, lots of breathing room.",
     "1024x1024", "high"),
    ("moon-night.png",
     "A soft painterly night scene: a slender crescent moon glowing in a calm "
     "dusk sky with a scatter of faint stars, gentle rolling silhouetted hills "
     "below, deep but warm. Serene, sleep-like, meditative.",
     "1024x1536", "high"),
    ("journal-light.png",
     "A cozy painterly still life from above: an open blank journal with a "
     "fountain pen resting across it, a warm ceramic mug nearby, a sprig of "
     "greenery, soft golden window light. Inviting, calm, contemplative.",
     "1024x1024", "high"),
    ("ensō-bloom.png",
     "An abstract painterly illustration of a single soft ink ensō circle "
     "(brushed zen circle) with a delicate green leaf resting at its base, "
     "minimal, perfectly centered, meditative, enormous negative space.",
     "1024x1024", "high"),
]

def gen(name, prompt, size, quality):
    out = OUT / name
    payloads = []
    base = {"model": "gpt-image-2", "prompt": f"{prompt}. {LANG}",
            "size": size, "n": 1}
    # Try a few quality shapes defensively.
    payloads.append({**base, "quality": quality})
    payloads.append({**base, "quality": "auto"})
    payloads.append({**base, "output_format": "png"})
    payloads.append(base)
    last_err = None
    for body in payloads:
        req = urllib.request.Request(
            URL, data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {KEY}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            last_err = e.read().decode()[:300]
            continue
        except Exception as e:
            last_err = str(e)[:300]
            continue
        item = (data.get("data") or [{}])[0]
        if item.get("b64_json"):
            out.write_bytes(base64.b64decode(item["b64_json"]))
            return f"OK   {name} ({size}) via {set(body)-set(base) or 'base'}"
        if item.get("url"):
            with urllib.request.urlopen(item["url"], timeout=300) as r:
                out.write_bytes(r.read())
            return f"OK   {name} ({size}) via url [{set(body)-set(base) or 'base'}]"
        last_err = "no image in response"
    return f"FAIL {name}: {last_err}"

if __name__ == "__main__":
    print(f"Generating {len(JOBS)} images with gpt-image-2 -> {OUT}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(JOBS)) as ex:
        futures = {ex.submit(gen, *j): j[0] for j in JOBS}
        for fut in concurrent.futures.as_completed(futures):
            print(fut.result(), flush=True)
    print("Done.")
