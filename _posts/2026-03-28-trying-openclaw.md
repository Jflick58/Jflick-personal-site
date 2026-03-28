---
layout: post
title: "Trying OpenClaw Without Losing Your Mind (or Your Accounts)"
date: 2026-03-28
image: /assets/images/generated/trying-openclaw-header.jpeg
tags: [ai, openclaw, security, infrastructure, musings]
---

## I Was Skeptical, and Then I Wasn't

I'll admit I deliberately stepped back from the OpenClaw hype when it first hit. Not because I doubted the underlying capability (I'd seen enough demos to know something real was happening), but because the default setup I kept seeing looked, to be direct, insane. People logging into their personal accounts on Mac minis, giving an AI agent unfettered access to their email, their files, their calendar. I'm impressed with what some of them pulled off. I was also watching and thinking: I would never do that.

What actually got me to reconsider was [an episode of the *How I AI* podcast](https://podcasts.apple.com/us/podcast/how-i-ai/id1809663079?i=1000747009405) from a few weeks back. Claire Vo described her OpenClaw setup, and the key detail was that she'd given the agent its own Google account. Its own email, its own calendar. She shared her calendar *with* the agent so it could see her availability, but the agent wasn't creating events as her. It was acting like an executive assistant, creating things from its own account and sharing them. That reframing clicked for me. You don't give a new EA your login credentials. You give them their own identity and a clearly scoped set of things they can see and touch.

That became the starting point.

## The Mental Model That Made This Work

The executive assistant framing isn't just a nice analogy. It's the actual architecture. Once I committed to it, most downstream decisions became obvious.

Separate Google account for the agent, with selective calendar sharing. 1Password CLI with a read-only vault containing only the credentials I want the agent to have access to. A dedicated `openclaw` system user on the VPS, isolated from my admin account, no sudo. The agent isn't me. It has its own identity and a defined perimeter.

For model backends: OpenAI's API with my ChatGPT subscription handles the core agentic loop. Anthropic doesn't allow their Claude subscription for OpenClaw's primary driver, so that's off the table there. But Claude Code *does* run as a subagent (that's approved usage), which means I can spin off Opus and Sonnet for coding tasks without burning my API token budget. Gemini fills in as a fallback and for image generation. In practice, most heavy token operations hit subscriptions rather than pay-per-token, which keeps the runaway cost exposure low.

For prompt injection, I'm running multiple layers. [OpenClaw Defender](https://github.com/openclaw-defender/openclaw-defender) is a repo I almost skipped because it only has six stars, which made me nervous enough that I read through the code before installing it. The approach is solid: fast deterministic checks against known injection patterns, then a DeBERTa-based classifier trained specifically to detect prompt injection. High recall, not perfect. [SecureClaw](https://github.com/secureclaw/secureclaw) complements it by injecting behavioral instructions into the agent's memory files, including guidance around emoji-based injection patterns that Microsoft researchers found could bypass DeBERTa. I chose not to add a third LLM in the loop for secondary classification. The latency trade-off didn't feel worth it for a personal setup, and I had a concern about implicit authority creep, where something that's already cleared multiple layers ends up treated as more trusted than it should be.

The final layer is a Squid proxy wrapping all outbound traffic from the OpenClaw process, with an explicit domain allowlist. The browser runs in an isolated Docker container and can make arbitrary requests outside the proxy. Yes, I've thought about what that means. The proxy containment is for the main process. The browser isolation is about blast radius: if the agent hits a malicious site and something executes, it lands in the container, not on the host. Container escapes are real, but I'm not trying to solve every possible scenario. I'm trying to add boundaries that matter in the likely cases.

## The Setup Journey, Honestly

![A blown electrical fuse resting on an oak workbench beside a small screwdriver, warm side lighting.]({{ '/assets/images/generated/trying-openclaw-1.jpeg' | relative_url }})

The original plan was to run this on an old desktop I had sitting under a table in a spare room. It used to be a hackintosh. Got it running, loved it, and then at some point macOS updates got too painful to chase and I replaced it with a real Mac and just... left the desktop under the table. For years. It had 32 gigs of RAM and a discrete GPU, which felt like exactly the kind of machine you'd want for this. So I dusted it off, made a USB installer, had the whole plan ready.

Then I opened the case. I figured I'd at least check on things before powering it on for the first time in years. I noticed one of the RGB LED strip connectors had come loose, which seemed easy enough to fix. Went to plug it back in and immediately got a short. Took out the cooler LEDs, the RGB controller, and as I found out over the next hour of increasingly frantic troubleshooting, the PSU. The paperclip test confirmed it. The machine that was going to become my capable, cost-free OpenClaw host was now just an expensive desk ornament with a dead power supply.

So: lesson one of my OpenClaw setup journey is don't short your PSU while trying to fix something that was already working fine.

So I went with a Hetzner CPX31: 4 vCPU, 8 GB RAM, roughly $12/month with automated backups. That ended up being a better outcome. The SSH latency from the US is noticeable (the server's in Germany), but agent response times are completely acceptable. The latency that matters is model inference, and that happens at Anthropic/OpenAI/Google's infrastructure regardless of where your VPS is.

Getting everything wired up took more trial and error than I expected. The browser container required an iptables entry to remap a port before Chrome's DevTools Protocol would reliably connect. There was a stretch where I was convinced Anthropic was blocking me. I kept getting 400 errors whenever I tried to authenticate Claude Code from the `openclaw` user account. Eventually I figured out the Squid proxy didn't have the Anthropic domains on the allowlist. Every error was a proxy rejection, not Anthropic doing anything. That diagnosis took longer than it should have, and by the time I got there I'd burned roughly $50 in Opus tokens having it help me troubleshoot. I've documented the correct allowlist entries in [the setup guide]({{ '/2026/03/28/openclaw-setup-guide.html' | relative_url }}) specifically so no one makes that particular mistake.

The other significant pivot was moving from Telegram to Slack. Telegram is what every getting-started guide recommends, and the initial setup is genuinely easier. But I hit real problems trying to get topic-based threading to work reliably with the allowlist configuration. I wanted multiple parallel sessions for different contexts: code in one thread, email and calendar in another, research in another. Telegram's topic model was fighting me the whole way. Slack handles this natively. Each thread is its own session. I have a coding channel, an executive assistant channel, an email and calendar channel, and threads within each channel maintain separate contexts. The agent also reacts with a custom emoji when it receives a message, which gives me an immediate acknowledgment that the invocation went through even if the actual response takes a minute.

Discord apparently works similarly; I haven't tested it. Either way: skip Telegram entirely, even though all the tutorials start there.

## What It's Actually Doing

![A printed calendar page on a white desk with a few items circled in brass ink, an open notebook beside it.]({{ '/assets/images/generated/trying-openclaw-2.jpeg' | relative_url }})

Something worth understanding about OpenClaw is that it won't just spontaneously become proactive on its own. The memory system is genuinely powerful, but getting it to actually use that memory to reach out to you without being asked takes real work. I spent a good amount of time iterating on the SOUL.md and memory files, specifically trying to give it explicit permission and instruction to act proactively: check in on things we've discussed, surface emails that connect to prior conversations, flag when something needs a follow-up. The heartbeat cron runs every night at 8pm and gives me a briefing on the next day, which is useful. But I wanted it to go further than that.

The moment I knew it had clicked was getting an unprompted Slack message mid-afternoon about a venture I've been evaluating. Nothing triggered it. No cron, no explicit ask. The agent had pulled in an email that came in that day, associated it with a research thread we'd had a few days earlier, and sent me a message with a draft response suggestion that was actually good. In the same message it flagged that a GitHub PR I'd opened in the OpenClaw Defender repo had been sitting without activity and asked if I wanted to follow up on it.

That was genuinely surprising. The content was substantive, the connections it made were correct, and it came completely out of nowhere from my perspective. That kind of thing happens regularly now. I'll be in the middle of something and get a Slack message that's the agent surfacing something I would have forgotten about or not gotten to. It's not always right about what's worth flagging, and coaching it toward better signal-to-noise is still an ongoing process, but the behavior is there and it's useful.

That's the thing that shifted my read on this. OpenClaw isn't a new model capability. The models have been this capable for a while. [Felix Rieseberg said something along these lines in a recent interview](https://youtu.be/ZpZ7lFoWaT8): that the models right now are smarter than most of what people are asking them to do. I'd been thinking about this with a coworker recently and that observation really landed. It explains a lot of why OpenClaw got so much attention so fast. It wasn't any evolution in what the models could do. It was just taking the training wheels off. Going no brakes on the agentic loop and seeing what actually happened. And what happens, it turns out, is that you can do some genuinely impressive things. You can also do some very destructive and questionable things (shout out to the recruiter who sent me a very personalized recruiting email from something called "Agent Mel"), but the potential is real. The model was always there. The harness is what changed.

I think that framing matters because it reorients what the setup work is actually for. It's not about making the model more capable. It's about giving a capable model enough room to act while being thoughtful about what it has access to.

## The Part I Don't Have Figured Out

The capability I'm most interested in next is voice. Letting the agent make calls on my behalf for things that require a phone during East Coast business hours. I work West Coast. There's a whole category of tasks I just never get to because of the time zone gap and the friction of a phone call, and that use case makes sense to me practically. I know that sounds like the worst first-world problem imaginable, but I think it gets at something real about where these tools can actually remove friction from your life rather than just feeling impressive.

What I don't have a clean answer for is consent. I've drawn a clear line that the agent should never represent itself as me. It signs emails as "Assistant to Justin Flick" and I've been explicit in its instructions that it should be transparent about being an AI. That feels right to me and I'm not willing to budge on it. But I also think there's a harder version of the question I haven't resolved. If someone receives an email from my AI assistant, they can decide whether they want to engage with that. They have information. A phone call is different. Someone picking up the phone didn't sign up to interact with an AI agent, and some people genuinely don't want that. I think that's a reasonable position to hold and I want to be respectful of it. I just don't have a clean policy yet for how to handle it in practice.

I'm raising this because I think it's worth sitting with, not as a reason to avoid the tools. Part of why I wanted to write about this at all is that I haven't found a lot of honest discussion about these questions that isn't either behind a Medium paywall or buried in a Discord. As someone building agentic products professionally, I also think of this as research. Understanding what the bleeding edge of what these agents can actually do, and what the real friction points are, is genuinely useful for thinking about how you'd build something more scaled and more responsible.

## Where I've Landed (For Now)

OpenClaw is genuinely cool. I've surprised myself with how much I've come to appreciate it over the past few weeks, especially after starting from a pretty skeptical position. The proactive email moment alone was enough to make me want to keep building this out.

I'm still forming my final read on it. The setup work was real, the security questions are real, and the ethical questions around consent are real. I don't think any of those are reasons not to use it. They're just the actual shape of the problem, and I'd rather engage with them directly than pretend the whole thing is frictionless.

More to come as this evolves.
