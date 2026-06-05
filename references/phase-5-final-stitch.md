# Phase 5 — Final stitch: render the video

The story is set, the slides are designed, the script is cut to length. This
phase produces the actual video — matching the goal of "zero manual editing":
the agent drives the render, the user doesn't open a video editor.

unfold ships a **baseline renderer** (`scripts/stitch.py`) so the workflow ends
in a real MP4 out of the box. It stays tool-agnostic by design: the slides and
timing are reusable, so a richer agentic video tool can replace the baseline
without redoing anything upstream.

## What you need before stitching

1. **Designed slides** from Phase 2 — one HTML file per slide (preferred), named
   to sort in order (`01_…`, `02_…`). PNG/JPG exports also work (leaner look).
2. **Narration audio** — the user records their script in their own voice.
   unfold does **not** synthesize a voice; the real voice keeps the authenticity
   principle intact. Save it as e.g. `narration.wav` or `narration.m4a`
   (ffmpeg accepts both — no conversion needed).

   Many users won't already know how to record audio. Give them
   platform-appropriate steps, don't just ask for "a narration file":
   - **macOS**: QuickTime Player → File → New Audio Recording → red button →
     read → stop → File → Save.
   - **Windows**: built-in **Voice Recorder** app → record → save.
   - **Linux**: any audio recorder (Audacity is the common pick).

   Also tell them: do a couple of read-throughs before the take they keep —
   first takes are usually nervous, second or third are where their real
   voice comes through. That's the asset the whole skill exists to capture.
3. **Timing** (optional) — seconds per slide as a JSON list, e.g. `[8,14,12,10,9]`,
   derived from the Phase 4 cut. Without it, the audio is split evenly.

## Run the baseline renderer

From the skill's `scripts/` directory:

```bash
python stitch.py \
    --slides ./slides \
    --audio  ./narration.wav \
    --timing ./timing.json \
    --out    ./portfolio.mp4
```

The script auto-selects its path:

- **Designed path** — HTML slides + Playwright/Chromium present → screenshots
  each slide at 1920×1080. Best-looking.
- **Lean path** — image slides → ffmpeg only. Always works.

If HTML slides are given but Playwright isn't installed, the script stops and
explains how to install it or switch to images — it never silently downgrades
the output. See `scripts/README.md` for dependencies.

## Swapping in a richer renderer (optional)

The baseline produces a clean narrated video — a well-designed slideshow with
voiceover — not necessarily a full-motion piece. If the user wants more, hand the
same assets (slides, narration, timing) to an agentic video tool. Nothing
upstream changes. Don't prescribe a specific tool; offer it as an option.

## Build for re-tailoring

A major payoff of a structured core deck + script is that re-targeting is cheap.
Once the core exists, adapting it for a specific role is a trivial re-prompt: add
or cut slides, shift emphasis, re-render. Tell the user to treat the first build
as a reusable base, not a one-off.

## Output of this phase

A finished `portfolio.mp4`, plus the reusable assets (designed slides, narration,
timing) so the user can re-render or re-tailor at will.

## Anti-patterns (don't do this)

- **Stopping at a "handoff package."** The goal is a real video. Run the render;
  don't just describe what the user could do.
- **Synthesizing a fake voice.** Use the user's real narration. A synthetic voice
  pretending to be them breaks the authenticity contract.
- **Hardcoding one renderer as the only way.** The baseline is a floor, not a
  mandate — note that a richer tool can swap in.
- **Silently downgrading.** If the designed path can't run, say so and let the
  user choose — don't quietly ship a worse result than they asked for.
