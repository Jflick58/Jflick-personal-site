---
layout: post
title: "Building AI Development Intuition: Lessons from Managing Agents and Debugging with LLMs"
date: 2026-03-10
image: /assets/images/generated/ai-development-intuition-header.jpeg
tags: [ai, software development, claude code, developer productivity, musings]
---

## Master Your Tools Before You Chase New Ones

As I mentioned in my last post, I've been thinking about how to teach junior developers the intuition that I believe makes me productive with AI tooling. The same disclaimer applies: I understand there are studies suggesting developers only *think* they're more productive. Based on what I've been able to measure with my ability to execute on tasks simultaneously, I do feel that my output has materially increased. Your mileage may vary.

One of the first things I want to address is tool selection. I know [Pear](https://trypear.ai/) is gaining popularity right now, and I haven't quite gotten up to speed on it. I've used Claude Code since it launched. I was originally skeptical of agentic tooling. I had used [Continue.dev](https://www.continue.dev/) and actually contributed code to it early on, and I was impressed at what it could do. But the initial agentic solutions hadn't particularly impressed me. I was very much in the camp of wanting a chat interface where I controlled the context window and evaluated everything myself.

Claude Code changed my mind. I started using it heavily, but I still made sure I was in the driver's seat. It took me a long time to feel comfortable with dangerously skipped permissions and the more autonomous forms of the tool. Now, a year and a half later, I continue to use it as my primary interface, and the main reason is that Claude Code is opinionated. It comes with more batteries included than something like Pear. Pear allows heavy customization of your development environment, which is great, but I appreciate that I can install vanilla Claude Code on my personal machine, on my work machine, and have the same core experience in both places.

I've also found that Claude Code just works effectively for me. I really like plan mode, the flow, and the results. A lot of that is Claude Opus, but Claude Code also has its own system prompt and I've developed a certain trust and familiarity with its operating modality.

I think there's a broader point to be made here. A lot of developers are always chasing the hot new thing, and I think they waste time doing it. Every month there's some new revolutionary tool that everyone gets excited about. Some, like Claude Code, have sticking power. But I also think it's important to get familiar with your tools and to use them, quirks and all, to their maximum effectiveness. Don't be so quick to jump to whatever the hottest thing is. I know it's easy to get FOMO and feel like you're behind, but it's also very important to build a set of tools that you feel comfortable with.

I'll return to this point at the end, because I think it's more important than it sounds.

## The Development Flow: Plan Mode and Context Switching

Let me talk about how I actually approach a problem. I am a heavy, heavy user of plan mode.

I don't view my role now as being responsible for the absolute nuances of every line of code. My job is the architecture: making sure I'm using effective design patterns, making effective choices about data flow and contracts, and pointing the AI in the right direction. So I try to feed whatever context I can into Claude Code before it starts working.

This is where developers who have a strong ability to articulate what they're talking about have a real leg up. I use a tool called [Mac Whisper](https://goodsnooze.gumroad.com/l/macwhisper) with its dictation capabilities to code with my voice. I've found it has the best model offerings for this purpose, and I use its built-in dictation shortcuts to word-vomit context into prompts. I also make sure to include as many links as possible. I use the GitHub CLI as my Git interface (not the MCP), and I very often send repos, sample repos, or repos that I'm interfacing with as links to Claude, letting it pull documentation and explore the underlying implementation. I find this to be extremely effective, especially when working across code boundaries.

And this is a point worth expanding on. LLMs are really good at finding local maxima within a set of changes. They're not always so good at finding global maxima. That's where I find being able to tell the LLM, *"hey, you have access to these repos, or in the case of a large mono repo, to these different sections of the repo, and you are totally allowed to CD and explore"* makes a real difference. Even if it's underlying dependencies you're pulling in, or APIs, or whatever else, the more you can help inform the LLM and give it the ability to grab that context, the more effective it becomes.

That sounds basic, but I've sat and paired with other developers who seem stuck within the boundary of the folder they have open in their IDE. They don't give the AI permission to explore beyond that boundary, and they don't feed it the broader context it needs to make globally optimal decisions.

## Your Harness Is Your Ceiling

You are only as good as your coding harness and your infrastructure. At Shopify, we have MCPs for just about everything: internal documentation, the build system, observability platforms. That connectivity is really, really powerful for coding effectively with AI. But I also know that it's taken a lot of intention to get there. Shopify is going to be further ahead than a lot of organizations in developer tooling.

I compare that to my experience at non-tech companies and startups that don't have that scaffolding. Those companies are at a disadvantage, because right now it's that scaffolding that makes AI coding so effective in the right hands. We have CI pipelines with lots of tests and lots of checks that provide higher guardrails around the code these LLMs are writing.

If you're an individual developer, if you're at a company that doesn't have the scaffolding, I think it would be prudent to leverage AI tools to build that scaffolding as much as possible. Set up linters with custom rules. If you're using any sort of LSP, that can be valuable. Build checks, test suites. And if you're using GitHub, give your LLM API access so it can work with your Actions logs. Your scaffolding is going to be the limiter on your potential success with AI coding and how much it can accelerate you.

![A brass carpenter's square resting on a warm oak workbench, with faint pencil marks visible on the wood surface. Soft golden-hour light from the left. Represents the importance of good tooling as the foundation of craft.](/assets/images/generated/ai-development-intuition-1.jpeg)

## The Actual Workflow

So let's assume I've got all my scaffolding in place. I have my MCPs, my GitHub tokens configured with the CLI to access the multiple repos that make up my stack. I've word-vomited a bunch of context to the LLM. Here's what happens next.

I start with dangerously skipped permissions. I provide links, screenshots, and as much context as possible, but I'm also trying to structure it. Typically I work in a way where I say: *"This is everything I understand about the problem. This is my intuition for where in the codebase we should be making changes. A, can you validate that? B, can you propose an implementation?"* Then I let it run in plan mode.

The reason I use dangerously skipped permissions is that sometimes in plan mode, Claude will still ask you for permission the first time it tries to read something. I don't have time for that. Plan mode already restricts it from making destructive or permanent edits before I take a look, so the risk is low.

And this is the point where I start context switching. I make liberal use of worktrees. I'll have multiple worktrees running, each with its own Claude Code instance in plan mode. I get one started, let it go off to plan, switch my focus to setting up another worktree, get it ready, let it plan, do another, and so on. It very much reminds me of when I was a director, splitting my gaze across my team, trying to context switch and dive into problems to make sure everybody was pointed in the right direction.

Once plan mode finishes for each worktree, I interrogate the plan. This is a critical step. My rule of thumb: nine times out of ten, I should have feedback on the first plan. It should be more rare than not to accept a plan on the first pass. Usually I ask clarifying questions, ask it to walk me through the stack and the code. I'll command-click file paths in the terminal (this is why I prefer running Claude Code in a terminal inside an IDE) to quickly access and trace the code it's referencing.

I see people who run these things purely in standalone terminals or in bots where they're relying entirely on what the AI says about the code. There's no quick way to jump into the code or trace it yourself. For me, operating within an IDE and being able to trace the code that way helps me build my understanding of the codebase, my institutional knowledge, my instinct for that code.

After going back and forth on the plan, often revising the description, I'll feed it a Graphite skill and ask it to plan a stack of atomic PRs. I'll admit: I initially hated [Graphite](https://graphite.dev/). But I've come to appreciate it. Stacked PRs make the review burden easier on folks and help me test units of change more discretely. Once I have a plan ready with all the core changes and the stack of PRs, that's the point where I feel good about the implementation. I tell it to go, open the PRs as drafts, make PR descriptions according to the repo templates (or a specific format I provide), and look at my previous PRs for style.

At this point, I've already reviewed the plan and feel confident about it. I can sometimes switch from Opus to Sonnet for the implementation, because with a very good plan the actual code changes tend to be fairly surgical. Lower-tier models can be equally effective at a lower cost. But depending on the complexity, sometimes I'll stick with Opus.

Then I'm back in context-switching mode, waiting for it to finish so I can review the PRs and button them up. I take full ownership of everything. I am not one of those people who submits PRs and makes it clear they were "vibe coded." I do vibe-code certain things, and I try to delineate the experimental or low-risk things from the ones where I'm in the loop and taking a high level of ownership and liability for the code.

## Working Code Is Not the Same as Good Code

There's a great example from earlier today. I fed an AI lots of context on a problem. I initially thought it came to the right solution based on some manual testing. I had it work with our unit tests, and I wrote some additional unit tests for the function signatures to provide guardrails. But I also ran some curls to do end-to-end tests, because this was a backend change I was preparing for a subsequent frontend change.

The AI had produced a really plausible implementation, and it was working. But it wasn't until I ran the examples and took a closer look that I realized it had missed a critical part of the codebase. What I had wanted was simple: extend an existing section by overriding a small function to change a small piece of functionality, expose a different route that would do similar but sufficiently different work, and cut over from the previous route. The AI came up with a working solution, but it wrote more code than was needed because it didn't recognize the existing pattern it could have leveraged.

It wasn't until I interrogated the output based on my knowledge of design patterns, my tastes and opinions about what makes for good code, that I caught it. We quickly iterated on the feedback and came up with a simplified implementation that matched what I had in my head and was much cleaner with fewer potential issues.

This is an example where you really need to be in the loop. An LLM can output code that works well but is not globally optimal for your codebase. Working code and good code are not always the same thing.

![A single oak block placed precisely in line with a row of identical blocks, one gap visible where a misaligned block was removed. Clean white surface, warm side lighting. Represents recognizing when working code isn't the right fit for the existing architecture.](/assets/images/generated/ai-development-intuition-2.jpeg)

## The Debugging Flow: Correlation Is Not Causation

AI can be extremely helpful in debugging, but your debugging is only going to be as good as the data you feed back to it. And I'll note: there are a lot of CLIs and MCPs that take way too broad of an approach and are, in my opinion, poorly designed. If you're wasting too many tokens, if the MCP design doesn't help distill the workflows needed to get relevant data, it can confuse the AI, waste your context window, and send it spiraling.

The root issue in debugging with AI is that LLMs are really good at identifying correlation but can be lazy at identifying causation.

Here's an example. We had an unhandled error caused by a hash that was getting created on a file exposed on a route. We were getting intermittent 404s because the hash would periodically invalidate. The AI looked at this and said: the hash is invalidating correctly, so we need to handle the error more gracefully and look for the source file without the hash.

I asked it to trace the code for me, step through the functions. As I was looking at the trace, my spidey sense started tingling. I noticed a section of the code where it looked like we were already handling this scenario. And that's what led me to the actual problem: the causation wasn't in the error handler at all. It was in a later function that exposed all the files in bulk on the route without filtering out the outdated hash. Even though we had an error handler on the specific route for this type of scenario, the real fix was a filter on the static pages we were exposing.

The AI was correct about the correlation: there was a relationship with deployments, and there was overlap as pods wound down and new pods came online. But it was too eager, too greedy to find the shortest path to solve the problem. It reached for the most obvious correlation and proposed a fix that would have silenced the error without addressing the root cause.

Now in my debugging flow, I have a quasi-skill (not yet formalized, but a prompt I use regularly) that includes: *identify correlation and demonstrate a causation mechanism.* When I ask the AI to demonstrate causation, especially when it's basing a fix on strong correlation, it goes deeper. In this case, once I pressed it, it looked up the hash changes on those routes based on the logs and realized: although the deployments triggered the issue, the hashed files were persisting beyond the deployment, and those routes were still exposed. It found the actual fix.

This is not groundbreaking. It's basically the scientific method applied to debugging prompts. But I've had much better one-shot success since I started asking the AI to explicitly separate correlation from causation and identify specific data points, trends, and then a causation mechanism in the code or the errors.

## Managing Agents Is Managing People

There's a management analogy that I keep coming back to. When I was a director managing 30 engineers, I had to develop the capability to context-switch all day. It wasn't something that came easily, but it was a muscle I had to build. And the pattern was the same: frame the problem consistently so that my team and I were working off the same assumptions and heuristics for success, then check in regularly to understand how things were progressing and correct course.

I could have managed in a way where I just said: *"Here's the task, figure it out, let me know when it's done."* But that's not effective management. I'm not advocating for micromanagement, but there's a balance. You want enough shared understanding of the problem with whoever (or whatever) you're delegating to that you can periodically correct course.

The AI equivalent is iterating on plan mode. I could just give it a prompt, let it run a plan, let it execute, and check the code at the end. Some developers do this. I don't think it's effective. The equivalent of regular check-in points is interrogating the plan before execution. And at the end, you want to review and truly understand the output so that you, as a manager of agents, understand what the implementation actually looks like.

A weakness I've observed in a lot of leaders is that they can be effective ideators and vision-casters but then lose the plot as things get implemented. Implementation decisions get made, and leaders start to carry a different mental model of how things work versus how they're actually built. That was something I was always intentional about as an engineering manager and director: understanding the key implementation decisions so I maintained a context window of how things actually worked, not how I assumed they worked. That same discipline applies directly to managing AI agents.

## Context Switching as a Learnable Skill

I really think that AI is pushing developers into a more multi-threaded world. Previously, a lot of developers were extremely single-threaded, and that was fine. Now the developers who can manage context switching effectively are going to take the most advantage of these tools.

It's something like programming a multi-threaded system. When I'm writing asynchronous code with multiple thread pool executors, I structure it so I have a very clear atomic function: this is what a single unit of operation does. Then I increase the parallelism via an orchestration function. Context switching follows the same pattern. You need to define the atomic unit (a single worktree, a single plan, a single stack of PRs) before you can increase the number of threads you're managing.

To use a Python example: your brain has a semaphore. Initially it limits you to a small number of concurrent threads. As you get better and more efficient, as you optimize the individual threaded code, you're able to increase that semaphore and gather over more coroutines. I think breaking work into atomic pieces with stacked PRs actually makes context switching easier, because you're able to go deeper on any individual thing you're switching to rather than trying to maintain both a very deep and very wide context simultaneously.

![Three brass gears of different sizes interlocked on a white marble surface, each casting distinct shadows at slightly different angles. Golden-hour light from the right. Represents the mechanics of parallel context switching.](/assets/images/generated/ai-development-intuition-3.jpeg)

## The Reinforcement Loop

As you dial in this process, something interesting happens. You start to build a reinforcement loop. You get more comfortable with your models, your tools, your prompts. You start to understand the common failure modes of the harnesses you're using. You refine your skills and prompts to understand what you need to see in the output to feel confident that you're actually getting to the root of a problem.

And that loop is why I keep coming back to the idea that you should be hesitant to constantly adopt the hottest new tool. If the goal is maximizing productivity while maintaining your own context window and building your engineering and architectural chops, you almost need to be cautious about tool-hopping. There's a lot of value in the cycle of getting to know your tools, your models, your harnesses, their failure modes, what techniques focus their behavior in the directions you need.

If we think about engineering as a form of craft, a craftsman has to have mastery of their tools. That extends to AI. Take the time to make sure you're not only outputting code rapidly, but that you're building your own internal context. Do that at a sufficient balance of abstraction: not so high-level that you lose the thread, but not necessarily focused on every single line. You should know the core architecture, the data flows, and the contracts within your codebase well enough to effectively ideate and communicate how things function. I think that's the bare minimum that engineers should still do, even in this AI-augmented world.

As I disclaimed in my last post, I don't claim to have all the answers. I'm sharing from the perspective of having been an engineering manager and director, having led an org of 30 engineers, and now being an IC who spends most of his days working on multiple projects with a high level of ownership, executing things in parallel between different agents. This blog is my attempt to distill as much of that experience and intuition into teachable moments as I can.
