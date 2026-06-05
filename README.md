# unfold

**A resume folds a person down into bullet points. `unfold` opens them back up.**

`unfold` is an [Agent Skill](https://agentskills.io) — a reusable `SKILL.md`
workflow for AI coding agents — that turns your raw career artifacts (resume,
LinkedIn, product screenshots, links, a spoken brain-dump) into a short,
narrated **video portfolio**: a portfolio you can *watch* instead of read.

It works in any agent that supports the Agent Skills standard — Claude Code,
[Codex](https://developers.openai.com/codex/skills),
[Gemini CLI](https://geminicli.com/docs/cli/skills/), and others — by dropping it
into the agent's skills directory (`.agents/skills/`, or the tool-specific
equivalent like `.claude/skills/`, `.codex/skills/`, or `.gemini/skills/`).
ChatGPT is also beginning to support the same `SKILL.md` format via its Code
Interpreter.

## Why

If the résumé is becoming something you watch rather than read, the workflow to
make one should be *reproducible* — not re-improvised by hand every time. This
skill encodes the method so any agent can run it on anyone's material.

Inspired by Jaclyn Konzelmann's essay
[*Rethinking the AI PM Resume*](https://blog.jaclynkonzelmann.com/p/rethinking-the-ai-pm-resume)
and her observation that a traditional resume "strips away the humanity of the
builder behind it." This skill is an independent reimplementation of that idea as
a portable, reusable workflow — the method in my own framing, not a copy of her
post.

## The method, in five phases

1. **Inputs** — gather your source of truth: resume, LinkedIn, real product
   screenshots, links, and (most important) an unstructured spoken brain-dump.
2. **Conversational draft** — build the deck by *talking* to the agent. No manual
   slide editing. The agent designs real, brand-matched HTML slides — orchestrating
   its own `frontend-design` skill where available — instead of a stock template.
3. **Visual reality check** — use real screen-grabs of what you built.
   Authenticity beats generation when you're proving product taste.
4. **Ruthless edit** — your first cut runs 10–15 min. Cut sections, not words,
   down to a tight 3–5. The first draft is never the final draft.
5. **Final stitch** — the agent renders the actual MP4 from your designed slides
   and your narration, using the bundled `scripts/stitch.py` (or a richer video
   tool you swap in). You bring the voice; it brings the render.

## What you get

A finished narrated video (`portfolio.mp4`) plus its reusable source: the
designed slides, your narration, and timing notes — so you can re-render or
re-tailor it per audience without starting over.

The bundled renderer (`scripts/stitch.py`) produces a clean, well-designed
narrated video out of the box. Want something more cinematic? Hand the same
slides + narration to a richer agentic video tool — nothing upstream changes.

Built for real careers: if some of your best work is under NDA, `unfold` helps
you show the *thinking* behind it without leaking the work — public proxies,
redacted views, or honestly "described, not shown" slides.

## Install

`unfold` follows the portable `SKILL.md` standard, so it drops into any
compatible agent. Pick your tool:

**Claude Code**

```bash
# personal (all projects)
git clone https://github.com/denizergurel/unfold ~/.claude/skills/unfold
# or project-scoped: clone into .claude/skills/unfold inside your repo
```

Restart Claude Code, then run `/skills` to confirm `unfold` is listed.

**Codex**

```bash
git clone https://github.com/denizergurel/unfold ~/.codex/skills/unfold
```

Skills are behind a flag — start Codex with `codex --enable skills`, then use
`/skills` to confirm `unfold` loaded (or invoke it explicitly with `$unfold`).

**Gemini CLI**

```bash
gemini skills install https://github.com/denizergurel/unfold
```

Or clone into `.gemini/skills/unfold`. Confirm with `/skills list`.

**Any other Agent Skills–compatible tool**

Drop the `unfold/` folder into that tool's skills directory (often the portable
`.agents/skills/` alias).

## Use

Once installed, just describe the goal — no special command needed:

> "Help me build a video portfolio of my work."

The agent picks up `unfold` and walks you through the five phases, ending with a
render-ready handoff package.

## Structure

```
unfold/
├── SKILL.md                         # the workflow + when to trigger
├── references/                      # the detail for each phase
│   ├── phase-1-inputs.md
│   ├── phase-2-conversational-draft.md
│   ├── phase-3-visual-reality-check.md
│   ├── phase-4-ruthless-edit.md
│   └── phase-5-final-stitch.md
├── scripts/                         # the baseline video renderer
│   ├── stitch.py                    # slides + narration -> MP4
│   └── README.md                    # render paths + dependencies
└── assets/                          # fill-in templates
    ├── artifact-intake-template.md
    └── script-skeleton-template.md
```

## Renderer requirements

The bundled renderer needs **ffmpeg** (both paths). For the best-looking
"designed" path it also uses **Playwright + Chromium** to screenshot HTML slides;
without it, the renderer falls back to an image-based path that needs only
ffmpeg. See `scripts/README.md` for details.

## Credit & license

Built by [Deniz Ergürel](https://github.com/denizergurel) — turning a one-off,
hand-run process into a reusable Agent Skill anyone can install. Method inspired
by Jaclyn Konzelmann's writing (linked above); all skill text is original. Use
it, fork it, adapt it.
