# What to build

[Home](../README.md) / What to build

Voice agents work well for some jobs and fail in public for others. This page
sorts the common use cases by how hard they are and how much they're worth, using
what builders, buyers and researchers reported up to September 2026.

**On this page:** [The short version](#the-short-version) ·
[Good first projects](#good-first-projects) · [Every use case, rated](#every-use-case-rated) ·
[Avoid at first](#avoid-at-first) · [Five lessons from the field](#five-lessons-from-the-field) ·
[Read vendor numbers carefully](#read-vendor-numbers-carefully)

## The short version

Pick **one narrow, inbound, repeatable kind of call** where a missed call costs
real money and a mistake is cheap to undo. Put ordinary code between the model and
anything with consequences. Tell callers it's an AI and give them a fast way to
reach a person.

![Eighteen voice agent use cases placed on a grid of difficulty against value. Good first projects sit at medium difficulty and medium to high value.](../assets/diagrams/use-case-map.svg)

## Good first projects

| Project | Why it's a good start | The hard part |
| --- | --- | --- |
| **After-hours answering and message taking** | Bounded, low stakes, and a missed call has a clear cost | Getting callers to stay on the line; capturing names and numbers correctly |
| **Appointment booking against a real calendar** | A clear job with a clear success measure | Real-time calendar access, and checks such as insurance or eligibility before booking |
| **Restaurant and hotel phones** (hours, menu, reservations) | Many calls ask the same few things | Live reservation or ordering-system integration and busy periods |
| **Structured interviews** (hiring screens, research interviews) | Scripted, and the best-measured success in the field | Disclosure, fairness and keeping transcripts secure |
| **Speaking practice and oral exams** | Known users and a bounded script | Recognising learners' speech; pacing and one question at a time |
| **Check calls to known businesses** (freight status, appointment confirmations) | Repetitive calls to people who expect them | Exceptions and noisy lines |

## Every use case, rated

Difficulty and value run from 1 (low) to 5 (high). They are judgements drawn from
the sources below, not measurements. **Evidence** says how solid the proof is:
*strong* means independent measurement, *mixed* means anecdotes or conflicting
claims, and *thin* means vendor claims only.

| Use case | Works today? | Difficulty | Value | Evidence | Why it struggles |
| --- | --- | :---: | :---: | --- | --- |
| Healthcare front desk, reminders, outreach | Partly | 4 | 5 | mixed | Accents and atypical speech, eligibility rules, cost of a wrong answer |
| Bank, insurer and telco customer service | Mixed | 4 | 4 | mixed | Long tail of requests, caller authentication, right-to-a-human rules |
| Drive-thru ordering | Partly, with humans behind it | 5 | 4 | mixed | Noise, accents, custom orders, pranks, no hard limits on what the model can order |
| AI-led interviews (hiring, research) | Yes, with disclosure | 3 | 4 | strong | Candidate distrust when it isn't disclosed, data security |
| Language tutoring and speaking practice | Yes, for practice | 3 | 4 | mixed | Learner speech, remembering the learner's level, feedback that is too kind |
| Freight and logistics check calls | Claimed at scale | 3 | 4 | thin | Exceptions such as weather delays (inferred) |
| Small-business receptionist | Mixed | 3 | 3 | mixed | Callers who hang up on bots, booking without real schedule checks, unclear return for the owner |
| Restaurant and hotel phones | Probably | 3 | 3 | thin | Few independent reports either way |
| Speed-to-lead call-backs | Plausible | 3 | 3 | thin | Consent must be captured on the lead form |
| Oral exams and assessment | Yes, in a small pilot | 2 | 3 | one detailed write-up | Stacked questions, rushed silences, an intimidating voice |
| Debt collection and payment reminders | Unproven | 5 | 3 | thin | Strict call-frequency and time-window rules, consent, lawsuits |
| Companions, talking toys, game characters | Not recommended | 4 | 3 | mixed to thin | Child safety, content control, voice and likeness rights |
| In-car assistants | Early, users push back | 5 | 3 | mixed | Wordy answers, road noise, driver distraction |
| Accessibility (atypical speech) | Improving | 4 | 3 | moderate | Scarce training data, big differences between speakers |
| Government 311 and 911 | Narrowly | 4 | 3 | one city | Triage errors, disclosure, slow procurement |
| Outbound cold calling and AI sales reps | Not recommended | 5 | 2 | mixed | Consent rules with per-call damages, low answer rates, spam labels |
| Personal assistants that call businesses for you | Early | 3 | 2 | thin | Verification steps, phone menus, trust, big platforms entering |
| Reselling agents to local businesses | Unproven as a business | 2 | 2 | mixed | Weak customer pain, churn, hype and regulator attention |

## Avoid at first

- **Outbound cold calling and collections** without consent tracking, do-not-call
  scrubbing and calling-hour rules built in code. In the US an AI voice counts as
  an artificial voice, which needs prior consent. Read the
  [phone compliance skill](../skills/foundations/voice-phone-compliance/SKILL.md) first.
- **Open-ended companions or toys for children.** A companion app ended open chat
  for under-18s after lawsuits
  ([CNBC](https://www.cnbc.com/2025/10/29/character-ai-chatbots-teens-persona.html)),
  and a chatbot teddy bear was pulled after testers got explicit replies
  ([PIRG](https://pirg.org/washington/resources/ai-toys/)).
- **Drive-thru and in-car voice**, which depend on enterprise partners and are
  hard even for the biggest teams
  ([BBC on Taco Bell](https://www.bbc.com/news/articles/ckgyk2p55g8o)).
- **"Start an AI agency" income promises.** The FTC sued one seller of
  conversational AI business opportunities over its earnings claims
  ([FTC](https://www.ftc.gov/news-events/news/press-releases/2025/08/ftc-sues-stop-air-ai-using-deceptive-claims-about-business-growth-earnings-potential-refund)).

## Five lessons from the field

1. **Narrow scope wins.** What works again and again is a bounded job: after-hours
   capture, booking, status checks, scripted interviews. What fails is broad,
   high-stakes intake. An NYU course ran oral exams for 36 students with a voice
   agent for about $0.42 each by keeping the script tight
   ([write-up](https://www.behind-the-enemy-lines.com/2025/12/fighting-fire-with-fire-scalable-oral.html)).
2. **Put code between the model and consequences.** Check the menu, calendar,
   eligibility or payment rules in code before the agent commits anything. The
   drive-thru failures read as missing hard limits, not proof that voice ordering
   can't work. The [conversation design skill](../skills/foundations/voice-conversation-design/SKILL.md)
   covers confirmations and action states.
3. **Measure resolved calls, not answered calls.** Track what the caller needed,
   whether it happened, and how handoffs went. The
   [agent evaluation skill](../skills/foundations/voice-agent-evaluation/SKILL.md)
   builds that test set.
4. **Disclose, and keep a person close.** A field experiment with 70,000 job
   applicants found AI-led interviews led to 12% more offers and 18% more job
   starts, and most applicants chose the AI when given the choice
   ([Jabarian and Henkel](https://arxiv.org/abs/2607.28222)). Yet in a survey,
   38% of candidates had walked away from an AI interview, and 70% weren't told
   up front ([Greenhouse](https://www.greenhouse.com/uk/newsroom/63-of-job-seekers-have-faced-an-ai-interview-most-havent-had-a-good-one-yet)).
   How you run it decides which result you get.
5. **Test with real callers and real audio before you scale.** A GP surgery's AI
   receptionist struggled with local accents and speech differences, and patients
   walked in or hung up instead
   ([Healthwatch Rotherham](https://healthwatchrotherham.org.uk/blog/2026-07-10/patient-concern-over-ai-receptionist-emma-what-you-need-know)).

## Read vendor numbers carefully

Automation rates depend on how they are counted:

- Wendy's reported 86% of drive-thru orders taken without a team member stepping
  in, and nearly 99% if you count orders a person fixed
  ([Wendy's](https://www.wendys.com/blog/wendysr-square-deal-blog/transforming-ordering-experience-wendys-freshai-update)).
- The SEC found that a drive-thru "AI" company advertising 95%+ non-intervention
  had off-site humans handling most orders
  ([SEC order](https://www.sec.gov/enforcement-litigation/administrative-proceedings/33-11352-s)).
- A bank cut jobs citing 2,000 fewer calls a week, then reversed the cuts after
  its union said call volumes were rising
  ([ABC News](https://www.abc.net.au/news/2025-08-21/cba-backtracks-on-ai-job-cuts-as-chatbot-lifts-call-volumes/105679492)).

Ask what counts as "handled", who fixed the failures, and over what period.
Before you promise savings, run the numbers with the
[cost estimation skill](../skills/foundations/voice-cost-estimation/SKILL.md).

---

**About these ratings.** Compiled on September 30, 2026 from news reports,
regulator filings, research papers, vendor case studies and builder discussions.
Most outcome numbers in customer service come from the companies that deployed
or sold the agent; independent data is scarce for collections, insurance,
real-estate call-backs, restaurant phones and small-business receptionists, so
treat those rows as lower confidence. Corrections with sources are welcome:
[open an issue](https://github.com/RBStrayer/nl-voice-skills/issues/new/choose).
