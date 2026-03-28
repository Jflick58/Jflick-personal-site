---
layout: post
title: "OpenClaw is LangChain 2.0"
date: 2026-03-28 16:00:00 -0700
image: /assets/images/generated/openclaw-is-langchain-2-header.jpeg
tags: [ai, openclaw, langchain, musings]
---

## We've Been Here Before

I want to caveat this up front: this is not intended as a disparagement of either LangChain or OpenClaw. I contributed code to LangChain in its first six months. I respect what it did, particularly as a locus for concentrating the patterns people were figuring out and making them accessible. And I think what the team built with LangGraph and LangSmith is considerably better than the original LangChain. I'm also on record as being genuinely impressed by parts of OpenClaw, having spent the last few weeks building out a pretty involved setup. So this isn't coming from a place of dismissal. It's coming from a place of recognition.

LangChain emerged at a moment when there was a real gap. People had these powerful LLMs stuck behind chat interfaces, and LangChain promised to take AI from simple chatbot territory into something transformative: hook up your data, chain your prompts, build real applications. That generated enormous hype. I was at the [Gartner conference in 2023](https://www.youtube.com/live/USkXsD8eMBE?t=2572&si=blh47vynBAKsC5VD) and heard, repeatedly, that every enterprise should be figuring out how to leverage LangChain. They literally had a slide up in front of thousands of enterprise tech leaders telling them now was the time to learn LangChain. In retrospect, that was incredibly premature.

That sounds familiar, doesn't it? Because it feels like, three and a half years later, we're hearing the same narrative again. Even with all the evolution we've gotten with things like Claude Code, Pi, and the agentic applications that have been in production for a long time (including ones I work on at Shopify), there's still this push for the thing that's going to truly explode autonomous agents. And right now, OpenClaw is positioned as that thing. [Jensen Huang of NVIDIA said every enterprise needs an OpenClaw strategy.](https://www.fierce-network.com/broadband/nvidia-gtc-openclaw-new-linux-and-every-company-needs-strategy-says-jensen-huang) I heard that and had an immediate flashback to the Gartner floor.

## The Pattern I Keep Recognizing

When I first saw OpenClaw, my immediate reaction was: this is AutoGen all over again. The idea that an AI agent could develop its own skills, manage its own context, act proactively across your entire digital life. We tried versions of this before. But I'll admit that as I started looking at actual use cases, I began to see some real potential, particularly after hearing how people like Claire Vo were setting it up thoughtfully and securely.

And I did get a lot of value out of it. I've used it to help get a grip on my calendar, unsubscribe from things, set up better email filtering rules. The proactive email moment I described in my [previous post]({{ '/2026/03/28/trying-openclaw.html' | relative_url }}) was genuinely impressive. For every use case like that, though, I spent a corresponding number of hours fighting with configuration.

That is what reminds me the most of LangChain. I remember trying to do the things I'd heard people do, configuring it myself, and fighting with LangChain the entire way. That is why I ended up contributing code: if I am going to fix things, I try to upstream them. And I find myself in the exact same place with OpenClaw right now.

## The Twilio Breaking Point

![A vintage rotary telephone on an oak table with its coiled cord tangled into an elaborate knot]({{ '/assets/images/generated/openclaw-is-langchain-2-1.jpeg' | relative_url }})

I was genuinely excited about giving my agent a phone number. Outgoing calls on my behalf, with the transparency rules I'd already established. But I could not get it working. With my multi-thread approach in Slack and the process isolation I'd set up, I kept running into an issue where OpenClaw couldn't see an already-running process and kept trying to spin up a new RPC server for Twilio whenever the tool was invoked in a new session.

I spent hours on this. I consulted Claude Code via Opus. The only thing that partially worked was an extremely hacky workaround: calling it via the OpenClaw CLI as a subprocess from within the OpenClaw code itself. It did technically produce some outgoing calls, but the latency was terrible, the errors were frequent, and even when calls connected, there was a 10 to 15 second delay before the LLM would respond. That's not usable. That's a demo you show someone at a conference, not something you'd actually rely on.

At one point I sat there and thought: why am I spending this much time trying to get this thing to work when what I actually want to be doing is configuring the agent to do useful things?

That was the moment I recognized the pattern. That feeling, where the concepts are genuinely cool and the capabilities are real but you are fighting the tool instead of using the tool, is exactly what I watched hundreds of people express about LangChain in 2023 and 2024.

## What I'm Actually Considering Now

![A hand-carved oak block on a clean workbench with discarded brass gears pushed to the edges]({{ '/assets/images/generated/openclaw-is-langchain-2-2.jpeg' | relative_url }})

I'm researching the smaller alternatives: PicoClaw, NanoClaw. I want to see if they resolve some of the configuration overhead I'm hitting. But I think I could probably build the one-twentieth of OpenClaw's codebase that I actually need, especially without all the layers of config abstraction.

I could probably build most of what I use on top of Pi and leverage Pi skills, or even directly on top of Claude Code. Anthropic seems to be thinking along similar lines with Claude Code Dispatch, though it doesn't support threads yet, and I really value the modality of having threaded Slack conversations where I can spawn multiple sessions and have agents working on different things in parallel with separate context.

So what I'm actually considering is building my own minimal solution. Anti-claw, you could call it. With only the functionality I need: primarily a Slack interface to an agent harness, probably built on Pi, with my own Twilio connector and direct connectivity to the services I actually use. The thing I keep coming back to is that for every piece of genuinely useful functionality OpenClaw gives me (and there is real value in the incoming channels, the email and calendar integrations, the coding agency, ACP for Claude Code, third-party skills like Monarch for money management), there's a corresponding amount of configuration friction that makes me question whether the abstraction is earning its keep.

## I'm Open to Being Wrong

I'll acknowledge the criticism that maybe I'm being unimaginative here. Maybe I'm not pushing OpenClaw hard enough, or maybe the way I've set it up with isolation and security constraints makes it harder than it would be for someone who goes full YOLO on a Mac mini with unrestricted access. I've seen genuinely impressive use cases from people who do that: running small businesses, automating entire workflows. It can clearly do impressive things when you give it the run of the place.

But I spend all day building and debugging agents professionally. The last thing I want out of a personal AI assistant is something I have to spend multiple hours every evening wrenching on to get one piece of functionality working. I want the tool to make my life easier, not become another project I am maintaining.

## Where This Lands

I think OpenClaw is LangChain 2.0. I do not say that to be dismissive. I say it because I see the same pattern: a valued pioneer in the space that caught enormous viral attention, that introduced genuinely cool concepts, but that I do not think will have long-term staying power in its current form. I think we will look back on it the way we look back on early LangChain, or on early 3D printing for that matter, where if you were into it, you spent more time fussing with your printer than you spent actually printing cool things.

I learned some cool concepts from this process. The proactive agent behavior I described in my [previous post]({{ '/2026/03/28/trying-openclaw.html' | relative_url }}) is real, and the executive assistant framing genuinely works. But I am now looking for, or more likely going to build, a more minimal harness for the functionality I actually use. One that is more natively compatible with the security and usage patterns I find necessary: process isolation, threaded multi-session Slack interfaces, explicit domain allowlisting, and agents that operate under their own identity rather than mine.

The concepts OpenClaw exposes are worth knowing. But the implementation has enough questionable decisions, redundant configs, and rough edges that for someone who wants to use the tool rather than tinker with the tool, you are better off building the pieces you need yourself. That is where I have landed after a few weeks of genuine effort, and this is where I will close out the series.
