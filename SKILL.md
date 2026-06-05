---
name: unfold
description: >-
  Turn a person's raw career artifacts (resume, LinkedIn, screenshots, links,
  spoken brain-dump) into a short, narrated video portfolio — a "portfolio you
  can watch" — instead of a flat written resume. Use this whenever someone wants
  to build a video resume, a narrated portfolio, a product portfolio, a "show
  don't tell" career artifact, or wants to present their work in a more human,
  visual way than bullet points. Trigger this even when the user just describes
  the goal ("I want to show what I've built, not list it") without naming a
  video, since the whole point is to unfold the person the resume flattens.
---

# unfold

A resume folds a person down into bullet points. This unfolds them back into
something a viewer can actually watch — a short, narrated tour of the work that
shows judgment and taste, not just a list of outputs.

This skill encodes a repeatable workflow for producing that artifact, working
*conversationally* with the user. You do not silently generate a finished video
and hand it over. You run the person through a five-phase method, doing the
heavy lifting at each step while keeping them in the driver's seat on what makes
the cut.

> Inspired by Jaclyn Konzelmann's essay "Rethinking the AI PM Resume" and her
> framing that a traditional resume "strips away the humanity of the builder
> behind it." This skill turns that one-off, hand-run process into a reusable
> method. It ships a baseline video renderer (`scripts/stitch.py`) so the
> workflow ends in a real MP4, but stays renderer-agnostic: that baseline is a
> swappable floor, not a required tool — a richer agentic video tool can replace
> it without changing anything upstream.

## When to use this

Use this when the user wants to present their professional story as something
watchable rather than readable — a video portfolio, narrated walkthrough, or
"product portfolio you can watch." The user supplies *their own* artifacts; this
skill never ships with anyone's resume baked in.

## What this skill bundles

- `references/` — detailed guidance for each of the five phases. Read the
  relevant file when you reach that phase (progressive disclosure; don't load
  them all up front).
- `assets/` — two fill-in templates you give the user: `artifact-intake-template.md`
  (Phase 1, gathering material) and `script-skeleton-template.md` (Phases 2 & 4,
  drafting and cutting the narration script).
- `scripts/stitch.py` — the baseline renderer used in Phase 5 to turn the
  designed slides + narration into an MP4. Dependencies and the two render paths
  are documented in `scripts/README.md`.

## The five phases

Work through these in order. At each phase, do the work, then check with the
user before moving on. The detail for each phase lives in `references/` — read
the relevant file when you reach that phase.

### Phase 1 — Inputs: gather the source of truth

Collect every raw artifact that proves who the person is and what they built:
the existing resume, LinkedIn profile, a personal site, screenshots of shipped
products, links to launches/talks/articles, and — most importantly — a spoken,
unstructured brain-dump of their experience in their own words.

The brain-dump matters more than the polished documents. It carries the voice
and the texture that bullets strip out. Prompt the user for it explicitly; don't
let them hand you only the clean stuff.

→ Read `references/phase-1-inputs.md` for the full intake checklist. Copy
`assets/artifact-intake-template.md` into the user's working directory (or paste
its contents into the conversation) so they have a concrete place to gather
material — don't just summarize the questions inline.

### Phase 2 — Conversational draft: build the deck by talking

Draft the presentation *conversationally*. Do not ask the user to hand-edit
slides. Iterate on structure and format by discussing it, modeling the look on
the person's own brand or personal site so it feels authentically theirs — not
a generic template.

Once the outline is agreed, produce **real designed HTML slides** — and if a
frontend/design capability is available, orchestrate it: invoke the agent's
`frontend-design` skill (or equivalent) to generate distinctive, brand-matched
slides rather than plain text on a background. unfold orchestrates; the design
skill executes the look. One self-contained HTML file per slide, named to sort
in order. The user should never have to open a slide editor.

→ Read `references/phase-2-conversational-draft.md`. Use
`assets/script-skeleton-template.md` to capture the slide-by-slide narration as
you draft.

### Phase 3 — Visual reality check: authenticity over generation

When choosing visuals, prefer **real screen-grabs of the actual products** the
person built over AI-generated imagery or animated graphics. When you are
showing product taste, authenticity beats generation every time — generated
visuals read as disingenuous, and screenshots of text lack the "wow" of full-
bleed product imagery.

Audit the proposed visuals against this rule. Flag anything generated or
decorative that's standing in for real proof of work.

→ Read `references/phase-3-visual-reality-check.md`.

### Phase 4 — Ruthless edit: cut to only what matters

Assume the first script is far too long — a natural brain-dump runs 10–15
minutes against a 3–5 minute target. The art here is thrift. Cut entire
sections, not just words. Keep only the pivotal moments that demonstrate
judgment. Expect to repeat the cut several times; the first draft is never the
final draft.

→ Read `references/phase-4-ruthless-edit.md`. The cut checklist lives there; use
the cut log in `assets/script-skeleton-template.md` to track what you remove and
why (it makes Phase 5 re-tailoring easier).

### Phase 5 — Final stitch: render the video

Produce the actual video — "zero manual editing": the agent drives the render,
the user doesn't open a video editor. unfold ships a baseline renderer
(`scripts/stitch.py`) that turns the designed slides + the user's narration audio
into an MP4, so the workflow ends in a real video out of the box. It stays
tool-agnostic: the slides, narration, and timing are reusable, so a richer
agentic video tool can swap in without redoing anything upstream. The user
supplies their own narration (their real voice); unfold does not synthesize one.

→ Read `references/phase-5-final-stitch.md`. Renderer details and dependencies
are in `scripts/README.md`.

## Core principles (carry these through every phase)

- **Authenticity beats generation.** Real proof of work over generated polish.
- **The art of writing is thrift.** The first draft is never the final draft.
- **Model it on their brand, not a template.** The artifact should feel like the
  person, because the whole point is to put the person back in.
- **Conversational, not hand-built.** The user directs; you do the assembly.
- **Tailorable by design.** Once the core deck and script exist, it's a trivial
  re-prompt to add/cut slides for a specific role or audience. Build the core so
  it re-colors easily.
- **Respect confidentiality.** Much of a senior person's best work is under NDA
  or otherwise unshareable. Never push the user to expose confidential material.
  Help them demonstrate the *thinking* behind protected work without leaking the
  work itself (see Phases 1 and 3).

## Output

The deliverable is a finished narrated video plus its reusable source assets:

1. `portfolio.mp4` — the rendered narrated video (via `scripts/stitch.py`, or a
   richer renderer the user prefers)
2. The designed HTML slides (one per beat), reusable for re-rendering
3. The final narration script and audio, cut to target length
4. Timing notes (seconds per slide) so it can be re-rendered or re-tailored
5. A one-line note on how to re-tailor the deck for a different audience
