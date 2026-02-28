---
layout: post
title: "The Intuition Gap: AI-Assisted Coding and the Challenge of Growing Junior Engineers"
date: 2026-02-28
image: "https://images.pexels.com/photos/21323/pexels-photo.jpg"
tags: [ai, software development, engineering management, junior developers, musings]
---

## The Agentic Shift Is Real

I've been a proponent of Claude Code since it launched. If I'm being honest, I was somewhat skeptical of truly agentic coding early on—not of AI's potential, but of its practical efficacy as an *agent* rather than a copilot. Claude Code changed my mind. It convinced me there was genuine merit to the approach, and since Claude Opus 4.5 shipped, I've been offloading progressively more of my development work to agents.

What my day looks like now is genuinely different than it did two years ago. As a staff engineer, a substantial portion of my time is spent overseeing and context-switching between multiple Claude agents running in parallel—sometimes across multiple worktrees if we're working on different areas of the same application, or across entirely different projects. I remember saying to former colleagues back in 2023: *"At some point, people's jobs are going to shift from doing the work themselves to managing a series of agentic runs."* At the time, I was thinking primarily about clerical and specialty roles—claims handling at the insurance company I was working for, for example, where you'd want human oversight but AI could dramatically scale what a single person could supervise. It turns out that reality arrived first in software development, and faster than I expected.

## Am I Actually More Productive?

There's a popular take floating around that AI only *makes you feel* more productive without actually delivering the goods. I'm aware of it, and I hold it with appropriate skepticism. That said, I feel extremely confident that my output has materially increased—and I think part of what separates my experience from others is *how* I use these tools.

This is an important aside: I think it is critical for software engineers to maintain an internal context window of what's happening in a codebase, even if you're not directly responsible for every single line of code. You have to interact with the agent's output—reading diffs, consuming the plan, tracking what changed and why—rather than treating it as a black box that just produces PRs. The moment you stop doing that, you lose the ability to catch the subtle problems that only experience can surface.

## What Actually Worries Me

What makes me nervous is watching colleagues use these tools without that engagement loop. No meaningful use of plan mode. No iterative refinement of the approach before execution. PRs reviewed only at the end rather than monitoring diffs as they develop. And increasingly, I see engineers whose primary evaluation criteria is: *does it work, and can I demo the core feature?*

The tell is in commit messages and PR descriptions. When those are thin or clearly AI-generated without meaningful curation, it signals that there wasn't much translation happening between the agent's output and the engineer's understanding. The engineer shipped something they can demonstrate but don't fully own.

This is where the root problem crystallizes for me.

## The Intuition Problem

Junior and mid-level engineers—or simply less experienced engineers regardless of title—lack the intuition that makes these tools genuinely powerful in capable hands. As a reasonably seasoned engineer, I can look at an implementation plan Claude produces and spot red flags: an approach that doesn't account for existing patterns in our codebase, a concurrency issue lurking in a data structure choice, a function boundary that's going to become a debugging nightmare at 2am. I can see those things quickly because I've encountered the consequences before.

Some of that comes from reading—design patterns, architecture books, the collective wisdom of the field. But most of it is **hard-won through direct experience**:

- **I built it, I shipped it, I owned it, it broke.** That feedback loop is irreplaceable. Knowing intellectually that certain mutation patterns can create race conditions is different from having *owned a production incident caused by one*. The latter sticks in a way that no textbook can replicate.
- **I've had to go to the source.** I remember early in my data engineering career trying to scale up pipelines and running into race condition issues I couldn't explain. I ended up having to read the actual Pandas source code to understand how certain mutation operations on DataFrames worked under the hood—specifically, what couldn't be safely parallelized. Now I can look at higher-level Pandas code and immediately recognize similar patterns. That recognition exists because of one painful debugging session, not because of anything I read.
- **Abstractions hide the lesson.** Every library we use has layers of abstraction that remove context. Sometimes that's fine. But the engineers who can reason through those abstractions are the ones who've had to dig below them.

The problem is that this knowledge is fundamentally *experiential*. Yes, you can encode some of it in shared libraries, code review culture, and team norms—but there's always some abstraction in that encoding that dilutes the lesson. You learn to recognize a race condition by having caused one, not by reading about one.

## The Broken Feedback Loop

AI has substantially disrupted the traditional feedback loop that built this intuition in junior developers. Previously, cutting your teeth as an engineer meant:

1. Getting assigned to something just slightly beyond your current capability
2. Struggling with it
3. Owning the consequences of your approach—the bugs, the on-call pages, the awkward code reviews
4. Iterating toward something better
5. Carrying that pattern-recognition forward into every future decision

Every 10X engineer had to start as a 1X engineer at some point. Unless you're Linus Torvalds, there was a period where you were functionally a little bit useless, and companies and mentors gave you the space to accumulate that hard-won knowledge. That was part of the deal—for both sides.

Now, a junior engineer can hand a complex problem to Claude and receive sophisticated, production-looking code they only partially understand. They can ship something that *works* without going through the struggle that would have built their internal model of *why* it works, or more critically, *when it will break*. We've replaced the struggle with output, and the struggle was where the learning happened.

## The 5-10X Shift and What It Means

I'm bullish on coding agents continuing to improve. And as they do, companies will respond in one of two ways: maintain the same productivity with fewer people, or increase productivity with the same headcount. In either scenario, remaining valuable as a developer means operating as a 5-10X engineer.

This isn't a prediction that programmers will be fully automated away. But I do think we'll see a structural lean-out of the industry. Here's the shift I expect:

- **What is a 1X engineer today will become the floor of acceptable performance tomorrow.** The baseline keeps moving.
- **What is a 5X engineer today will become the new 1X baseline** as productivity expectations adjust to what these tools make possible.

That creates a substantially higher barrier to entry into the field. And absent robust support structures—strong post-secondary education, meaningful professional pathways, real mentorship—you end up with a progressively more inaccessible on-ramp for new engineers. That's a problem worth taking seriously.

## What Do We Do About It?

I'm genuinely uncertain about the specific answer here. But I'm increasingly convinced that **the primary challenge for senior engineers is no longer pure technical mentorship—it's teaching intuition and critical thinking.**

In the past, mentorship often focused on things like how to operate professionally with Git, code review standards, or systems design fundamentals. Those things still matter, but I think what matters *more* now is helping junior engineers build their mental models of a codebase, across the stack, across the organization—in ways that make AI tools genuinely amplifying rather than just capable of producing plausible-looking output.

The challenge is that intuition is hard to teach through structured lessons. The field of pedagogy has grappled with this in other disciplines—how do experts transfer intuition to novices?—and I think software development is going to have to engage with that question seriously. Especially because the traditional feedback cycle that used to generate that intuition organically has been substantially modified.

## Final Thoughts

I don't have a crisp solution here, and I'd rather be honest about that than wrap this up with five clean bullet points that imply I do. What I'm confident about is the problem statement: **the more capable AI coding agents become, the more critical it is that the engineers directing them have well-developed intuition**—and we have not yet figured out how to develop that intuition without the apprenticeship model that AI is simultaneously disrupting.

That's the rub. It's something I intend to keep exploring, and I think it deserves a lot more attention than it's currently getting in the industry conversation around AI and engineering productivity.
