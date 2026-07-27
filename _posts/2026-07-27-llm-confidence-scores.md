---
layout: post
title: "Why I Hate LLM Confidence Scores"
date: 2026-07-27
image: /assets/images/generated/llm-confidence-scores-header.jpeg
tags: [ai, llm, rag, evaluation, prompt engineering, musings]
---

## Hello, Reader

If someone sent you this post, you have probably tried to extrude a confidence score out of an LLM.

I've now had this conversation at multiple companies with multiple people, and I've had it enough times that it seems like there's a broader misunderstanding at work here. So my hope is that I can just send people this post instead of relitigating it in a thread every six months.

The short version: asking an LLM to generate a score for how confident it is in its own response is, from everything I can tell, **completely useless**.

I want to be upfront that I'd love to be wrong about this. There are people much, much smarter than me working in this space (and I work with many of them!). If you can rebut any of the arguments below, or point me at research I haven't read, I would genuinely enjoy that conversation. But absent that, these are my current thoughts as I understand them.

## What I Keep Seeing

The pattern shows up everywhere. Chat-based outputs, structured outputs, agentic task results. Someone wants the model to hand back a JSON object with a `response` key and a `confidence` key. And more often than not, that confidence key is a continuous score from 0 to 100.

That continuous scale is what really grinds my gears, and I'll come back to why. But the broader problem is that there's no scientific validity behind any of it. What you have built is a psychological safety trick. It makes the output *feel* more trustworthy without making it more trustworthy, and I'd argue the people shipping this experience are mostly lying to themselves about what they've shipped.

## LLMs Cannot Rank the Confidence of Their Own Responses

![Two facing brass-framed mirrors reflecting each other into an endless receding tunnel]({{ '/assets/images/generated/llm-confidence-scores-1.jpeg' | relative_url }})

