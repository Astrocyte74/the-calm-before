#!/usr/bin/env python3
"""Generate the painterly image set for exam-room.html via OpenAI gpt-image-2.

Reuses the exact pipeline of gen_images.py (shared LANG style string, the
defensive gen() caller, cwebp -q82 build) so the new art is cohesive with the
existing hero-dawn / head-quiet / journal-light / moon-night set.

Sources the key from /Users/markdarby/projects/glm/.env (OPEN_AI_API_KEY),
writes full-res PNG masters into assets/src/, then builds optimized WebP
into assets/. Runs all generations concurrently.
"""
import subprocess
import shutil
import concurrent.futures

import gen_images as G   # noqa: shares LANG, gen(), MASTERS, SERVED

# (filename, prompt, size, quality)
JOBS = [
    # 1 — HERO: a calm, dignified courtroom chamber at dawn (courtroom metaphor
    #     meets the project's meditative landscape brand).
    ("courtroom-dawn.png",
     "A serene painterly illustration of an empty, dignified courtroom chamber "
     "at dawn: tall arched windows with soft warm morning light streaming "
     "through, a single calm wooden chair and quiet desk, faint golden dust "
     "motes drifting in the light. An atmosphere of hushed order and justice. "
     "Luminous pale sky filling the upper two-thirds with generous empty space, "
     "tiny solitary elements far below.",
     "1024x1536", "high"),

    # 2 — MECHANISM FEATURE: a calm head with three softly lit regions
    #     (PFC / hippocampus / amygdala), paralleling head-quiet.webp.
    ("brain-three.png",
     "An abstract painterly illustration of a calm human head in profile facing "
     "right, with three softly glowing regions gently lit from within in warm "
     "light: one at the front forehead, one deep in the center, one lower near "
     "the ear. Delicate flowing translucent lines connect them like quiet neural "
     "pathways. Minimal, centered, calm, lots of breathing room.",
     "1024x1024", "high"),

    # 3 — FALSE-FAMILIARITY BANNER: a soft mirage / calm reflective illusion.
    ("mirage.png",
     "An abstract painterly illustration of a soft mirage: a calm still lake at "
     "dusk with a faint, slightly shifting reflection that almost matches the "
     "shoreline above but not quite, low morning mist. A quiet sense of illusion "
     "and uncertainty, mysterious but serene. Lots of soft negative space.",
     "1024x1024", "high"),

    # 4 — CLOSING BAND: the courtroom restored to order — resolution & calm.
    ("courtroom-control.png",
     "A serene painterly illustration of an orderly sunlit courtroom in warm "
     "afternoon light: balanced and calm, a single soft beam of light falling "
     "across an empty quiet room, an atmosphere of peaceful resolution, as if a "
     "case has just been justly settled. Minimal, dignified, meditative.",
     "1024x1536", "high"),
]

def build_webp(name):
    if not shutil.which("cwebp"):
        return f"  cwebp missing — skip {name}"
    png = G.MASTERS / name
    webp = G.SERVED / name.replace(".png", ".webp")
    subprocess.run(["cwebp", "-q", "82", "-resize", "900", "0",
                    str(png), "-o", str(webp)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    return f"  webp: {webp.name}"

if __name__ == "__main__":
    print(f"Generating {len(JOBS)} exam-room images with gpt-image-2 -> {G.MASTERS}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(JOBS)) as ex:
        futures = {ex.submit(G.gen, *j): j[0] for j in JOBS}
        for fut in concurrent.futures.as_completed(futures):
            print(fut.result(), flush=True)
    print(f"Building optimized WebP -> {G.SERVED}")
    for name, *_ in JOBS:
        print(build_webp(name), flush=True)
    print("Done.")
