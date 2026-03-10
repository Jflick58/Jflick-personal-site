---
layout: post
title: "What My AI Development Flow Actually Looks Like"
date: 2026-03-10
image: /assets/images/generated/ai-development-intuition-header.jpeg
tags: [engineering, ai, musings]
---

In my last post I wrote about the intuition gap: the problem that AI makes it easy to produce code without developing the judgment to evaluate it. A fair question came back: okay, so what does your workflow actually look like?

This post is my attempt to answer that honestly. Not as a prescription, but as one data point from someone who's spent the last year and a half going deep on AI-assisted development.

## Why I'm Not Chasing the Next Thing

I want to be upfront about my tooling: I use Claude Code. I've used it since it launched. I went through the same skeptical arc that most developers did with early agentic tools. I was an early contributor to Continue.dev, and while I was impressed by what it could do, the initial agentic experiences left me convinced that I'd rather keep my hands on the context and control the evaluation loop myself. Those early tools just weren't reliable enough to trust with more autonomy.

Claude Code changed that for me. I'll admit it took a long time to feel comfortable with `--dangerously-skip-permissions` and the more autonomous modes. But I got there. And the main reason I've stayed there, without spending much time getting up to speed on every new tool that's come out since, is that Claude Code is opinionated in a way I find productive. Install it anywhere, get the same core experience. I've built up familiarity with its failure modes, its defaults, the shape of outputs I can trust. That familiarity took time to build, and it compounds.

I think a lot of developers burn energy they don't need to burn. There's a new revolutionary thing every month, and I watch engineers pivot toward it, spend a week or two, and then pivot again. I understand the FOMO. But every time you switch, you're resetting the feedback loop that makes your tools genuinely powerful. You don't develop intuition about a tool you've been using for three weeks.

I'd argue: get comfortable with your tools before you abandon them. The value isn't just efficiency. It's that the feedback loop *teaches you something* that you can't get any other way.

## The Development Flow

![Multiple brass workshop tools arranged in careful parallel on a white workbench, warm golden-hour sidelight casting long parallel shadows.]({{ "/assets/images/generated/ai-development-intuition-1.jpeg" | relative_url }})

Let me describe how I actually sit down and approach a problem.

