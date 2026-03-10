---
layout: post
title: "Building AI Development Intuition: Lessons from Managing Agents and Debugging with LLMs"
date: 2026-03-10
image: /assets/images/generated/ai-development-intuition-header.jpeg
tags: [ai, software development, claude code, developer productivity, musings]
---

## Master Your Tools Before You Chase New Ones

As I mentioned in my last post, I've been thinking about how to teach junior developers the intuition that makes me productive with AI tooling. Same disclaimer: I understand there are studies suggesting developers only *think* they're more productive. Based on what I've been able to measure, I do feel that my output has materially increased. Your mileage may vary.

I know [Pi](https://github.com/badlogic/pi-mono) is gaining popularity right now. I haven't gotten up to speed on it yet. I've used Claude Code since it launched. Before that, I had used [Continue.dev](https://www.continue.dev/) and actually contributed code to it early on. I was impressed at what it could do, but the initial agentic solutions hadn't particularly impressed me. I was in the camp of wanting a chat interface where I controlled the context window and evaluated everything myself.

Claude Code changed my mind. I started using it heavily, though it took me a long time to feel comfortable with `--dangerously-skip-permissions` and the more autonomous forms of the tool. Now, a year and a half later, I continue to use it as my primary interface. The main reason: Claude Code is opinionated. It ships with more batteries included than something like Pi. Pi's philosophy is heavy customization, which is great, but I appreciate that I can install vanilla Claude Code on my personal machine, on my work machine, and have the same core experience in both places. I like plan mode. I like the flow. I've developed trust in its operating modality.

A lot of developers chase the hot new thing every month. I think they waste time doing it. Some tools, like Claude Code, have sticking power. But the real value comes from getting familiar with your tools and using them, quirks and all, to their maximum effectiveness. FOMO is real, but building deep comfort with a stable set of tools matters more than staying on the bleeding edge.

I'll return to this point at the end. It's more important than it sounds.

## How I Approach a Problem

I am a heavy user of plan mode. I don't view my role now as being responsible for every line of code. My job is architecture: effective design patterns, data flow, contracts, and pointing the AI in the right direction.

This is where being able to articulate what you're talking about gives you a real leg up. I use [Mac Whisper](https://goodsnooze.gumroad.com/l/macwhisper) with its dictation capabilities to code with my voice. I word-vomit context into prompts, include links to repos I'm interfacing with, and let Claude pull documentation and explore underlying implementations. I use the GitHub CLI as my Git interface (not the MCP), and I regularly send it repos or sections of repos to pull as context.

LLMs are good at finding local maxima within a set of changes. They're not always good at finding **global maxima**. Telling the LLM *"you have access to these repos, you are totally allowed to CD and explore"* makes a real difference. I've sat and paired with developers who seem stuck within the boundary of the folder they have open in their IDE. They don't give the AI permission to explore beyond that, and they don't feed it the broader context it needs to make globally optimal decisions.

## Your Harness Is Your Ceiling

At Shopify, we have MCPs for just about everything: internal documentation, the build system, observability platforms. We have CI pipelines with lots of tests and checks that provide guardrails around the code LLMs write. That connectivity is powerful for AI-assisted development, but it took intention to build.

I compare that to my experience at non-tech companies and startups that don't have that scaffolding. Those companies are at a disadvantage. The scaffolding is what makes AI coding effective in capable hands.

If you don't have that scaffolding, use AI tools to build it. Linters with custom rules, LSP integration, build checks, test suites. If you're on GitHub, give your LLM API access so it can work with your Actions logs. Your scaffolding is going to be the limiter on how much AI can accelerate you.

![Diagram: your harness determines your AI ceiling](/assets/images/generated/ai-development-intuition-1.jpeg)

## The Workflow

Assume I've got my scaffolding in place: MCPs, GitHub tokens, the CLI configured to access the multiple repos in my stack. Here's the flow.

I start every session with `--dangerously-skip-permissions`. I provide links, screenshots, and structured context. My typical opening: *"This is everything I understand about the problem. This is my intuition for where in the codebase we should be making changes. Can you validate that? Can you propose an implementation?"* Then I let it run in plan mode.

Why `--dangerously-skip-permissions`? Because sometimes in plan mode, Claude still asks for permission the first time it tries to read something. Plan mode already prevents destructive edits before I review. The risk is low.

This is where context switching starts. I use multiple worktrees, each with its own Claude Code instance in plan mode. Get one started, let it plan, switch to setting up another, let it plan, repeat. It reminds me of when I was a director: splitting my attention across my team, diving into each problem just enough to make sure everybody was pointed in the right direction.

When a plan finishes, I interrogate it. **Nine times out of ten, I should have feedback on the first plan.** I ask it to walk me through the stack and the code. I command-click file paths in the terminal to trace the code myself. This is why I run Claude Code inside an IDE, not in a standalone terminal. Operating within the IDE lets me build institutional knowledge of the codebase rather than relying on what the AI tells me about it.

After iterating on the plan, I feed it a Graphite skill and ask it to plan a stack of atomic PRs. I'll admit: I initially hated [Graphite](https://graphite.dev/). I've come to appreciate it. Atomic stacked PRs make review easier and let me test units of change discretely. Once the plan and PR stack are solid, I tell it to go: open draft PRs, write descriptions according to the repo template, reference my previous PRs for style.

At this point I can sometimes switch from Opus to Sonnet for execution. A good plan makes the code changes surgical, and lower-tier models handle surgical changes well. Then I'm back to context switching, waiting for it to finish so I can review and button things up.

I take full ownership of everything I submit. I do vibe-code certain things, but I delineate: experimental or low-risk stuff versus the things where I'm in the loop and taking real liability.

## Working Code Is Not the Same as Good Code

Earlier today, I fed an AI lots of context on a backend service change. It produced a working implementation. Unit tests passed. I ran curls for end-to-end verification. Everything looked right.

Then I looked closer. What I had wanted was simple: extend an existing section by overriding a small function, expose a different route for similar but sufficiently different functionality, and cut over from the old route. The AI wrote more code than needed because it didn't recognize an existing pattern it could have leveraged. It worked, but it was architecturally subpar.

I caught it because I knew the design patterns in that codebase. We iterated on the feedback and landed on a simplified implementation that matched what I had in my head. Much cleaner, fewer potential issues.

This is why you need to stay in the loop. An LLM can produce code that works but is not globally optimal for your codebase.

![Diagram: local vs global optimization](/assets/images/generated/ai-development-intuition-2.jpeg)

## Debugging: Correlation Is Not Causation

LLMs are good at identifying correlation. They can be lazy at identifying causation. And their default instinct when debugging errors is to wrap them in better error handling so they stop surfacing. That's almost never the right fix.

Here's an example. We had intermittent 404s caused by a file hash that would periodically invalidate. The AI identified a correlation with deployments and proposed handling the error more gracefully by falling back to the unhashed source file.

I asked it to trace the code, step through the functions. As I read the trace, I noticed we were already handling this scenario somewhere. The actual problem was a later function that exposed all files in bulk on a route without filtering out stale hashes. The error handler the AI wanted to fix was a red herring. The real fix was a filter on the pages we were exposing.

The AI was correct about the correlation (deployments triggered hash changes). But it was too greedy in reaching for the shortest path. It proposed silencing the symptom instead of fixing the cause.

Now in my debugging prompts, I explicitly ask the AI to **identify correlation and demonstrate a causation mechanism**. When I force it to demonstrate causation, it goes deeper. In this case, it went back to the logs, realized the hashed files were persisting beyond the deployment window, and found the actual fix.

This is the scientific method applied to AI debugging. Not groundbreaking, but effective. I've had much better one-shot success since I started requiring the AI to separate correlation from causation before proposing fixes.

## Managing Agents Is Managing People

When I was a director managing 30 engineers, I had to build the muscle for context switching all day. The pattern was: frame the problem consistently so my team and I shared assumptions and heuristics for success, then check in at the right intervals to correct course.

I could have just said *"here's the task, figure it out, let me know when it's done."* But that's not effective management. The AI equivalent is iterating on plan mode. Some developers just give it a prompt, let it run, and check the code at the end. I don't think that works. Interrogating the plan before execution is the equivalent of regular check-ins.

A weakness in a lot of leaders: they ideate effectively but lose the plot as things get implemented. Implementation decisions accumulate, and leaders carry a mental model that diverges from what's actually built. I was always intentional about understanding the key implementation decisions so I maintained a context window of how things *actually worked*, not how I assumed they worked.

That same discipline applies directly to managing AI agents.

![Diagram: the plan-execute-review loop](/assets/images/generated/ai-development-intuition-3.jpeg)

## Context Switching as a Learnable Skill

AI is pushing developers into a multi-threaded world. Previously, most developers were single-threaded, and that was fine. Now the ones who can context switch effectively will take the most advantage of these tools.

Think about it like programming a multi-threaded system. I structure async code so each unit of operation is a clear atomic function. Then I scale parallelism via an orchestration layer. Context switching works the same way. Define the atomic unit first (one worktree, one plan, one stack of PRs), then increase the number of threads.

Your brain has a semaphore. Initially it caps you at a small number of concurrent threads. As you get better, you increase that cap. Breaking work into atomic pieces with stacked PRs actually makes context switching *easier*, because you can go deeper on any individual thing rather than trying to maintain both depth and breadth at the same time.

## The Reinforcement Loop

As you dial this in, you build a reinforcement loop. You get comfortable with your models, tools, and prompts. You learn the failure modes of the harnesses you're using. You refine your prompts to understand what you need to see in the output to feel confident you're at the root of a problem.

That loop is why I keep coming back to tool mastery over tool-hopping. If the goal is maximizing productivity while building your engineering and architectural chops, there's real value in the cycle of getting to know your tools and their failure modes, rather than constantly resetting that cycle with a new tool.

If we think about engineering as craft, a craftsman needs mastery of their tools. That extends to AI. Make sure you're not only outputting code rapidly, but building your own internal context. Know the core architecture, the data flows, and the contracts in your codebase well enough to ideate and communicate how things function. I think that's the bare minimum for engineers in this AI-augmented world.

I don't claim to have all the answers. I'm sharing from the perspective of having managed an org of 30 engineers and now being an IC who spends his days executing multiple projects in parallel between different agents. This blog is my attempt to distill that experience into something teachable.
