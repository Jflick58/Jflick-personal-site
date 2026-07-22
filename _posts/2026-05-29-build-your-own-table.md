---
layout: post
title: "Build Your Own Table"
date: 2026-05-29
image: /assets/images/generated/build-your-own-table-header.jpeg
tags: [career, ai, software development, engineering management, mentorship, musings]
---

## A New Social Contract

I've spent most of the last several years in roles where growing other people is part of the job. As a manager and a director, that came with the formal HR responsibility of advocating for someone's career. As a staff engineer, it's an expectation even without the org chart backing it up. It's the thing I like most about higher-level roles: the expectation is baked in, and there are usually formal practices that support it.

I've always gravitated toward this. It's why I speak at CS career events at local universities, why I'll help people with their resumes, and why, after debating in undergrad, I spent three or four years as an unpaid volunteer assistant coach at Sacramento State. The organizations and people who invested in me to get me where I am created a debt I feel I owe back. You pay it forward.

Lately a theme has come up in conversation after conversation. Shopify is a very impact-driven culture, which I appreciate, but it also means people are hungry about what goes on their impact reviews. Coming out of a review cycle, everyone is cognizant of the real impact they've driven. So I've been talking with a lot of people lately (mentees, colleagues, new interns, current CS students), and the question almost always boils down to the same thing: *how do I get myself into a position to have maximal impact, to be utilized, to have a seat at the table, to the point where I can attribute direct outcomes to my work?*

It's a question I've heard for my entire career. What's different now is the anxiety underneath it. The only way I can describe it is a kind of existential unease, like we're in the middle of negotiating a new social contract for the programming profession.

## The Old Contract, and the Roles We Built Around It

Let me use "programming" here as the broad umbrella. There are real distinctions inside it. As a side note, while the term "software engineer" has been completely diluted in the US, other places have stronger protections on who gets to call themselves an engineer. I'd argue there's a real difference between a software engineer, a developer, and a programmer in terms of the actual role. All software engineers are programmers; not all programmers are developers or software engineers.

The old contract went something like this: you either taught yourself, learned some complicated concepts, and proved you could ship working code, or you went through a university education and proved you could handle some above-average math, some difficult algorithmic and data structure work, a few languages, and the structured reasoning that comes with it. Because the barrier to entry was real, you could carve out a solid career being rewarded for executing a spec.

I remember a lot of conversations about this, especially at a startup where we were building out roles. The operating assumption was that the highest-value thing a person with a programming title could do was sit hands-on-keyboard and write code. So as an industry we built up a set of ancillary roles whose job was essentially to keep programmers from doing anything but program.

You see it in product management. Good product managers make my life substantially easier, and I've said that for years. The problem is the average product manager just isn't very good. More than almost any role, product management has a deeply subjective definition of success. It's subjective to the time period you're working in, to where the technical capabilities of the industry happen to sit, and to your ability to thread the needle between what's easily executable and what's actually possible. I've worked with brilliant PMs who explore the whole product space and bring a strongly reasoned perspective I could genuinely collaborate with. I've also worked with PMs who were a lossy translation layer and not much else.

The same pattern shows up elsewhere: enterprise project management, which is partly an artifact of inefficient corporate structures, and even the dedicated scrum master, which was in vogue for a while specifically to take the burden of self-organization off of engineers.

## Code Is Table Stakes Now

![A row of brass machinist tools on white marble, one worn tool set apart from the rest]({{ '/assets/images/generated/build-your-own-table-1.jpeg' | relative_url }})

Here's the irony: in 2026, the ability to execute on code is no longer the most valuable thing a software engineer brings to the table.

I've watched this happen in real time. First at the insurance company (a classical non-tech enterprise shop with a lot of corporate process) and now at Shopify (a big tech company with cultural principles built around moving fast). The most effective engineers I see, the ones rocketing up and having the largest impact, still have strong technical chops; I don't think that value has gone away. But they're also the ones driving strong ideation, who have a real product understanding, and who are opinionated about the *product* they're building, not just the code they're writing to build it.

That distinction matters enormously, especially for junior engineers, because the two things are symbiotic. I've always believed the engineers with better product understanding write better code, because they can match the abstractions in their code to the abstraction decisions in the product itself. That's how you get elegant codebases that are easy to extend, modify, and maintain.

