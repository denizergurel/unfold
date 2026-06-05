# scripts/ — the baseline renderer

`stitch.py` is unfold's **baseline** Phase 5 renderer: it turns a set of slides
plus your narration audio into a single narrated MP4. It is deliberately thin —
the visual quality comes from the *slides* (designed in Phase 2, ideally via the
agent's `frontend-design` capability), not from this script. A richer agentic
video tool can replace it entirely; the slides and timing are reusable.

## Two paths (chosen automatically)

**Designed path (preferred).** You provide one HTML file per slide. If
Playwright + Chromium are installed, each slide is screenshotted at 1920×1080
and used as a frame. Best-looking output.

**Lean path (fallback).** You provide one PNG/JPG per slide. Only ffmpeg is
needed — no headless browser. Plainer, but always works.

If you give it HTML but Playwright is missing, it stops and tells you how to
either install Playwright or switch to images. It never silently downgrades your
output.

## Requirements

- **ffmpeg** on PATH — both paths. https://ffmpeg.org
- **Playwright + Chromium** — designed path only:
  ```bash
  pip install playwright && playwright install chromium
  ```

## Usage

```bash
python stitch.py \
    --slides ./slides \         # folder of 01_*.html ... OR 01_*.png ... (ordered by name)
    --audio  ./narration.wav \  # your recorded narration — your real voice
    --timing ./timing.json \    # optional: [8, 14, 12, 10, 9] seconds per slide
    --out    ./portfolio.mp4
```

- **Slide order** is by filename — name them `01_…`, `02_…` so they sort right.
- **Timing**: without `--timing`, the audio length is split evenly across slides.
  With it, pass a JSON list of seconds per slide (the Phase 4/5 narration timing
  notes give you these).
- **Narration**: you supply your own audio. unfold does not synthesize a voice —
  using your real voice keeps the authenticity principle intact.

## Why it's this thin (on purpose)

unfold orchestrates; it doesn't reimplement a video engine. The look is borrowed
from the agent's design skill in Phase 2; this script just renders and muxes.
That keeps Phase 5 tool-agnostic and lets you swap in something fancier without
touching the rest of the workflow.
