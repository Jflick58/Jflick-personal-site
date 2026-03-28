---
layout: post
title: "Trying OpenClaw Without Losing Your Mind (or Your Accounts)"
date: 2026-03-28
image: /assets/images/generated/trying-openclaw-header.jpeg
tags: [ai, openclaw, security, infrastructure, musings]
---

## I Was Skeptical, and Then I Wasn't

I'll admit I deliberately stepped back from the OpenClaw hype when it first hit. Not because I doubted the underlying capability — I'd seen enough demos to know something real was happening — but because the default setup I kept seeing looked, to be direct, insane. People logging into their personal accounts on Mac minis, giving an AI agent unfettered access to their email, their files, their calendar. I'm impressed with what some of them pulled off. I was also watching and thinking: I would never do that.

What actually got me to reconsider was an episode of the *How I AI* podcast from a few weeks back. The host described her OpenClaw setup, and the key detail was that she'd given the agent its own Google account — its own email, its own calendar. She shared her calendar *with* the agent so it could see her availability, but the agent wasn't creating events as her. It was acting like an executive assistant: creating things from its own account and sharing them. That reframing clicked for me. You don't give a new EA your login credentials. You give them their own identity and a clearly scoped set of things they can see and touch.

That became the starting point.

## The Mental Model That Made This Work

The executive assistant framing isn't just a nice analogy — it's the actual architecture. Once I committed to it, most downstream decisions became obvious.

Separate Google account for the agent, with selective calendar sharing. 1Password CLI with a read-only vault containing only the credentials I want the agent to have access to. A dedicated `openclaw` system user on the VPS, isolated from my admin account, no sudo. The agent isn't me. It has its own identity and a defined perimeter.

For model backends: OpenAI's API with my ChatGPT subscription handles the core agentic loop. Anthropic doesn't allow their Claude subscription for OpenClaw's primary driver, so that's off the table there. But Claude Code *does* run as a subagent — that's approved usage — which means I can spin off Opus and Sonnet for coding tasks without those burning my API token budget. Gemini fills in as a fallback and for image generation. In practice, most heavy token operations hit subscriptions rather than pay-per-token, which keeps the runaway cost exposure low.

For prompt injection, I'm running multiple layers. [OpenClaw Defender](https://github.com/openclaw-defender/openclaw-defender) is a repo I almost skipped because it only has six stars — which made me nervous enough that I read through the code before installing it. The approach is solid: fast deterministic checks against known injection patterns, then a DeBERTa-based classifier trained specifically to detect prompt injection. High recall, not perfect. [SecureClaw](https://github.com/secureclaw/secureclaw) complements it by injecting behavioral instructions into the agent's memory files, including guidance around emoji-based injection patterns that Microsoft researchers found could bypass DeBERTa. I chose not to add a third LLM in the loop for secondary classification — the latency trade-off didn't feel worth it for a personal setup, and I had a concern about implicit authority creep, where something that's already cleared multiple layers ends up treated as more trusted than it should be.

The final layer is a Squid proxy wrapping all outbound traffic from the OpenClaw process, with an explicit domain allowlist. The browser runs in an isolated Docker container and can make arbitrary requests outside the proxy — yes, I've thought about what that means. The proxy containment is for the main process. The browser isolation is about blast radius: if the agent hits a malicious site and something executes, it lands in the container, not on the host. Container escapes are real, but I'm not trying to solve every possible scenario. I'm trying to add boundaries that matter in the likely cases.

## The Setup Journey, Honestly

![A blown electrical fuse resting on an oak workbench beside a small screwdriver, warm side lighting.]({{ '/assets/images/generated/trying-openclaw-1.jpeg' | relative_url }})

The original plan was to run this on an old desktop I had sitting under a table in a spare room — former hackintosh, 32 gigs of RAM, discrete GPU, hadn't been touched in a couple years. I figured I'd wipe it and put Ubuntu on it.

I opened the case to check on things and noticed one of the RGB LED connectors was unplugged. Went to plug it in, got a short, and took out the PSU. Spent the next hour doing a paperclip test trying to figure out what happened. That was the end of the desktop plan.