Because we can theoretically move so fast now, some of the traditional corporate scaffolding is breaking down. I've been at Shopify just under a year and I've already seen a transformation in our GSD process (Get Shit Done) and how tightly we adhere to its formal structure. The process can't always keep up with empowered teams that sit close to the product and move very quickly.

I'll add a caveat, because I think it matters. We're entering a world where anyone can pull the roulette wheel of agentic coding. I still believe good engineers flavor the output of agentic engineering, but the models are good enough now that I've watched non-technical people get decent code out of genuinely crummy, undirected prompts. I've also watched junior engineers treat it like a roulette wheel, which is a different problem for a different day. Either way, in big tech and probably even more so in startups, you're going to have the largest impact by being more than just a programmer. Your programming skill becomes an amplifier of your ability to be opinionated about the product and to organize the execution of a project.

## We Infantilized Programmers

I know what some people are thinking. We're collapsing a bunch of roles into the software engineer and raising expectations for no additional pay. Maybe there's a fair criticism there.

But I think the premise is wrong. The view that multiple roles are collapsing *into* software engineering assumes we were right to strip those expectations out in the first place. I'd argue we weren't. I think we hyper-optimized the software engineering role into a pure programming role, and in doing so we did a lot of engineers a disservice. Instead of complete professionals who understand the product end to end and can organize themselves, we built code jockeys. That's part of the struggle now.

And to be clear, I love writing code. I love the feeling of building an elegant interface for an application, of hunting down a bug, of squeezing performance out of something slow. I loved getting data pipelines down to subsecond latencies across a large number of threads. I loved digging into the innards of Pandas to figure out how to parallelize operations across DataFrames safely. I loved restructuring our ML approaches to take advantage of a distributed training environment. I enjoyed all of those problems.

But like most things as an industry matures, these things become table stakes, and you have to move up a level of abstraction.

## The Part That's Hard to Teach

Even when I was deep in the code, I was always curious (some would say precocious) about everything around it, because those things affected my efficacy as an engineer.

Poor project management caused inefficiencies that hurt my ability to know what to execute on. I remember one situation vividly. Our reporting was focused on building fancy dashboards for executive presentations rather than reflecting reality, so engineers would keep building while reports got assembled over two or three days. By the time it reached the executive at the end of the week, the question was: *why aren't the engineers further along?* After answering that enough times, I decided I needed to be opinionated about project management and tie those processes directly into how we tracked progress in the code, so I could describe accurately and quickly where we actually were. Our project managers appreciated engineers owning more of the reporting, and the meetings got more honest. We could finally talk about real blockers.

I was the same way about product. At that startup we had two product components that made a lot of sense to bridge once we started extending into API interfaces, trying to make some of our data services self-serve and cut down the manual reporting effort. I dove into the backend to understand how the product was actually being used, found the right integration points for those data services, and identified product abstractions we could reuse to enable self-service. The result was a better experience for customers and a more capable product, because nobody had to babysit a manual flow just to get data in for analysis.

These are hard things to teach. I wish I could rip the precociousness out of my own head and implant it in the junior engineers I work with. I can't. The best I can do is describe what I see: the frameworks that have worked for me, and the patterns I notice in the people who are elevated within my company and the industry.

There's one engineer I work with who I think about a lot. They take an extremely high degree of ownership, they're opinionated about the product, and they really help organize the team. They're a software engineer, but their impact on the business is very high. Having been a director in a thirty-person engineering org, I can tell you that's the difference. The engineers who become a cornerstone, who become *sticky*, are the ones with outsized impact on the process, on the business, on the team. The good coders who just pull tickets off the board and execute them always became question marks, and in some cases they unfortunately became layoff targets. That gets amplified when good engineers can produce decent code with AI very quickly. The edge moves to the ability to synthesize your knowledge and experience, to see across the stack and across the organization in ways we can't currently encode in a prompt, and to produce something novel out of it.

## Dress for the Job You Want

The more of these conversations I have, the more I notice that some people just seem to come out of the box with it: the organizational skills, the follow-up, the communication, the ownership. It would be easy to file those under the same heading as precociousness, as things you either have or you don't. But I was trying to explain to a junior developer I mentor that there's an old saying about dressing for the job you want, not the job you have. I'm sure HR gets sick of me dressing up as Batman, but outside of the cliche and the jokes, I think there's some reality to it.

