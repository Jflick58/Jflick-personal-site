---
layout: post
title: "Building AI Development Intuition: Lessons from Managing Agents and Debugging with LLMs"
date: 2026-03-11
image: /assets/images/generated/ai-development-intuition-header.jpeg
tags: [ai, software development, claude code, developer productivity, musings]
---

## Master Your Tools Before You Chase New Ones

As I mentioned in my last post, I've been thinking about how to teach junior developers the intuition that makes me productive with AI tooling. Same disclaimer: I understand there are studies suggesting developers only *think* they're more productive. Based on what I've been able to measure, I do feel that my output has materially increased. Your mileage may vary.

I know [Pi](https://github.com/badlogic/pi-mono) is gaining popularity right now, however I haven't really gotten up to speed on it yet. I have used Claude Code since it launched. Before that, I used [Continue.dev](https://www.continue.dev/) and actually contributed code to it early on. I was impressed at what it could do, but the initial agentic solutions hadn't particularly impressed me. I was in the camp of wanting a chat interface where I controlled the context window and evaluated everything myself.

Claude Code changed my mind. I started using it heavily, though it took me a long time to feel comfortable with `--dangerously-skip-permissions`. Now, a year and a half later, I continue to use it as my primary interface. The main reason: Claude Code is opinionated. It ships with more batteries included than something like Pi. Pi's philosophy is heavy customization, which is great, but I appreciate that I can install vanilla Claude Code on my personal machine, on my work machine, and have the same core experience in both places. I like plan mode. I like the flow. I've developed trust in its operating modality.

Every month there's some new revolutionary tool that everyone gets excited about. Some have sticking power. Most don't. And I think a lot of developers waste time chasing them. There's a real cost to constantly resetting your familiarity with your primary tool. FOMO is real, but building deep comfort with a stable set of tools matters more than staying on the bleeding edge. Don't get me wrong, I love tinkering with my dev environment as much as the next coder, but most of the time I want trusty, predictable, low-fuss tools that don't get in the way of getting things done. 

I'll return to this point at the end. It's more important than it sounds.

## How I Approach a Problem

I am a heavy user of plan mode. My role, as I see it now, is not to be responsible for every line of code. It's to own the architecture: design patterns, data flow, contracts, and making sure the AI is pointed at the right problem.

This is where being able to articulate what you're talking about gives you a real leg up. I use [Mac Whisper](https://goodsnooze.gumroad.com/l/macwhisper) for dictation and word-vomit context into prompts. I include links to repos I'm interfacing with and let Claude pull documentation and explore underlying implementations. I use the GitHub CLI as my Git interface (not the MCP), and I regularly point Claude at repos or sections of repos to pull as context.

Here's why that matters: LLMs are good at finding local maxima within a set of changes. They're not always good at finding **global maxima**. If the AI only sees the folder you have open, it will optimize within that folder. It won't know about the pattern three directories over that already does what you're asking for. Telling the LLM *"you have access to these repos, you are totally allowed to `cd` and explore"* or *"here's my architecture, you can `git clone` around dependent service repos"* makes a real difference.

I've paired with developers who seem stuck within the boundary of what's open in their IDE. They don't give the AI permission to explore beyond that, and they don't feed it the broader context it needs to find globally optimal solutions. I think that's one of the most common and most fixable mistakes people make with these tools.

## Your Harness Is Your Ceiling

At Shopify, we have MCPs for just about everything: internal documentation, the build system, and observability platforms. We have CI pipelines with extensive tests and checks that provide guardrails around the code LLMs write. That connectivity is powerful, but it took real intention to build.

I compare that to my experience at non-tech companies and startups. Those organizations are at a disadvantage right now, because the scaffolding around the AI is what makes it effective. The AI itself is the same everywhere. The difference in outcomes come from what you wrap around it: linters with custom rules, LSP integration, build checks, test suites. If you're on GitHub, giving your LLM API access so it can work with your Actions logs is a force multiplier.

Your scaffolding is the limiter. Not the model.

![Diagram: your harness determines your AI ceiling](/assets/images/generated/ai-development-intuition-1.jpeg)

## The Workflow

Assume I've got my scaffolding in place: MCPs, GitHub tokens, the CLI configured to access the multiple repos in my stack. Here's what a typical session looks like.

I start with `--dangerously-skip-permissions`. I provide links, screenshots, and structured context. My typical opening: *"This is everything I understand about the problem: This is my intuition for where in the codebase we should be making changes: Can you validate that? Can you propose an implementation?"* Then I let it run in plan mode.

Why `--dangerously-skip-permissions`? Because sometimes in plan mode, Claude still asks for permission the first time it reads something. Plan mode already prevents destructive edits. The risk is low, and the interruptions slow me down.

This is where context switching starts. I use multiple worktrees, each with its own Claude Code instance in plan mode. I get one started, let it plan, switch to another, let it plan, repeat. I'll come back to why I think this pattern matters in a later section.

When a plan finishes, I interrogate it. **Nine times out of ten, I should find something that needs work in the first plan.** I ask it to walk me through the stack and the code. I command-click file paths in the terminal to trace the code myself. This is why I run Claude Code inside an IDE, not in a standalone terminal. I see people who run purely in terminals or slack bots and rely entirely on what the AI *says* about the code. That's a trap. Operating inside the IDE and being able to jump to the code helps me build real institutional knowledge of the codebase.

After iterating on the plan, I feed it a Graphite skill and ask it to plan a stack of atomic PRs. I had never used Graphite until I started at Shopify, and I'll admit: I initially hated [Graphite](https://graphite.dev/). However, I've come to appreciate it. Atomic stacked PRs make review easier and let me verify changes in small, testable units. Once the plan and PR stack are solid, I tell it to go: open draft PRs, write descriptions according to the repo template (or a format I specify), and reference my previous PRs for style.

At this point I can sometimes switch from Opus to Sonnet for execution. A good plan makes the code changes surgical enough that a lower-tier model handles them fine. I tell it to check CI, fix anything that fails, and let me know when it's done. I've watched it sleep for a while as it waits for CI to run, then use the GitHub CLI and our build system MCP to pull logs, diagnose failures, and amend. By the time a PR gets back to me, it's buttoned up.

**I take full ownership of everything I submit.** Before I take a PR out of draft, I review the diffs, do manual verification beyond the automated suite, take screenshots or record a video of the behavior (if there are UI impacts), and edit the PR description where needed. I do vibe-code certain things, but I make sure to delineate between experimental/low-risk stuff versus the things where I'm in the loop and taking real liability.

## Working Code Is Not the Same as Good Code

As an example of a potential AI trap, I recently fed an AI lots of context on a backend service change. It produced a working implementation. Unit tests passed. I ran curls for end-to-end verification. Everything looked fine.

Then I looked closer. What I had wanted was simple: extend an existing section by overriding a small function, expose a different route for similar but sufficiently different functionality, and cut over from the old route. The AI wrote more code than needed because it didn't recognize an existing pattern it could have leveraged. It worked, but it was architecturally subpar and would have contributed most spaghetti code. 

I caught it because I knew the design patterns in that codebase. We iterated on the feedback and landed on a simplified implementation that matched what I had in my head. Much cleaner, fewer moving parts. I also had it update a memory based on the iterations we went through to get to the ideal design (this is functionally done via appending the user-scoped `Claude.md`). I've seen lots of criticism that basically boils down to "if an AI can't one-shot the problem, it's useless because it won't learn from feedback". I like the different scopes of memory files in Claude Code to help refine the AI's approach in the future. 

This is why you need to stay in the loop. An LLM can produce code that passes every test you throw at it and still be the wrong solution from a software engineering standpoint.

![Diagram: local vs global optimization](/assets/images/generated/ai-development-intuition-2.jpeg)

## Debugging: Correlation Is Not Causation

LLMs are good at identifying correlation. They can be lazy about causation. And their default instinct when debugging errors is to wrap them in better error handling so they stop surfacing. I've noticed this pattern repeatedly: you point the AI at an error, and its first proposal is to catch it more gracefully. That's almost never the right fix.

Here's an example that illustrates the problem well. We had intermittent 404s surface in our error-tracking system caused by a file hash that would periodically invalidate. The AI identified a correlation with deployments (the hashes would change as new pods came online) and proposed handling the error more gracefully by falling back to the unhashed source file.

I asked it to trace the code for me, step by step. As I read the trace, I noticed we were already handling this scenario somewhere else. And that's what led me to the actual cause: a later function that exposed all files in bulk on a route without filtering out stale hashes. The error handler the AI wanted to fix was a red herring. The real fix was a filter on the pages we were exposing.

The AI had the correlation right. It just reached for the shortest path to make the symptom disappear.

Now in my debugging prompts, I explicitly ask the AI to **identify correlation and demonstrate a causation mechanism**. That framing forces it to go deeper. In this case, once I pressed it to demonstrate causation rather than just proposing a fix based on correlation, it went back to the logs, realized the hashed files were persisting well beyond the deployment window, and found the real fix on its own.

This is a simplistic application of the scientific method to AI-powered debugging. Not revolutionary, but the difference in one-shot success rate has been meaningful.

## Managing Agents Is Managing People

This is the section where I want to spend some time, because I think the analogy is more precise than it might seem at first.

When I was a director managing a 30-person engineering org, I had to build the muscle for context switching all day. It wasn't natural. Early on, I was used to going deep on problems myself. Driving them. Having the full context. Transitioning to management meant developing a different skill: getting good at framing problems consistently so that my team and I shared the same assumptions and heuristics for success, and then checking in at the right intervals to correct course.

The key was *how* you frame things and *when* you check in. I could have just said *"here's the task, figure it out, let me know when it's done."* That's a mode of management, but it's not a good one. The good version is: make sure there's enough shared understanding of the problem that you can catch divergence early. Not micromanagement - more like calibrated oversight.

I think about this a lot now, because managing AI agents follows a very similar pattern. Some developers give Claude a prompt, let it run a plan, let it execute, and check the code at the end. That's the "figure it out, let me know when it's done" school of management. It produces output. It does not produce reliably good output.

What I do instead is iterate on the plan. That's the check-in. That's where I catch the AI heading for a local maximum when I know there's a better approach. That's where I catch it about to add 200 lines when the existing pattern needed 20 lines extended.

A weakness that I've observed in a lot of engineering leaders is they can be effective ideators and vision-casters, but then they lose the plot as things get implemented. Implementation decisions accumulate, and the leader's mental model of how the system works starts diverging from how it's actually built. I was always intentional about trying to prevent that. I did that via working closely with my engineers to understand key implementation decisions, staying close enough to the code that my context window of how things *actually worked* stayed accurate.

That same discipline is directly applicable here. If you don't interrogate the plan, if you don't trace the code, if you don't review the diffs; you develop the same kind of context drift with your AI agents that a hands-off manager develops with their team. You think the system works one way. It actually works another. And that gap bites you eventually.

## Context Switching as a Learnable Skill

AI is pushing developers into a multi-threaded world. Previously, most developers were single-threaded, and that was fine. Celebrated, even. In this new AI world, the ones who can context switch effectively will take the most advantage of these tools. And, I think it's worth being explicit about what makes context switching work, because it's a skill that can be developed systematically.

Think about it like programming a concurrent system. When I write async code, I don't mix the individual coroutine logic with the orchestration of those coroutines. That's a design mistake I've made before, and it creates systems that are hard to reason about. Instead, I write each unit of operation as a clear, self-contained atomic function like `process_one_thing()` Then I scale parallelism separately via an orchestration layer where I handle how many things I pass to it, how many things I pass to it at once, and how to gather the results of processing all the things.  The individual function doesn't know or care how many other instances of itself are running. It just does its thing.

Context switching between AI agents works the same way. The "atomic function" is one worktree, one plan, one stack of PRs. If you define that unit cleanly, then scaling up the number of parallel threads is just an orchestration problem. Your brain has a semaphore. Initially it caps you at maybe two or three concurrent threads. As you get better at defining the atomic unit and trusting your process, you can increase that cap.

To use a Python analogy: early on, your brain is like an `asyncio.Semaphore(2)`. You can maybe handle two worktrees that turn into two separate open PRs before you start losing context trying to switch back and forth. As you build the muscle, and you optimize the individual "coroutine" (your plan mode iteration, your review process, etc...), you start to increase that semaphore. You gather over more coroutines. And breaking work into atomic pieces with stacked PRs actually makes this easier, not harder. You can go deeper on any individual thing you're switching to because the unit of work is small and well-defined. You don't have to maintain both depth and breadth simultaneously.

I think this is also why I've come around on stacked PRs in general. They force you to think about changes atomically. That structure doesn't just help with code review. It helps with the whole flow of managing parallel agent work.

![Diagram: the plan-execute-review loop](/assets/images/generated/ai-development-intuition-3.jpeg)

## The Reinforcement Loop

As you dial this in, something interesting happens. You build a reinforcement loop. You get comfortable with your models, tools, and prompts. You learn the common failure modes of the harnesses you're using. You refine your prompts based on what you've seen work and what hasn't. You develop a sense for what the output should look like before you even read it.

That loop is why I keep coming back to tool mastery over tool-hopping. Every time you switch to a new tool, you reset that loop. You lose the accumulated knowledge of how *this particular tool* tends to fail, what prompting strategies work with *this particular system prompt*, what the output looks like when it's heading in the wrong direction. If the goal is maximizing productivity while building your own engineering judgment (and like I said in my [last post](https://justinflick.com/2026/02/28/the-intuition-gap.html), I think that caveat to productivity is key to the future of software engineering), there's real value in staying with a tool long enough to complete several full turns of that feedback cycle.

If we think about software engineering as craft, a craftsman needs mastery of their tools. That extends to AI tooling. The goal isn't just to output code rapidly. It's to build your own internal context while doing so. Know the core architecture, the data flows, and the contracts in your codebase well enough to ideate and communicate how things function. I think that's the bare minimum for engineers in this AI-augmented world: not every line of code, but enough of the structural picture that you can catch the AI when it's heading somewhere wrong.

## Wrapping Up

If you've made it this far, I'll leave you with this: I don't claim to have all the answers. I'm simply sharing from the perspective of having managed an org of 30 engineers and now being an IC who spends his days executing multiple projects in parallel between agents. In future posts, I plan to dive deeper into MCP and tool design best practices, which I think is a topic that deserves its own treatment, since those are so critical to successful AI coding. For now, this blog is my attempt to distill my experience/intuition into something teachable, and I hope some of this has been useful.