I recognize that Anthropic and others have published research arguing that models maintain some kind of latent internal state while they generate. Anthropic's interpretability work on [tracing the thoughts of a language model](https://www.anthropic.com/research/tracing-thoughts-language-model) found that Claude plans several words ahead when writing a rhyming couplet, which is not the behavior you'd predict from a naive next-token story. And their more recent work on [emergent introspective awareness](https://transformer-circuits.pub/2025/introspection/index.html) found that models can sometimes notice concepts injected into their activations and report on them accurately.

That's real, and it's interesting. But read the caveat the researchers themselves put on it: the capability is highly unreliable and highly context-dependent. We do not currently have a strong enough understanding of that internal state to assert that models have any usable ability to assess their own correctness. Noticing that something was injected into your activations under laboratory conditions is a very long way from quantifying how likely your paragraph about a customer's refund policy is to be right.

If we think about what's happening under the hood, there is some quasi-cognition going on in the sense of symbolic relationships between aspects of language. With reasoning models, there's some observation of that process happening too. But this is where the whole thing collapses for me, because it immediately regresses into a who-watches-the-watchmen problem.

Say we want to tap into the thinking trace and use it to evaluate the self-correctness of a response. Fine. That approach has yielded real performance benefits, and I don't dispute those. But if we're talking about actually quantifying confidence, the thinking step can't rescue us, because the obvious next question is: what's the confidence of the confidence score produced by my thinking step? And then what's the confidence of *that*? It's confidence all the way down.

Do I think reflective reasoning patterns help models catch some of their own errors? Yes. Do I think models currently have a sufficient understanding of their own state to *quantify* that? No. It's also worth noting that the research on intrinsic self-correction is not especially encouraging on this front. The DeepMind paper [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) found that when models attempt to correct their initial responses using only their inherent capabilities, without external feedback, performance often *degrades*.

## Confident Of What, Exactly?

Here's the question I now ask immediately whenever someone requests a confidence score: what is your heuristic for confidence?

Because "confidence" gets ambiguous extremely fast. Not slightly ambiguous. Extremely.

Is the model confident in the correctness of the response? In the coherence of the response? That it has attempted to fulfill the goal of the user's request? Those are three completely different questions with three completely different failure modes, and a single float between 0 and 1 flattens all of them into the same number. Absent some heuristic that bounds the concept, these scores are effectively useless.

## Confidence Isn't Uniform Across a Response

![Oak blocks of varying heights with a single straight brass rod laid across the tallest few]({{ '/assets/images/generated/llm-confidence-scores-2.jpeg' | relative_url }})

There's another problem with treating this as a single number, and it goes back to internal state.

In traditional machine learning, we have real mechanisms for this. Confidence intervals. Classifiers that output a score that at least serves as a legitimate proxy for confidence. The closest analog an LLM has is the predicted likelihood of each next token.

As a side note, I think "LLMs just lossily predict the next token" has become a real oversimplification of where these systems are, especially once you account for reasoning, adaptive thinking, post-training, and the classifiers running on top of the response. But set that aside and take the most simplistic version.

Even there, the problem is that tokens are not uniform. If I'm generating the first hundred words of a response, every single token has its own likelihood value. Some of those are structural glue with near-certain probabilities. Some of them are the load-bearing factual claim in the entire paragraph. Collapsing that distribution into one number that the model then verbalizes is not a measurement. It's a vibe.

And I've gone looking. From every piece of research I've been able to find, I can't locate a scenario where these self-reported scores demonstrate the kind of validity people assume they have when they put them in a JSON schema.

## If You Really Wanted One, Here's the Work

I want to be clear that I'm not claiming it's impossible to get some reliable indication of confidence out of an LLM. I'm claiming that nobody I've met wants it badly enough to do the work required.

That work would look something like this. You'd need a strong prompt calibration process in which you define actual heuristics for the model to self-classify against, preferably across a small set of categorical labels rather than a continuous 0-to-100 scale. Then you'd need a lot of calibration and prompt optimization to demonstrate, over some sufficiently large *n* of responses, that the scores are actually truthy.

The research here is more supportive than my general position might suggest, and I want to represent it fairly. Lin, Hilton, and Evans showed in [Teaching Models to Express Their Uncertainty in Words](https://arxiv.org/abs/2205.14334) that a model can be trained to emit calibrated verbal confidence, though notably they fine-tuned on a purpose-built task distribution to get there. Tian et al. found in [Just Ask for Calibration](https://arxiv.org/abs/2305.14975) that with the right prompting strategy, RLHF'd models verbalize probabilities that are better calibrated than the model's own conditional probabilities, and that prompting plus temperature scaling can cut expected calibration error by more than half. And Anthropic's [Language Models (Mostly) Know What They Know](https://arxiv.org/abs/2207.05221) found encouraging results asking models to estimate the probability that their own proposed answer is true.

That's the strongest case against me, and I take it seriously. But look at what all three have in common: fine-tuning, or a deliberately chosen prompting strategy, or a constrained answer format, or explicit post-hoc scaling. That's the calibration work. It is not what happens when you add `"confidence": number` to a Pydantic model and ship it.

Meanwhile, the argument for categorical over continuous keeps getting stronger. Xiong et al.'s [empirical evaluation of confidence elicitation](https://arxiv.org/abs/2306.13063) documented how badly overconfident verbalized scores tend to be. And a paper from earlier this year, [Rescaling Confidence: What Scale Design Reveals About LLM Metacognition](https://arxiv.org/abs/2603.09309), found something I find genuinely damning: models don't use the 0-to-100 scale as a continuous spectrum at all. They cluster on round-number anchors. Across six models, more than 78% of responses landed on just three values, with one model reporting exactly 100 on 68% of instances. Coarser scales performed *better* on metacognitive sensitivity than the 0-to-100 baseline.

So the continuous score that everyone reaches for first is the one with the least support in the literature. If you're going to do this at all, the label set should be small and the categories should mean something specific that you defined.

Which brings me to a related gripe. LLMs do function decently as ad hoc classifiers, and I'll grant that. But I think reaching for one is usually a lazy approach. It's great for labeling synthetic data or for genuinely ad hoc work where you're not strict on the success criteria. For anything serious in production, I'd much rather train a classical classifier, even if I use an LLM to help bootstrap the training data. And note that if you go the categorical-confidence route, you're right back to needing humans to define the heuristics behind each label anyway.

## Confidence Is Almost Always a Proxy for Correctness

![A level brass balance scale holding a solid oak cube on one pan and a hollow brass box of the same size on the other]({{ '/assets/images/generated/llm-confidence-scores-3.jpeg' | relative_url }})

At least the way I've seen it used in practice, "confidence" is really a stand-in for correctness, or for certainty. Which makes it another variation of the factuality and grounding problem wearing a different hat.

Case in point: most of the examples I encounter are RAG use cases. Somebody wants the model to indicate whether it's confident it retrieved the right documents, pulled the data it actually needed, and that its response is accurate to what it pulled. It's being used as a trust signal.

Here's where I think that gets genuinely risky, and it's not the objection people expect. A big part of the value of an LLM in a retrieval system is synthesis. Suppose we perfectly tuned a confidence score where the heuristic was "every explicit fact in this response is grounded in a retrieved document." Optimizing hard toward that score would reduce the model's willingness to synthesize across sources. Yes, ideally you'd end up with a set of verified facts and the model could still draw assertions between them. But I've seen enough side effects from prompt optimization that I'd be skeptical of overtuning toward aggressively cited factuality, because a lot of the value is the model inferring across retrieved context and its training data to get somewhere neither one contained on its own.

There's also a cost problem hiding in that heuristic. If correctness means "cited in an external source," how do you validate a fact that came from training data? You end up spending retrieval calls on things that are self-evident. I don't want my LLM making a web search call to find out whether the sky is blue. That's a waste of my time and a waste of my tokens.

I'd expect a model's training data to be strong enough that if I asked it to check the claims in its own response, it could handle "the sky is blue" without assistance. Absent some ecological phenomenon, or chemical/biological warfare, that one is settled. Where it gets genuinely hard is specific business logic for a process the model has been asked to operate inside of, and that's exactly where you start losing the synthesis and the intuition that made the model useful in the first place.

## Every Line of a Prompt Is a Liability

![A brass pendulum frozen at the far end of its swing, past the center mark scored into an oak base]({{ '/assets/images/generated/llm-confidence-scores-4.jpeg' | relative_url }})

I want to take a detour, because this is the part I think people underestimate most.

At this point I've been working on LLM experiences for several years, and I cannot tell you how many times I've watched a team go off the rails by tuning a prompt to correct a specific issue and overcorrecting straight past the target.

One example sticks with me. In one of our support experiences, we had a problem where the LLM wasn't reliably finding the documents that detailed our escalation process. So we did some prompt optimization against some ad hoc evals to correct it. And we shifted it so far that the model then *often* found an escalation path immediately, without ever considering what our frontline advisors could resolve themselves. We'd spent months responding to feedback to produce a system that had learned exactly the wrong lesson.

I laugh about it now, but it's the example that made something click for me. Much like how every line of code is a liability, every line of a prompt is a liability, because each one expands the latent space around the outcome you're trying to drive. Models are as good at inferring the space around what you *didn't* say as they are at adhering to what you did.

Absent a sufficiently holistic, goal-oriented rubric that grounds your optimization process in overall answer quality, targeted prompt fixes tend to produce exactly this kind of pendulum swing.

This is a big part of why I now try to write the most minimal prompts I can get away with. Partly because minimal prompts let me evaluate the actual causal capability of a given model rather than measuring how well I've tuned around it. That's the persistent downside of aggressive prompt optimization: you're optimizing against a specific model and architecture, so swapping models becomes a project. This has gotten much better, to be fair. Compared to the GPT-4o days, where changing providers meant substantial rework, today's models are forgiving enough that you can often drop in a replacement. But the effect hasn't disappeared, even between model sizes within a single provider. Moving between Sonnet and Opus can still surface places where you've overfit. Mostly, though, minimal prompts help me avoid the overcorrection problem before it starts.

All of which is to say: the path to a reliable confidence score runs directly through the kind of prompt optimization that I've watched produce bad second and third-order effects over and over.

## If the Model Knows It's Wrong, I Want It to Fix It

This is the argument I keep coming back to, and I think it's the one that actually settles it.

If a model is aware that it has an ungrounded assertion in its response, I would much rather it stay in its tool loop, go find a source for that claim, or drop the claim entirely, and *then* hand me the response. What good does it do me for the model to be aware of its own incorrectness and ship it anyway with a sticker on it?

If the model is aware enough to know something is wrong, just correct it. If it isn't, then the confidence score it's giving me is not measuring anything.

There's no third option that I can see. Which is why I don't think these scores do anything for reliability. They serve as a psychological tool for the humans reading the output, and that's a different product requirement than the one people think they're solving.

## The Actual Work Is Search

If your confidence score is a proxy for correctness, and your correctness heuristic is grounding in retrieved sources, then what you actually have is a retrieval problem. So put the energy there.

I don't think this is a solved problem at any level of the industry, and I want to be clear that I'm not just talking about the systems I've worked on. I see it in commercially available frontier products. I see it in deep research features and web search features from the labs themselves. I see it in Perplexity. The other day I was using ChatGPT to research BBQ competitions, asked it about entry deadlines, and it returned one from 2024, with a cited source. Not a subtle failure. And the question I'm left with isn't "why didn't the model tell me it was unsure." It's why, in its search and in its selection of which documents to trust, it made an obviously wrong choice.

A model's retrieval is only as good as the information fed into it and the quality of the search it performs. That's where I'd spend the effort.

I'd also push back gently on the framing that motivates a lot of these requests. Mikhail Parakhin, Shopify's CTO, has made a point a couple of times when I've heard him speak, both internally and externally, that we only call things hallucinations when they're wrong. Otherwise, when the output is what we wanted, we call it creativity. He's been [making that argument publicly](https://x.com/MParakhin/status/1629010494257303558) since his Bing days. It's the same mechanism producing both, and that's worth sitting with before you go optimizing it out.

Sometimes it feels like what people really want out of these RAG systems is the thing we had before. I built chatbots back in 2017 when everything was intent-based (shoutout to the Covered California chatbot back in the day, IYKYK), and you'd try to enumerate the whole spectrum of possible user intents and map each one to a specific condition. You could wire those intents through something like Microsoft's [LUIS](https://learn.microsoft.com/en-us/azure/ai-services/luis/what-is-luis) into a knowledge management tool and retrieve specific, cited information every time. Deterministic and auditable, and also brittle and incapable of anything you hadn't anticipated. I understand the pull. It's hard to trust a system that can be wrong in ways you didn't enumerate. But asking for a confidence score is trying to buy back that determinism with a number the model made up.

## Things Move Fast

So, in conclusion: I struggle to see the value in getting a model to output a confidence score, and I struggle to see a way to have it do so reliably. There may be a version of this that works with serious prompt calibration and a small set of well-defined categorical labels, but I think the second and third-order effects of that calibration would likely be negative, and I've yet to meet anyone who wanted the score badly enough to find out. And as you scrutinize what you actually intend to *do* with the number, the whole thing tends to fall apart under a bit of critical logic.

Like I say in most writings where I make an argument, I'm super open to being wrong here, so if you've got the paper that changes my mind, please send it.