![Batman meme: my boss told me to dress for the job you want, not the job you have. Now I'm sitting in a disciplinary meeting dressed as Batman.]({{ '/assets/images/batman-dress-for-the-job.jpeg' | relative_url }})

Here's the distinction. You may not have the technical knowledge or the experience that people at higher levels have, and you can't wake up tomorrow and decide to have it. Some of that only comes with time, and I respect that. But there are traits you *can* wake up tomorrow and decide to emulate: organization, communication, ownership. I've watched junior developers who are strong technically but can't seem to make one idea click: they aren't just junior engineers anymore; they're professional software engineers, and they can take real ownership over things.

Ownership starts with asking questions. When your boss comes to you and says *I need you to do this thing*, don't just do it. Ask why. (Maybe don't ask "why" obnoxiously; that can come off a little precocious.) Ask what's driving it. What's the context? Who's asking for this, and who's pushing for it? Then interrogate a little. Why are we doing it the way we're doing it? What are the reasons behind the design? Junior developers, and plenty of mid-level developers too, feel uncomfortable inserting themselves into a project through questioning. But I approach every project by asking how I can add value to it. Lots of engineers, especially in the age of AI, can take a ticket and do it. I view my job differently. My job is not to take a thing and execute it. My job is to apply my knowledge, my skills, my experience, and my critical thinking to uniquely make the things I'm working on better.

Maybe I'm at an advantage because I worked for a startup early in my career. I became a data engineer with a huge scope of responsibility for the ETL pipelines of a company whose primary product was the data being collected. When I walked in, the ETL scripts I owned were literally scripts running on the head data scientist's laptop (which lived under his desk). We were trying to scale; customers wanted more and more data, and we needed to process it faster. This was a critical flow of the business, so I had to figure it out. I had to ask the questions, understand all the constraints, and own the outcome. It wasn't enough to build an ETL pipeline; I had to build it in a way that met our business objectives, and I had to build it reliably. That experience shaped my mindset around really owning outcomes more than anything else in my career.

The communication side is similar. When I start on a project, I overcommunicate. I give frequent updates, try to be very clear, and pull people into the conversation to make sure we're all on the same page with the design. I'm also not shy about going through different departments to figure things out and to get people moving on the things that need to get done. A lot of people just don't operate with that level of ownership. They look at the task, go off, and do the task, but they never own the outcome or the end-to-end execution. And those are exactly the traits you're expected to embody as you take on more responsibility. Unfortunately, some people never make those jumps, and they cap themselves no matter how strong they are technically.

So this has become the biggest piece of advice I give when I mentor: if there's a level you want to get to, wake up and start thinking of yourself as that level, and start trying to operate there. Look at the people around you and how they work: the ownership, the communication, the way they take a task and run with it, the improvements that come out of their analysis and critical thinking. You can do all of those things now. Yes, experience gives you a bigger base to draw from. I can ask more particular questions today because I've done enough projects to have caught myself deep in one, staring at something that needed a significant change, thinking: if only I had asked one question earlier, I could have avoided all this rework. As a staff engineer, I have that to draw on. But junior and mid-level developers, y'all can still do this without it. And doing it becomes an accelerant for your experience, because that level of ownership puts your back against the wall and forces you to really figure things out.

## Passion Is the Forcing Function

![A small oak seedling in a brass pot catching golden light, casting a long shadow]({{ '/assets/images/generated/build-your-own-table-2.jpeg' | relative_url }})

Some engineers I've talked to really struggle with the idea of being a novel ideator, and I don't know how to teach that directly either. But I think it comes from a place of passion about the work.

For me, the passion comes from something simple: if I'm going to spend 40 to 60 hours a week on something, I have to give a shit about it. I can't physically not care, because I know how valuable my time and my life are. If I'm doing something, I'm doing it at 110%, and that includes having strong opinions and trying to put my own stamp on it.