I start almost everything in plan mode. Before any code gets written, I'm giving Claude Code as much context as I can: the problem statement, links to related repos or APIs, my intuition about where in the codebase the changes should live, screenshots if they're useful. I use [Mac Whisper](https://goodsnooze.gumroad.com/l/macwhisper) for voice dictation to do a lot of this context-loading, mostly because I can get context out of my head faster than I can type it. The ability to articulate a problem precisely is a real competitive advantage here. Developers who can speak exactly about what they're working on get better outputs. That sounds obvious, but I don't think it's acted on enough.

My standard opening looks something like: *here's everything I understand about this problem, here's where I think the changes should live. Can you validate that and propose an implementation?* Then I let it run in plan mode with `--dangerously-skip-permissions`. I use that flag at this stage because even in plan mode, Claude Code can prompt for permissions on the first run, and I don't want to babysit that. Plan mode already constrains it from making permanent edits before I've reviewed anything.

Once plan mode is running, I context switch. I use git worktrees, often multiple in parallel. I get one agent started on a plan, then go set up the next worktree and get another agent going. This rhythm (start, hand off, start, hand off) is the closest thing I've found to what I had to develop when I was a director managing a team of 30. The question in both cases is the same: are they all pointed at the right problem, and do they have what they need?

**The step I consider most critical: interrogating the plan before approving it.** My rule of thumb is that nine times out of ten I should have feedback on a plan. Accepting it on first pass should be the exception, not the default. Usually I'm asking it to walk me through the affected code, and I'm using the terminal integration in my IDE to follow along, command-clicking into functions, tracing data flows myself. This is why I run Claude Code in an IDE rather than a standalone terminal. If you're purely relying on what the AI says about the code to understand it, with no quick way to jump into the code yourself, you're building your context window on a summary of a summary.

At Shopify we use [Graphite](https://graphite.dev/) for stacked PRs. I'll be honest: I initially hated it. I've come around. Stacked PRs force you to think atomically about changes, and that turns out to help both the AI and the review process. Each piece is narrow enough that the AI can plan and execute precisely, and you can verify changes discretely rather than reviewing one massive diff at the end. Once I've refined the plan, I ask Claude Code to plan a stack of atomic PRs, open them as drafts, write descriptions that match the repo template and my prior PR style, and then execute.

At that point I often switch from Opus to Sonnet. With a good plan, the implementation changes tend to be surgical, and surgical changes don't need the most capable model. For larger or more complex change sets, I'll stay on Opus.

The last piece before I pull anything out of draft: I tell the agent to sit and wait for CI, pull the build logs via our build system MCP, debug what fails, and push amendments. By the time a PR gets to me for final review, it's already been through that loop. I still review everything, take screenshots or record a video of the functionality, and edit the description if needed. Nothing goes out until I'm comfortable signing my name to it.

I want to be direct about this because I think "vibe coding" has gotten normalized in contexts where it shouldn't be. There are experimental, low-risk, one-off things where I'll let the AI run and I'm less precious about the output. Those exist. But production work where I'm taking full ownership is a different mode, and staying in the loop isn't optional there.

## The Debugging Flow

![A brass magnifying glass resting on a sheet of white paper covered in a fine web of ink lines, one path traced in warm amber. Warm overhead studio light.]({{ "/assets/images/generated/ai-development-intuition-2.jpeg" | relative_url }})

Debugging is where I've had to develop the most explicit counter-pressure against how AI naturally wants to behave.

The pattern I see consistently, and have been guilty of enabling, is the AI identifying correlation and treating it as causation, then taking the shortest path to eliminate the symptom. In error-handling contexts, the shortest path is almost always to catch the error and stop it from surfacing. That's almost never the right answer.

A concrete example: we had an unhandled error tied to files being served with hashed filenames. Intermittent 404s, correlated with deployments: the hashes were invalidating as new pods came online. The AI's first proposal was to handle the 404 gracefully so it wouldn't surface to our error tracking. Plausible, clean, and wrong.

When I asked it to trace the causation mechanism rather than just name the correlation, it went back through the logs. What it found was that the hashes were *persisting* beyond the deployment window. The 404s weren't purely a timing issue. The actual problem was a missing filter on the endpoint that exposed static pages in bulk, serving outdated hashed files long after new ones were available. The fix was a filter. Not error handling.

That's now a standard piece of my debugging prompt: *identify the correlation, then demonstrate a causation mechanism in the code or the logs.* When you require that second step explicitly, the AI goes back and looks harder rather than accepting the first plausible story.

The other constraint worth naming: your debugging is only as good as the data you give the AI access to. Good observability integrations, readable logs, error tooling that distills rather than dumps. That's the substrate everything else runs on. I've run into enough poorly-designed MCPs that feed the AI walls of unfiltered context that I'll say it plainly: if your tooling doesn't help distill the relevant signal, you're wasting the context window and you're going to get worse outputs. That's worth a full post on its own, but it's worth flagging here.

## You're Only As Good As Your Harness

The scaffolding matters more than the specific techniques.

At Shopify, we have MCPs for internal documentation, our build system, observability platforms, and error tracking. That's a lot of intentional infrastructure built up over time, and I'm not naive about how far ahead that puts us relative to most organizations. A startup or a non-tech company without that scaffolding is at a real disadvantage, and I don't have a satisfying answer for how to close that gap quickly, other than to say that if you're in that position, using AI to *build* the scaffolding is probably more valuable than using it to ship more features on a weak foundation.

Linters with custom rules, a CI pipeline your agent can monitor, a build system it can query, observability it can read: that's the floor. The workflows I've described above work because there's a harness underneath them that catches the AI's failure modes before they become my problem. Without the harness, you're doing a lot of manual compensation, and the ceiling is lower.

This is also why I keep coming back to the CI loop. Having the agent wait for CI, pull logs, debug failures, and push fixes before a PR gets to me isn't just convenient. It's a quality gate. The AI can iterate freely within that loop in a way that doesn't produce bad output for me to review, because the CI either passes or it doesn't.

## Context Switching as a Learnable Skill

I've been using the multi-threaded programming analogy throughout this post, so let me make it explicit: most developers have been single-threaded workers. Deep focus, full context loaded, execute. That's still where good plans come from. But AI-augmented development is pushing toward an orchestration model: multiple agents running parallel units of work, with you responsible for keeping them all pointed at the right problems.

The trick, just like when writing multi-threaded code, is to keep individual units clean and atomic. When each thing you're delegating is well-scoped, context switching between them stays manageable because you're not trying to hold both a wide and deep context for everything simultaneously. You go deep on one thing, frame it well, hand it off, go deep on the next. The orchestration is lightweight when the units are well-defined. This is part of why stacked PRs help. They keep the atomic units small enough that your own context switch between them stays cheap.

This isn't a skill that arrives immediately. I watched myself build it when I moved into management. You have to develop the habit of framing problems clearly before you hand them off, checking in at the right intervals without micromanaging, and maintaining enough implementation context to know when something has drifted. Plan interrogation maps directly onto that: it's the equivalent of the pre-flight conversation you'd have before delegating something important to a person. Not a status check after the fact. An alignment check before the work begins.

A common weakness in leaders, and increasingly in AI-assisted developers, is being very effective at framing problems but losing the plot as implementation happens. Implementation decisions get made, the context of how things actually work diverges from how they were imagined, and the gap becomes a source of friction. I was intentional about avoiding that as an engineering manager, and I try to be intentional about the same thing with agents.

## What This Adds Up To

None of this is revolutionary on its own. The scientific method applied to debugging. Atomic commits. CI-gated iteration. Maintaining your own context window of what's actually shipping. These practices predate AI.

What AI changes is the ratio. When you're producing an order of magnitude more code surface, the cost of skipping these practices scales accordingly. The engineer who can maintain quality control at that throughput, context switching without losing depth and reviewing outputs critically without grinding the velocity down, is going to be useful for a long time.

The engineers I'd worry about are the ones optimizing for output volume without investing in the harness or the judgment. You can produce a lot of code that way. It's not the same thing as producing a lot of *good* code.
