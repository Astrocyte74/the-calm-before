# The Calm Before

An evidence-based **pocket field guide for steadying the mind before an exam** —
a mobile-first rebuild of a clinical reference handout on pre-examination
relaxation and cognitive diversion.

→ **Live:** https://astrocyte74.github.io/the-calm-before/

## What it is

A single self-contained mobile web page (`index.html`) that turns the
evidence into things you can actually do:

- 🫧 **Box-breathing orb** — a guided 4-4-4-4 cycle with a live countdown.
- ✍️ **Worry-offload pad** — expressive writing with a word count and a
  "release" that clears the page (mirrors Ramirez & Beilock, *Science* 2011).
- 🎯 **Scenario finder** — tap your situation, get the matched intervention,
  evidence level, and signal.
- **Accordion study cards**, sticky header, reading-progress bar.

Every claim is sourced (PubMed, *Science*, *BMC Psychology*, *Frontiers in
Psychology*). For educational / clinical-training purposes only — not
individualized medical advice.

## Design

- **Type:** Fraunces (display) · Newsreader (body) · Schibsted Grotesk (UI).
- **Palette:** warm cream paper, pine green, terracotta, sage, dusty blue.
- **Imagery:** painterly illustrations generated with OpenAI `gpt-image-2`
  (see `gen_images.py`), served as optimized WebP.

## Files

```
index.html      # the whole experience (inline CSS + JS)
assets/         # 4 WebP illustrations (~300 KB total)
gen_images.py   # regenerates the source illustrations via gpt-image-2
```
