# Phase 1 — Inputs: gather the source of truth

The goal of this phase is to assemble enough raw material that the rest of the
process is about *selection and shaping*, not *invention*. You cannot unfold a
person you don't have material for.

## What to collect

Prompt the user for each of these. Don't assume they'll volunteer the messy
stuff — explicitly ask for it.

1. **The existing resume.** Even an old or bad one. It's a map of what they think
   matters, and a baseline to react against.
2. **LinkedIn profile.** The public narrative they've already written.
3. **Personal site, if any.** This doubles as the *brand reference* for Phase 2 —
   note its tone, color, typography, voice.
4. **Proof-of-work artifacts.** Screenshots of shipped products, product
   announcements, dashboards, launches. The actual things, not descriptions of
   them.
5. **Links.** Talks, podcasts, keynotes, published articles, press.
6. **The spoken brain-dump.** The single most important input. Ask the user to
   talk, unstructured, about their experience — what they built, why it
   mattered, the moments they're proud of. This carries the voice and humanity
   that a resume strips out. If they hand you only polished documents, push for
   this.

## Why the brain-dump matters most

Polished documents are already flattened. The brain-dump is where the texture
lives — the "I was proud of this because…", the offhand detail that reveals
taste. The whole artifact you're building exists to surface exactly this. Treat
it as primary source, not supplementary.

## Practical prompts to elicit the brain-dump

- "Walk me through the three things you've built that you're proudest of — not
  what they were, but why they mattered and what was hard."
- "What's a product decision you made that you'd defend in a room full of
  skeptics?"
- "If someone only remembered one thing about your work, what should it be?"

## Output of this phase

A collected, labeled set of artifacts plus a transcript (or notes) of the
brain-dump. Hand the user `assets/artifact-intake-template.md` if they'd like a
structured place to gather it. Confirm you have enough before moving to Phase 2 —
if proof-of-work visuals are thin, flag it now, because Phase 3 depends on them.

## Confidential / NDA'd work

Many senior people cannot share most of what they built — it's under NDA, or the
screenshots are employer-confidential. Do **not** push the user to expose
protected material. Instead, help them surface the *judgment* without the
artifact:

- Capture the decision, trade-off, or insight in the brain-dump, described at a
  level that doesn't reveal protected specifics.
- Note which beats are confidential so Phase 3 can plan a non-leaking visual
  (a redacted view, a generic stand-in clearly labeled as such, a public
  proxy, or a "described, not shown" slide).
- When in doubt, the user decides what's shareable — your job is to flag the
  risk, not to make the call for them.

## Anti-patterns (don't do this)

- **Accepting a thin brain-dump.** If the user hands you one sentence and a
  resume, do not proceed. The brain-dump is the primary input — push for it.
- **Inventing material to fill gaps.** If proof is missing, say so and work with
  the user; never fabricate accomplishments or details to make a beat land.
- **Pressuring for confidential artifacts.** If something is NDA'd, route to the
  confidentiality guidance above — don't ask "can't you just blur it?"