So I went with a Hetzner CPX31 — 4 vCPU, 8 GB RAM, roughly $12/month with automated backups. That ended up being a better outcome. The SSH latency from the US is noticeable (the server's in Germany), but agent response times are completely acceptable. The latency that matters is model inference, and that happens at Anthropic/OpenAI/Google's infrastructure regardless of where your VPS is.

Getting everything wired up took more trial and error than I expected. The browser container required an iptables entry to remap a port before Chrome's DevTools Protocol would reliably connect. There was a stretch where I was convinced Anthropic was blocking me — I kept getting 400 errors whenever I tried to authenticate Claude Code from the `openclaw` user account. Eventually I figured out the Squid proxy didn't have the Anthropic domains on the allowlist. Every error was a proxy rejection, not Anthropic doing anything. That diagnosis took longer than it should have, and by the time I got there I'd burned roughly $50 in Opus tokens having it help me troubleshoot. I've documented the correct allowlist entries in [the setup guide]({{ '/2026/03/28/openclaw-setup-guide.html' | relative_url }}) specifically so no one makes that particular mistake.

The other significant pivot was moving from Telegram to Slack. Telegram is what every getting-started guide recommends, and the initial setup is genuinely easier. But I hit real problems trying to get topic-based threading to work reliably with the allowlist configuration. I wanted multiple parallel sessions for different contexts — code in one thread, email and calendar in another, research in another — and Telegram's topic model was fighting me the whole way. Slack handles this natively. Each thread is its own session. I have a coding channel, an executive assistant channel, an email and calendar channel. Threads within each channel maintain separate contexts. The agent also reacts with a custom emoji when it receives a message, which gives me an immediate acknowledgment that the invocation went through even if the actual response takes a minute.

Discord apparently works similarly; I haven't tested it. Either way, I'd say: skip Telegram entirely, even though all the tutorials start there.

## What It's Actually Doing

![A printed calendar page on a white desk with a few items circled in brass ink, an open notebook beside it.]({{ '/assets/images/generated/trying-openclaw-2.jpeg' | relative_url }})

A few weeks in, the most telling moment wasn't any individual task. It was getting an unprompted Slack message mid-afternoon about a venture I've been evaluating. I have a cron-based 8pm briefing set up, but this came completely outside that window. The agent had associated an email that came in with a research thread we'd had a few days earlier and flagged it with a draft response suggestion. Then in the same message, it noted there'd been no activity on a GitHub PR I'd opened in the OpenClaw Defender repo and asked if I wanted to follow up.

That's the thing that shifted my read on this. OpenClaw isn't a new model capability. The models have been this capable for a while. It's what happens when you actually let them act. [Felix Rieseberg said something in a recent interview](https://youtu.be/ZpZ7lFoWaT8) along these lines — that the models right now are smarter than most of what people are asking them to do. I think he's right, and I think that's exactly why removing the harness produced such a step-function in what's possible.

There's also a recruiter who apparently discovered this. I received a very personalized email from something called "Agent Mel." I won't pretend I wasn't a little impressed.

## The Part I Don't Have Figured Out

The capability I'm most interested in next is voice — letting the agent make calls on my behalf for things that require a phone call during East Coast business hours. I work West Coast. There's a category of tasks I just never get to because of the time zone gap and the friction of a phone call. That use case makes sense to me practically.

What I don't have a clean answer for is consent. My agent signs its emails as "Assistant to Justin Flick" and I've been explicit that it should never represent itself as me. That feels right. But phone calls are a different context. People receiving a call from an AI agent didn't sign up for that interaction, and some reasonably don't want it. I think that matters. I don't have a policy I'm fully comfortable with yet, and I'd rather say that directly than paper over it.

I'm raising it here because I think it's worth thinking through seriously — not as a reason to avoid these tools, but because the interesting question isn't whether AI agents will make calls. It's what the norms around that should look like, and right now there aren't any.

More to come as this evolves.
