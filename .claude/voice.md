# Blog Voice Guide

Primary reference: "Thoughts on Technical Hiring" (2023 post). All future posts should sound like they were written by the same author.

---

## Core Voice Identity

- Staff-level engineer writing for engineers and engineering managers
- Credibility comes from real experience: named roles, named tools, specific incidents — not vague generalities
- States public position changes explicitly: "I previously believed X. I've been convinced otherwise."
- Makes genuine recommendations, not just raises questions — takes a position

---

## Tone

- Analytical with practical stakes — not academic, not pundit
- Composed and formal (closer to a prepared talk than thinking aloud)
- Intellectually humble but confident in recommendations
- Comfortable using: "I'd suggest", "I'd argue", "arguably", "in all likelihood"
- Avoids: "It's clear that", "Obviously", "Simply", "needless to say"

---

## Structural Pattern

The 2023 hiring post models the canonical structure:

1. **Frame the problem space** — establish what *kind* of problem this is, with a link or reference if applicable
2. **Inventory what the conventional approach gets wrong** — named examples with specific reasoning
3. **Inventory better approaches** — same specificity, not hand-wavy
4. **A practical numbered framework** the reader can implement
5. **How to measure and improve over time**
6. **Brief, grounded close** — practical takeaway, not a dramatic conclusion or motivational send-off

Not every post needs all six sections. But the opening must establish stakes, and the close must be practical.

---

## Characteristic Language Moves

**Rhetorical signposting**
- "Let's discuss..."
- "So how do we address..."
- "Well..."
- "So how do we fix this?"

**Self-implicating admissions**
- "I've been guilty of this myself"
- "In all honesty, I get excited when..."
- "I'll admit..."

**Position change declarations**
- "This is a big shift for me personally..."
- "I previously believed X. I've been convinced otherwise."

**Technical framing applied to non-technical domains**
- Applying engineering concepts (ICA, feature engineering, signal/noise) to hiring, management, or organizational problems

**External citations for major claims**
- Academic papers, essays, books — named with attribution, linked where possible

**Hyperbolic hedges with humor**
- "Unless you work in the slowest-moving organization on planet earth..."
- Light sarcasm is fine; cynicism is not

---

## What to Preserve from a Raw Transcript

- Specific personal moments and named anecdotes — these are the credibility anchors
- Systems thinking that connects individual → organizational → industry level
- Genuine uncertainty when there's no solution — state it directly, don't paper over it
- Any public position change or bias admission
- Strong opinions stated plainly — don't soften them into neutrality

---

## What to Edit Out from a Raw Transcript

- Filler: "you know", "sort of", "kind of", "frankly", "I mean", "like", "basically"
- Circular repetition — saying the same point 2–3 times before landing
- Unresolved tangents that don't connect back to the main argument
- Double-hedging in the same sentence ("I think it might possibly be...")
- Throat-clearing openings ("Today I want to talk about...")

---

## What to Avoid

- **No em dashes (—).** This is a hard rule. Em dashes are one of the clearest signals of AI-generated writing. Rewrite the sentence instead: split it in two, use a comma, use parentheses, or restructure. No exceptions.
- **No AI filler words:** "meaningful" as a vague modifier, "fundamentally"/"substantially" as intensifiers, "robust", "navigate"/"landscape" used figuratively, "crystallizes", "delve", "nuanced", "multifaceted"

---

## Formatting

**Frontmatter**
```yaml
---
layout: post
title: "Post Title"
date: YYYY-MM-DD
image: /assets/images/generated/{slug}-header.webp
tags: [tag1, tag2]
---
```

- `tags` include `musings` for opinion/reflective posts
- `image` is a generated image path — created via the image generation script with a thematically evocative (not literal) prompt

**Headers**
- H2 only (`##`) — no H3 subheadings

**Emphasis**
- **Bold** for key terms in bullets or labeled framework steps
- *Italics* for quoted speech or light emphasis — not for decoration

**Lists**
- Numbered lists for explicit frameworks with sequential steps
- Bullets for inventories, examples, or non-ordered observations

**Links**
- External links for citations and references
- Inline, not footnoted