I was listening to a podcast recently and they quoted Cal Newport on passion and calling in one's work. The gist (and I may be misquoting) was that passion is a function of competence and confidence in your ability to do the work. That struck me, because it reframes the whole thing. A lot of people tell me they want the kind of organizational impact that requires bringing something novel, and the reality is we're now competing with AI synthesis. There's a lot AI doesn't have context for, or can't yet synthesize well. As humans we experience things differently; we filter and remember differently; we draw conclusions from things across the stack and the organization that were never properly documented. Some things are too wide and too nuanced to fit into a prompt.

Over time, as more organizations get their information into RAG systems and AI understands wider and wider stacks, this edge will narrow. But right now, the novel synthesis of your own experience with your problem domain, plus the undocumented and nuanced things you know about the stack and the organization, is the real value humans add on top of AI as a tool.

Here's where the reframe earned its keep for me. Some engineers say they don't feel close enough to the product to have a strong opinion, or that they haven't worked on something long enough to even generate ideas. You may not be able to manufacture novel ideation on command. But if you treat confidence and competence as the two levers that build passion, then focusing on those should, over time, develop the passion that leads to ideation.

I'll be honest that I'm making a logical leap there. I'm not certain there's a clean internal link between passion and ideation. But my own intuition is that a lot of my ability to ideate comes from how much I care about the work.

## How You Actually Develop It

So my new advice to interns, to junior engineers, to anyone who wants to stay impactful in this strange new environment, is to focus on developing passion, and to work on something you can be passionate about.

I'd err on the side of Newport's argument that passion can be developed. It isn't binary, and it isn't static. If something interests you, run toward it. Build your confidence working in the domains you find interesting and focus on building competence.

AI is a great tool for that, not so much for generating code as for helping you understand the codebase and the stack you're in. Yes, it gets things wrong. I run my AI in an IDE specifically so I can command-click through the references it surfaces and verify the specific things it tells me. But it can get you to a level of competence in a codebase fast enough that you can start to feel some passion for it.

Would I have said I was passionate about support tooling before I joined Shopify? No. I'm passionate about it now, because I've built confidence and, arguably, competence in it (you can ask my boss about that one), and I've come to understand it better. Now I genuinely want to make tooling that makes our merchants' lives better and makes the advisors who support those merchants more effective.

It's probably easier at a company like Shopify. Whatever general criticisms one can level at corporations, I find real solace in the stories of the people who build small businesses on the platform. I have friends and family who run stores. The testimony that sticks with me is the simplest one: *we wanted to sell t-shirts online, and Shopify made it easy.* Don't read this as a Shopify advertisement. But I do find meaning in that work. And the point generalizes. At the insurance company I was passionate about doing good work and building strong solutions. There's almost always something to find.

## Build Your Own Table

I'm skeptical of corporate values and I make fun of them constantly, but I've come to respect Shopify's GSD. Underneath the acronym it's really just: care, give a shit. Maybe that's naive. But I think the people who actually care get 10X further than the people who are pompously detached. Most of us are still employees building someone else's company, and that's a trade-off we make, but you can still find a lot of passion inside it.

In a world where pulling tickets and executing on them has become fast and cheap, there's still some value in a human supervising the AI and having opinions about how things get built. But you have to be more than that, and to be more than that, you have to care. It's hard to force otherwise.

I was joking with my own boss the other day that at least 25% of my career success comes down to the fact that I just speak up. You'd be surprised how many people keep their heads down and never do it, and how badly people underestimate the value of putting themselves out there.

I know this is harder in a big company, where it's easy to stay in your lane and think of yourself as nothing more than your current title or your current role. Some of you work in cultures where speaking up isn't as encouraged, and you may need to be strategic about how you do it. But I've worked at a variety of companies at this point in my career, and the vast majority of the time this approach, even when it gets read as precocious or pretentious, is the thing that has served me well.

So when people ask how to be impactful in 2026, how to grow their career, how to keep climbing in influence and pay, my answer comes back to building that seat for yourself. You build it through strong execution, ownership, and ideation, and I think ideation is an outflow of the passion and the give-a-shit-ness you bring. I can't teach the precociousness or the outspokenness I seem to have had inherently. But passion is something you can work to develop, and the fruit from that tree will carry you a long way. If you want the seat, if you want to be in the room, you have to get after it, and that starts with changing your mindset and refusing to be constrained by your current state.
