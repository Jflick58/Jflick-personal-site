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
- For `image`: leave as `image: TBD` — this will be filled in Step 5 after image generation
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

## Step 5: Generate inline images

After completing the draft, generate images to accompany the post. Use the script at `.claude/commands/blog/transcript-to-post/scripts/generate-image.py`.

**Prerequisites:** Ensure `gemimg` is installed (`pip install -r requirements.txt`) and `GEMINI_API_KEY` is set in the environment.

**How many images:**
- **Every post** gets a header image (for the frontmatter `image` field and social cards)
- **Short posts** (under ~1000 words): 1 inline image max
- **Standard posts** (1500–2500 words): 1–2 inline images
- **Longer posts** (2500+ words): 2–3 inline images
- **Never exceed 3 inline images.** One strong image is better than three mediocre ones.

**What to illustrate:**
- Images should illustrate concepts **abstractly and evocatively**, not literally. If the post discusses "technical debt," don't generate a picture of someone at a computer. Generate something like tangled brass wire on a white surface, or oak blocks stacked with deliberate gaps.
- Place images at **section transitions** — after an H2 heading — to give the reader a visual breath between sections. Not every section needs one.
- Images should feel like they belong in a well-designed magazine, not a PowerPoint deck.

**Aspect ratios:**
- Header image (frontmatter `image` field): `16:9`
- Inline images within the post body: `3:2`

**To generate each image, run:**

```bash
python .claude/commands/blog/transcript-to-post/scripts/generate-image.py \
  "Your descriptive prompt here" \
  --post-slug "{slug}" \
  --aspect-ratio "3:2" \
  --index {n}
```

Where `{slug}` is the post's filename slug (e.g., `the-intuition-gap`) and `{n}` is the image number (1, 2, 3).

**For the header image:**

```bash
python .claude/commands/blog/transcript-to-post/scripts/generate-image.py \
  "Your descriptive prompt here" \
  --post-slug "{slug}" \
  --aspect-ratio "16:9" \
  -o "{slug}-header"
```

**Writing good prompts:**

Prompts should be specific, evocative, and describe a concrete scene. The script automatically applies the blog's warm minimalist aesthetic (oak, brass, white, golden-hour lighting). You only need to describe the subject. Examples:

- "A single brass key resting on a white marble surface, warm directional light casting a long shadow. Represents unlocking institutional knowledge."
- "Oak building blocks arranged in a careful tower, one block slightly askew. Warm studio lighting, shallow depth of field. Represents fragile systems."
- "Scattered handwritten index cards on a warm white desk, connected by thin brass wire. Overhead view. Represents mapping ideas."

**Embed in the post body** using standard Markdown:

```markdown
![Alt text describing the image](/assets/images/generated/{slug}-{n}.webp)
```

Place images after the H2 heading of the section they relate to, with a blank line above and below.

**Update the frontmatter** with the header image path:

```yaml
image: /assets/images/generated/{slug}-header.webp
```

## Step 6: Present with editorial notes

After the draft and images, include a short section called **Editorial decisions** that notes:

- What was trimmed and why
- Any structural choices that weren't obvious (e.g., combined two sections, moved a point to the close)
- Image choices: what each image represents and why it was placed where it is
- Anything you were uncertain about and flagged for the user

Keep this section brief — three to five bullet points.

## Step 7: Ask for feedback

End with: "Does this match the voice? Anything to adjust before we finalize?"

Do not finalize or write the file until the user confirms they're satisfied.
