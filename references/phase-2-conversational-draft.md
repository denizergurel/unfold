# Phase 2 — Conversational draft: build the deck by talking

The user should never open a slide editor. You build the presentation through
dialogue: you propose structure, they react, you revise. This keeps them in
their voice while removing the manual labor that usually kills these projects.

## Model it on their brand, not a template

Before drafting, study the brand reference gathered in Phase 1 (their personal
site is ideal). Note tone, color palette, typography, and voice. The artifact
should feel like *them* — a generic deck template reintroduces exactly the
flattening this whole process exists to undo.

## Build real, designed slides — orchestrate the design skill

The slides are where the visual quality lives, so don't settle for plain text on
a background. Produce **real HTML slides**, and if a frontend/design capability
is available, use it: invoke the agent's `frontend-design` skill (or equivalent)
to generate distinctive, brand-matched slide markup rather than a generic
template. unfold orchestrates; the design skill executes the look.

Practically:

- One self-contained HTML file per slide (so Phase 5 can render each to a frame).
- Full-bleed imagery where there's a real product visual (resolved in Phase 3).
- Typography, color, and tone modeled on the person's brand reference from
  Phase 1 — not a stock deck theme.
- Name files so they sort in order: `01_intro.html`, `02_proof.html`, …

If no design capability is available, still produce clean HTML slides yourself —
just be honest that the look is baseline, and note the user can re-render later
with a richer tool.

## Build a structural pass first

Produce a slide-by-slide outline, not finished slides. For each slide:

- A working title / the beat it covers
- The one idea it carries (one idea per slide)
- A placeholder for the visual (resolved in Phase 3)
- A rough note on what the narration says here

Keep it to the spine of the story. Resist detail — detail gets cut in Phase 4
anyway. Once the outline is agreed, render it into the designed HTML slides
described above. Capture the per-slide narration in
`assets/script-skeleton-template.md` as you go — one idea, one visual, rough
narration per slide.

## Iterate in dialogue

Share the outline. Ask targeted questions: "Does this order tell your story, or
is the strongest beat buried?" "Which of these slides is doing real work and
which is filler?" Revise conversationally. Repeat until the skeleton feels
right to the user.

## A note on narrative shape

A portfolio you watch is a *story*, not an org chart of accomplishments. Look
for an arc: a through-line that connects the pivotal moments rather than a flat
list. The brain-dump from Phase 1 usually contains the arc already — find it
there.

## Output of this phase

An agreed slide-by-slide outline with one idea per slide, visual placeholders,
and rough narration notes. This is the skeleton the next two phases flesh out
and then cut.

## Anti-patterns (don't do this)

- **Hand-editing slides for the user.** The point is conversational iteration —
  propose, react, revise in dialogue. Don't silently produce finished slides.
- **Defaulting to a generic template.** Model the look on the person's own brand.
  A stock template reintroduces the flattening this whole process undoes.
- **More than one idea per slide.** Crowded slides bury the story. One beat each.
