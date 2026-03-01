# Transcript to Blog Post

Convert a raw transcript into a Jekyll blog post matching the project's established voice.

## Step 1: Load the voice guide

Read `.claude/voice.md` from the project root before doing anything else. That document is the style reference — do not rely on memory or generic writing advice.

## Step 2: Get the transcript

If the user has provided a transcript in the invocation, confirm you have it. If not, ask for it now. Accept it as pasted text.

## Step 3: Extract before you draft

Before writing a single word of the post, identify and state:

- **Core argument**: What is the one-sentence claim this post makes?
- **Key anecdotes**: Which specific personal moments or named examples carry the argument?
- **Position changes**: Does the speaker state any view they previously held and have reversed?
- **Genuine uncertainty**: Is there anything the speaker admits they don't have a solution to?
- **Structural fit**: Which sections of the voice.md structural pattern apply here? (Not all posts need all six.)

Show this extraction to the user briefly before drafting. One short paragraph is enough.

## Step 4: Draft the post

Write the Jekyll blog post following voice.md:

**Frontmatter**
- Generate `title`, `date` (today's date), `tags`
- For `image`: either ask the user for a Pexels URL, or suggest a specific search term they can use on pexels.com — describe what visual would work thematically, not literally
- Include `layout: post`

**Body**
- Apply the structural pattern from voice.md appropriate to this content
- Use H2 headers only — no H3
- Apply characteristic language moves from voice.md: rhetorical signposting, self-implicating admissions, position change declarations where the transcript supports them
- Preserve specific anecdotes and named examples verbatim or near-verbatim — these are load-bearing
- Remove all filler per the voice.md editing list
- Preserve one pass of the speaker's natural wandering — don't collapse every repeated point into its sharpest version. Cut only dead weight: pure filler, tangents that never reconnect. A sentence that meanders toward its point but sounds like the author is better than a clean sentence that doesn't.
- Where the speaker expressed genuine uncertainty, preserve that — do not resolve it artificially
- Numbered lists and parallel bullet structures should only appear if the speaker actually enumerated things in the transcript. Do not impose structure the speaker didn't use.

**Do not over-polish.** The goal is voice fidelity to the 2023 hiring post and "The Intuition Gap" (2026-02-28) — not a generic clean essay. If a sentence is a little rough but sounds like the author, keep it rough.

**Avoid AI-isms.** The following words and phrases signal AI authorship and must not appear in the draft:
- "meaningful" as a vague modifier ("meaningful curation", "meaningful mentorship", "meaningful portion")
- "fundamentally" or "substantially" used as filler intensifiers
- "robust" as a generic intensifier
- "navigate" or "landscape" used figuratively
- "crystallizes", "delve", "nuanced", "multifaceted"
- Section headers that announce exactly what follows ("This is where X crystallizes for me")
- Clean parallel bullet structures that resolve genuine ambiguity too neatly
- Double em dash parentheticals: `x — a, b, c — y`. Use commas or restructure instead.

## Step 5: Present with editorial notes

After the draft, include a short section called **Editorial decisions** that notes:

- What was trimmed and why
- Any structural choices that weren't obvious (e.g., combined two sections, moved a point to the close)
- Anything you were uncertain about and flagged for the user

Keep this section brief — three to five bullet points.

## Step 6: Ask for feedback

End with: "Does this match the voice? Anything to adjust before we finalize?"

Do not finalize or write the file until the user confirms they're satisfied.
