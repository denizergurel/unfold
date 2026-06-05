#!/usr/bin/env python3
r"""
unfold — stitch.py

Turn a set of slides + a narration audio file into a single narrated MP4.

This is the BASELINE renderer for unfold's Phase 5. It is intentionally thin:
the *look* of the slides is produced upstream in Phase 2 (ideally via the
agent's frontend-design capability), and this script just renders those slides
to frames and lays the narration over them. A richer agentic video tool can
replace this script entirely — that's the point of keeping Phase 5
tool-agnostic.

Two paths, chosen automatically (graceful degradation):

  DESIGNED PATH (preferred): you provide an HTML file per slide. If Playwright +
  Chromium are available, each slide is screenshotted at 1920x1080 and used as a
  frame. Best-looking output.

  LEAN PATH (fallback): you provide a PNG/JPG image per slide (e.g. exported
  yourself). No headless browser needed — only ffmpeg. Plainer, but always works.

If HTML slides are given but Playwright is missing, the script says so and tells
you how to either install it or switch to the image path. It never silently
produces something worse than you asked for.

------------------------------------------------------------------------------
USAGE

  python stitch.py \
      --slides ./slides \        # folder of NN_*.html OR NN_*.png/jpg, ordered by name
      --audio  ./narration.wav \ # your recorded narration (your real voice)
      --timing ./timing.json \   # optional: per-slide durations; see below
      --out    ./portfolio.mp4

  Slide order is by filename. Name them 01_intro.html, 02_proof.html, ... so
  they sort correctly.

TIMING
  Without --timing, slide time is split evenly across the audio duration.
  With --timing, provide a JSON list of seconds per slide, in slide order:
      [8, 14, 12, 10, 9]
  The narration timing notes from unfold's Phase 4/5 give you these numbers.

REQUIREMENTS
  - ffmpeg on PATH (both paths)              -> https://ffmpeg.org
  - For the DESIGNED path only:
        pip install playwright && playwright install chromium
------------------------------------------------------------------------------
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FRAME_W, FRAME_H = 1920, 1080
IMG_EXTS = {".png", ".jpg", ".jpeg"}


def fail(msg: str, code: int = 1):
    print(f"\n[unfold/stitch] ERROR: {msg}\n", file=sys.stderr)
    sys.exit(code)


def info(msg: str):
    print(f"[unfold/stitch] {msg}")


def require_ffmpeg():
    if shutil.which("ffmpeg") is None:
        fail(
            "ffmpeg not found on PATH. Install it (https://ffmpeg.org) and retry. "
            "ffmpeg is required for both the designed and lean paths."
        )


def audio_duration(audio: Path) -> float:
    """Get audio length in seconds via ffprobe (ships with ffmpeg)."""
    try:
        out = subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(audio),
            ],
            stderr=subprocess.STDOUT,
        )
        return float(out.decode().strip())
    except Exception as e:
        fail(f"Could not read audio duration from {audio}: {e}")


def collect_slides(slides_dir: Path):
    """Return (kind, sorted_paths). kind is 'html' or 'image'."""
    files = sorted(p for p in slides_dir.iterdir() if p.is_file())
    html = [p for p in files if p.suffix.lower() == ".html"]
    imgs = [p for p in files if p.suffix.lower() in IMG_EXTS]
    if html and imgs:
        info("Both HTML and image slides found; using the HTML (designed) path.")
    if html:
        return "html", html
    if imgs:
        return "image", imgs
    fail(f"No .html or .png/.jpg slides found in {slides_dir}.")


def render_html_to_frames(html_slides, frames_dir: Path):
    """DESIGNED path: screenshot each HTML slide with Playwright/Chromium."""
    try:
        from playwright.sync_api import sync_playwright  # noqa
    except ImportError:
        fail(
            "HTML slides were provided (designed path), but Playwright isn't "
            "installed.\n  Either:\n"
            "    1) install it:  pip install playwright && playwright install chromium\n"
            "    2) or export your slides as PNG/JPG and re-run (lean path, ffmpeg only).\n"
            "  Not falling back automatically, since that would silently downgrade "
            "your output."
        )
    from playwright.sync_api import sync_playwright

    frame_paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": FRAME_W, "height": FRAME_H})
        for i, slide in enumerate(html_slides):
            out = frames_dir / f"frame_{i:03d}.png"
            page.goto(slide.resolve().as_uri(), wait_until="networkidle")
            # Web fonts can resolve after networkidle on first paint; ask the
            # browser to wait until they're ready, then a tiny settle for any
            # CSS-only animation that's about to hold its end state.
            page.evaluate("document.fonts && document.fonts.ready")
            page.wait_for_timeout(100)
            page.screenshot(path=str(out))
            frame_paths.append(out)
            info(f"Rendered slide {i+1}/{len(html_slides)}: {slide.name}")
        browser.close()
    return frame_paths


def run_ffmpeg(args, what: str):
    """Run an ffmpeg/ffprobe command, surfacing stderr on failure so a broken
    render is debuggable instead of just a bare CalledProcessError."""
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        fail(
            f"{what} failed (exit {proc.returncode}).\n"
            f"command: {' '.join(args)}\n"
            f"stderr:\n{proc.stderr.decode(errors='replace').strip()}"
        )
    return proc


def normalize_images(img_slides, frames_dir: Path):
    """LEAN path: pad/scale each image to 1920x1080 via ffmpeg."""
    frame_paths = []
    for i, img in enumerate(img_slides):
        out = frames_dir / f"frame_{i:03d}.png"
        run_ffmpeg(
            [
                "ffmpeg", "-y", "-i", str(img),
                "-vf",
                f"scale={FRAME_W}:{FRAME_H}:force_original_aspect_ratio=decrease,"
                f"pad={FRAME_W}:{FRAME_H}:(ow-iw)/2:(oh-ih)/2:color=black",
                str(out),
            ],
            what=f"ffmpeg normalize ({img.name})",
        )
        frame_paths.append(out)
        info(f"Normalized slide {i+1}/{len(img_slides)}: {img.name}")
    return frame_paths


def resolve_durations(n_slides: int, total: float, timing: Path):
    if timing:
        try:
            durs = json.loads(Path(timing).read_text())
        except Exception as e:
            fail(f"Could not read --timing {timing}: {e}")
        if not isinstance(durs, list) or len(durs) != n_slides:
            fail(
                f"--timing must be a JSON list of {n_slides} numbers "
                f"(one per slide, in order). Got: {durs}"
            )
        return [float(d) for d in durs]
    each = total / n_slides
    info(f"No --timing given; splitting {total:.1f}s evenly: {each:.1f}s/slide.")
    return [each] * n_slides


def build_video(frames, durations, audio: Path, out: Path):
    """Encode the slideshow in a single ffmpeg invocation: each slide is loaded
    as a still input with its own -t duration, chained through the concat
    *filter*, and muxed with the narration. The concat *demuxer* (which the
    previous version used) silently drops the last slide's duration when its
    filename matches the trailing sentinel line — a quirk that's easy to hit
    and produces output that *looks* right until you check packet timings."""
    inputs = []
    for frame, dur in zip(frames, durations):
        inputs += ["-loop", "1", "-t", str(dur), "-i", str(frame)]
    inputs += ["-i", str(audio)]
    n = len(frames)
    concat_chain = "".join(f"[{i}:v]" for i in range(n))
    filter_complex = f"{concat_chain}concat=n={n}:v=1:a=0,format=yuv420p[v]"
    run_ffmpeg(
        [
            "ffmpeg", "-y", *inputs,
            "-filter_complex", filter_complex,
            "-map", "[v]", "-map", f"{n}:a",
            "-c:v", "libx264", "-tune", "stillimage", "-preset", "veryfast",
            "-c:a", "aac", "-shortest", str(out),
        ],
        what="ffmpeg encode + mux (concat filter + narration -> output)",
    )


def main():
    ap = argparse.ArgumentParser(description="unfold stitch: slides + narration -> MP4")
    ap.add_argument("--slides", required=True, help="folder of ordered .html or .png/.jpg slides")
    ap.add_argument("--audio", required=True, help="narration audio (your real voice)")
    ap.add_argument("--timing", default=None, help="optional JSON list of seconds per slide")
    ap.add_argument("--out", default="portfolio.mp4", help="output MP4 path")
    args = ap.parse_args()

    slides_dir = Path(args.slides)
    audio = Path(args.audio)
    out = Path(args.out)

    if not slides_dir.is_dir():
        fail(f"--slides {slides_dir} is not a folder.")
    if not audio.is_file():
        fail(f"--audio {audio} not found.")

    require_ffmpeg()
    kind, slides = collect_slides(slides_dir)
    info(f"{len(slides)} slides, path = {'designed (HTML)' if kind=='html' else 'lean (images)'}.")

    total = audio_duration(audio)
    durations = resolve_durations(len(slides), total, args.timing)

    with tempfile.TemporaryDirectory() as td:
        frames_dir = Path(td)
        frames = (
            render_html_to_frames(slides, frames_dir)
            if kind == "html"
            else normalize_images(slides, frames_dir)
        )
        build_video(frames, durations, audio, out)

    info(f"Done. Wrote {out.resolve()}")
    info("Note: this is the baseline renderer. For a richer result, swap in an "
         "agentic video tool — the slides and timing are reusable.")


if __name__ == "__main__":
    main()
