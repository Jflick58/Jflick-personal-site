---
layout: post
title: "You Are Going to Need It"
date: 2026-08-05
image: /assets/images/generated/you-are-going-to-need-it-header.jpeg
tags: [software development, abstractions, engineering principles, ai, musings]
---

## What YAGNI Is Trying to Prevent

YAGNI is an acronym for "you aren't gonna need it." It comes out of Extreme Programming, [coined by Kent Beck](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it), and in practice it's another way of encouraging engineers to avoid premature optimization.

The trap it exists to catch is real. The classic failure mode for people who write code is to sit down and immediately assume you're going to need every nice abstraction you can imagine. Everything has to be highly scalable and highly parallel out of the box. You spend a lot of time making premature optimizations and premature abstractions in code that you probably won't need. I understand that criticism. There's a real history of engineers going in the opposite direction and being too idealistic about writing super proper code. And in a lot of cases, shipping as fast as possible to get feedback and find product market fit is exactly the right call.

But I think we've gone too far in the YAGNI direction. I see it in a lot of the programmers I work with. In a world of AI I think that's actively dangerous, and I think it works against the things that make a good engineer good.

## It's a Spectrum, Not a Default

This principle is a spectrum. If you're trying to bootstrap a startup, then yes, lean into YAGNI and build only what you need to get some feedback from potential customers and try to develop product market fit. Totally cool.

But if you're like me and you work for a large company, the calculus shifts. You're often dealing with problems where you already know a certain level of scale ahead of time. You also know that the thing you're building is going to be worked on by multiple engineers. Those two facts change what actually counts as speculative.

It's worth noting that [Fowler's writeup on Yagni](https://martinfowler.com/bliki/Yagni.html) is careful about this in a way the shorthand isn't. Yagni applies to capabilities built to support a presumptive *feature*. It explicitly does not apply to effort spent making the software easier to modify. That distinction gets dropped constantly in practice, and it gets dropped in the direction that matters most, because "we don't need that abstraction yet" is usually said about the modifiability work rather than the feature work.

I don't want to be pompous about this. But I do think there's a lot to be said for spending a few cycles critically thinking about the proper abstractions and primitives you need for something you're working on, in a way that makes your life and the lives of the developers around you easier. Part of engineering is being able to decompose difficult, complex problems into approachable chunks, and I think good engineers are anticipatory. That anticipation is a skill, not a vice.

## Sight Reading

![A sheet of music resting on a pale oak music stand in bright, even light]({{ '/assets/images/generated/you-are-going-to-need-it-1.jpeg' | relative_url }})

Here's the analogy I keep coming back to. I'm a musician, and I grew up as a band kid, so we did competitions. One of the things you do in those competitions is sight reading. For those not familiar: you and your group are handed a piece of sheet music, and you're not allowed to practice it or work out your parts. You get a few minutes to read it, and then you're expected to perform it on the fly and be judged on how musically you follow the piece.

I remember a seminar at what I believe was the Santa Cruz Jazz Festival where the instructor talked about the value of sight reading. He asked how many of us liked to play music, and we all raised our hands. He asked how much we liked playing in front of people, and we all raised our hands again. Then he asked how many of us loved to practice. Some hands went up. Not everyone's.

His point was that sight reading makes you a better musician because it compresses the loop. It helps you learn pieces faster, and music in general faster, and it gets you to the point where you can pick up something new and perform it at performance level.

Now think about the arc of an engineering career. A lot of junior engineers are not great, and they can be slow. As you move into mid-level you get a little better and a little faster. And as you move up, there's a matrix effect between how good your code is and how fast you can produce it. The best engineers are the ones who can write good code quickly, and by my definition good code includes defining the proper abstractions that make your life easier as you build out whatever you're working on.

I think the best engineers are sight reading their code. What I mean is that when they're decomposing a problem, the question isn't just *can I play these notes*. It isn't even *can I play the right notes*. It's *can I play these notes musically, in a way that's sonically pleasing*. The same is true of code. The best engineers draw on their experience, their intuition, and their technical knowledge to pattern match: this element of the code is something it would be useful to abstract early, this other area probably not. They're writing near-production code on the first pass, they're doing it quickly, and they know when to make the trade between "you aren't gonna need it" and "you probably are going to need it."

And the baseline keeps moving. As you get better at writing production-grade code with properly chosen abstractions and primitives, a larger and larger chunk of what you write is production-grade the first time. You get faster at it, so you solve problems quickly, but you also one-shot them better. That, to me, is the mark of a good engineer.

## A Recent Example

I'll give a concrete example, and I'm going to keep the specifics somewhat generic.

I was recently working on a pipeline for an AI automation use case. We use [Tangle](https://shopify.engineering/tangle) at Shopify, which is open source, and as a side note from my past data engineering experience I've been genuinely impressed with it. I'm not just shilling for my employer here. The content-based caching per task is really sweet, and it's saved me the pain of building caching that I've otherwise had to build myself in Airflow or in custom solutions.

Tangle works on a component pattern, where components get composed into pipelines. So one of the conversations we kept having as we started this new thing was how to build it. There was a real emphasis on speed. We wanted to move fast, and there was a healthy dose of YAGNI in those conversations.

I spent a lot of time thinking about what our core primitives actually were, and I landed on two.

The first was retrieving data from a data store in an abstracted way, so that you weren't writing custom Python every time you needed data. You configure the component against your data store, configure a query, and get your data back as a Tangle manifest so it can be used in the pipeline.

The second was scaling a large number of agent tasks. We have some internal infrastructure that makes this easier, but I wanted a heavily abstracted component around how we fan work out to a large number of agent sessions.

The bet was that spending a couple of extra cycles making these primitives easy to use would be an accelerant, because we already knew out of the gate that we were going to build a series of pipelines to support this automation effort. This was never going to be one pipeline.

Then we had to make an infrastructure pivot. We had assumed one internal solution and moved to a different one, and it turned out the new one had a capability we hadn't been aware of when we designed the highly parallel agent session architecture. Because we already had that abstracted component, I was able to build a POC extremely quickly, and then we were able to scale on top of it just as quickly. Scaling had been the hard part with the original architecture. It was straining at a few dozen concurrent tasks. We're currently testing at a scale roughly thirty times that.

That's the payoff I was after. Rather than looking for the shortest path to getting something out, I did a bit of critical thinking and problem solving up front to engineer something that's scalable and elegant for extension.

And the anticipation wasn't really a guess. Over the last few years I've built a number of architectures shaped like this: how do I churn through a bunch of data using agents, reliably and at scale? Drawing on that experience, I recognized that the pattern wasn't unique to this one pipeline, and honestly it wasn't unique to this project either. Take data, feed it to a large number of parallel agents that operate over that data, collect the results, then do something with the results. That's a pattern worth accelerating.

I had some real discussions with other engineers about whether this was premature optimization. I felt convicted that it wasn't, based on my experience and on what we knew we had coming. I think it's already paid off.

## AI Makes This Trade Cheaper, Not Less Important

![A single brass rod fanning out into dozens of fine brass wires against a warm white surface]({{ '/assets/images/generated/you-are-going-to-need-it-2.jpeg' | relative_url }})

Here's where I think this matters more now than it used to.

With AI, the cost of implementation is so much cheaper and faster than it's ever been. So if the price of a better abstraction is you spending a few brain cycles to specify it more precisely to your agent, the trade-off is far, far less than it's ever been.

What I find interesting about this moment is that so many people have coalesced around the idea that AI helps us go faster. It does. But I really think there's less of an excuse for writing low-quality code now than there was before, which sounds crazy in a world where people are lobbing AI slop grenades at each other. Because AI lets you iterate so fast, and because it does a pretty good job of implementing your ideas, it affords you more space to think critically about the systems you're building and the code you're writing.

It just requires a little more self-discipline to actually use that space, rather than pulling the roulette wheel of the agent. By that I mean throwing things at the agent and hoping you get good output back. The way I look at it, the agent helps with implementation and it helps with discovery, especially working through existing codebases or unfamiliar frameworks. The thinking about what to build is still mine.

I've written before that [we infantilized programmers]({% post_url 2026-07-22-build-your-own-table %}). For those of us who consider ourselves software engineers, who believe in applying real engineering principles to the work and holding ourselves to that standard, I think falling too far into YAGNI is dangerous and counterproductive.

## Where I Land

As with everything I write, this is just my perspective. It may change over time, and I may be wrong. That's fine with me, and I'm open to the alternative.

I also don't have a clean rule for when to abstract and when not to, and I don't think one exists. That's part of why "you aren't gonna need it" is so appealing as a default. It's a rule, and rules are easier than judgment. What I'd push back on is treating it as the thing you do until proven otherwise, which is the framework I think a lot of engineers are operating under right now.

There's something to be said for the art of picking good abstractions and writing high-quality code, and I think a reflexive YAGNI can be detrimental to developing the engineer who is both good and fast. It's the equivalent of playing the notes with no dynamics and no flair. The notes are right. It just isn't music.
