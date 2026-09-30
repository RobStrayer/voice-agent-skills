# Common problems and fixes

[Home](../README.md) / Common problems

The twenty problems builders hit most, with what causes them, what builders
report works, and the skill that helps. Compiled from about 660 public sources
from January 2025 to September 2026: GitHub issues, Hacker News threads, vendor
forums, engineering blogs, benchmarks and regulator documents.

Most fixes below are what builders say worked for them, not controlled
measurements. Where a number was measured with a published method, the text
says so.

![The twenty problems builders hit most, in four groups with a one-line fix each. The conversation: knowing when the caller is done, caller trust, names and numbers, interruptions, echo and noise, languages. Actions and the phone: phone plumbing, tool calls, guardrails, handoffs, voicemail and spam labels, consent. Choosing: platform, cost, one model or a pipeline. Running it: latency, reliability, observability, testing, changing APIs.](../assets/diagrams/common-problems.svg)

## Find your problem

| What you notice | Go to |
| --- | --- |
| Replies feel slow, or slower than the dashboard says | [1. Latency](#1-latency-callers-hear-is-not-what-the-dashboard-shows) |
| It cuts people off, or leaves long awkward gaps | [2. Turn-taking](#2-turn-taking-knowing-when-the-caller-has-finished) |
| Calls won't connect, audio is silent or choppy on the phone | [3. Phone plumbing](#3-phone-plumbing) |
| Can't decide between Vapi, Retell, LiveKit, Pipecat… | [4. Choosing a platform](#4-choosing-a-platform-and-avoiding-lock-in) |
| The bill is bigger than the advertised per-minute price | [5. Cost](#5-cost-headline-price-versus-the-invoice) |
| Callers hang up or ask for a person straight away | [6. Caller trust](#6-caller-trust-and-conversation-design) |
| Dead air during lookups, or it says it did something it didn't | [7. Tool calls](#7-tool-calls-in-the-middle-of-a-conversation) |
| Works in testing, fails at volume or after an upgrade | [8. Reliability](#8-reliability-at-scale) |
| Wrong phone numbers, emails, names or addresses | [9. Getting the data right](#9-getting-the-data-right) |
| You can't tell what actually happened on a call | [10. Observability](#10-seeing-what-actually-happened-on-a-call) |
| It stops for coughs and "mm-hm", or won't stop when interrupted | [11. Interruptions](#11-interruptions-and-barge-in) |
| Speech-to-speech model or separate speech-to-text and text-to-speech? | [12. Architecture](#12-speech-to-speech-or-a-cascade) |
| It hears itself on speakerphone, or the TV in the room | [13. Echo and noise](#13-echo-and-background-noise) |
| It switches language, or struggles with accents | [14. Languages and accents](#14-languages-accents-and-switching) |
| Confident wrong answers, leaked prompts, abuse | [15. Guardrails and security](#15-hallucination-guardrails-and-security) |
| Tests pass but real calls fail | [16. Testing](#16-testing-that-predicts-real-calls) |
| A tutorial or SDK stopped working | [17. Fast-moving APIs](#17-fast-moving-apis-and-silent-model-changes) |
| Transfers to a person drop or ring out | [18. Handoffs](#18-handing-the-call-to-a-person) |
| Outbound calls hit voicemail or show "Spam Likely" | [19. Outbound calling](#19-outbound-calling-voicemail-screening-and-spam-labels) |
| Consent, AI disclosure, recording rules | [20. Compliance](#20-compliance-and-consent) |

---

## 1. Latency callers hear is not what the dashboard shows

**What happens.** A dashboard shows about 1.3 seconds and the recording sounds
like 3. In one vendor-forum thread, staff broke a 5.2-second turn into about
1 second of model and speech time and about 4 seconds of waiting for the caller
to finish, which the dashboard left out.

**Why.** A reply crosses at least ten network hops. The wait for the end of
the caller's turn is often the biggest part and is often missing from platform
numbers. Distance adds more, and the phone leg can roughly double what you
measured in the browser.

**What works.** Run your agent server and its speech and model services in the
same region as your phone provider's nearest data centre. Keep speech
connections warm. Replace a
fixed silence timer with an end-of-turn model. Say something short before slow
steps. Measure from recorded audio on both sides of the call, not from
platform timestamps. One independent test of real phone calls measured medians
of 1.3 to 1.7 seconds across five managed platforms, even with the end-of-turn
wait cut to 0.1 seconds on three of them, with platform self-reports about half a
second lower than what callers heard.

**Skills:** [voice-latency-audit](../skills/foundations/voice-latency-audit/SKILL.md) ·
[voice-stack-selection](../skills/foundations/voice-stack-selection/SKILL.md)
**Sources:** [OpenBenchmarks](https://openbenchmarks.com/voice-agent-latency) ·
[Twilio latency guide](https://www.twilio.com/en-us/blog/developers/best-practices/guide-core-latency-ai-voice-agents) ·
[Retell forum breakdown](https://community.retellai.com/t/massive-jitter-and-llm-streaming-failing-more-often-increased-perceived-latency/3402) ·
[a sub-500 ms build write-up](https://www.ntik.me/posts/voice-agent)

## 2. Turn-taking: knowing when the caller has finished

**What happens.** It goes wrong both ways, and "it answers the moment I pause"
is now the louder complaint. Builders describe the trap: a 1.2-second silence
threshold feels broken, and 500 ms cuts people off mid-thought.

**Why.** A silence timer can't tell a thinking pause from a finished sentence,
and common defaults sit around 300 to 500 ms. Builders often stack several turn
detectors (voice activity, an end-of-turn model and the speech-to-text
service's own endpointing) that disagree with each other.

**What works.** Use a semantic end-of-turn model rather than silence alone.
Give one component ownership of the turn and set any watchdog longer than its
timeout. Choose the wait per use case: one interview product raised its
threshold from 0.4 to 1.5 seconds and reported 26% fewer interruptions. For
slow, thoughtful speakers, consider push-to-talk.

**Skills:** [voice-turn-taking](../skills/foundations/voice-turn-taking/SKILL.md) ·
[voice-conversation-design](../skills/foundations/voice-conversation-design/SKILL.md)
**Sources:** [HN: faster is worse without better turn-taking](https://news.ycombinator.com/item?id=48013919) ·
[Pipecat: competing turn controllers](https://github.com/pipecat-ai/pipecat/issues/4279) ·
[production eval playbook](https://velagao.substack.com/p/the-voice-ai-playbook-i-wish-i-had)

## 3. Phone plumbing

**What happens.** Getting a real number connected is the most common first
blocker. Then the phone behaves differently from the browser demo: calls that
never connect, a greeting followed by silence, choppy audio, transfers that
ignore timeouts.

**Why.** Phone audio is narrowband (8 kHz) and adds delay. Hidden sample-rate
conversions break components built for 16 kHz: in one Pipecat issue a turn
model's accuracy fell from 98% to 60% on 8 kHz audio. SIP behaviour differs by
carrier and region.

**What works.** Set audio formats explicitly from end to end, and test with real
phone calls early. Host near your callers. When SIP fails, capture a packet
trace first. Use the documented session-lifetime settings so a network blip
doesn't end the call.

**Skills:** [voice-media-debugging](../skills/foundations/voice-media-debugging/SKILL.md) ·
[voice-call-reliability](../skills/foundations/voice-call-reliability/SKILL.md)
**Sources:** [Pipecat: 8 kHz breaks turn detection](https://github.com/pipecat-ai/pipecat/issues/3844) ·
[LiveKit: phone latency versus web](https://github.com/livekit/agents/issues/3685) ·
[OpenAI forum: Realtime over SIP](https://community.openai.com/t/realtime-api-unreliable-over-sip/1366350)

## 4. Choosing a platform, and avoiding lock-in

**What happens.** "Vapi, Retell, LiveKit, Pipecat or ElevenLabs for 3,000
minutes a month?" is the most common beginner question. Advice splits by
community: small-business builders lean to managed platforms, developers to
frameworks. Lock-in shows up late: features that only work on a vendor's cloud,
and models retired before their replacements can do the same job.

**What works.** Prototype on a managed platform if you need a phone line live in
days. Keep stages swappable if you need tools, audit trails or your own voice.
Pin model versions and read deprecation notices. Check which features are
cloud-only before you commit. Compare platforms on your own recorded calls, not
their latency pages.

**Skills:** [voice-stack-selection](../skills/foundations/voice-stack-selection/SKILL.md) ·
[provider landscape](landscape.md) · [where to start](getting-started.md#pick-a-starting-path)
**Sources:** [HN: frameworks versus platforms](https://news.ycombinator.com/item?id=46380399) ·
[Google forum: model retired before its replacement](https://discuss.ai.google.dev/t/gemini-2-5-flash-native-audio-preview-09-2025-text-text-only-not-working/107467) ·
[LiveKit: cloud-only noise cancellation](https://github.com/livekit/livekit/issues/4029)

## 5. Cost: headline price versus the invoice

**What happens.** The advertised per-minute price covers one layer. Speech
recognition, the model, the voice, the phone carrier, concurrency and add-ons
are billed separately, sometimes with 60-second minimums or burst pricing.
Builders report dashboards at double the expected rate and calls billed long
after they ended.

**What works.** Add up last month's invoices from every provider and divide by
billed minutes. Read the per-call cost breakdown. Make sure your code actually
ends calls and closes sockets. Cache repeated phrases such as greetings. One
independent test that read each platform's own billing measured about $0.05 to
$0.14 per minute across five managed platforms, for short test calls.

**Skill:** [voice-cost-estimation](../skills/foundations/voice-cost-estimation/SKILL.md)
**Sources:** [OpenBenchmarks cost per minute](https://openbenchmarks.com/voice-agent-latency) ·
[Pipecat: wrong model billed](https://github.com/pipecat-ai/pipecat/issues/2801)

## 6. Caller trust and conversation design

**What happens.** Callers hang up on bots that only repeat the website, loop, or
ignore "no thanks". A post about building an AI receptionist drew over 300
comments on Hacker News, with people saying they hang up on AI receptionists, and asking how its
hang-up rate compared with plain voicemail.

**Why.** The agent doesn't solve the caller's actual problem, botches a name or
number, or has no hard limits between the model and the order system.

**What works.** Make escalation to a person and callback capture core features.
Let the model fill structured fields and check them with ordinary code against
the real menu, calendar or price list. Read back names, numbers and orders.
Start narrow. The best-measured success is scripted: in a field experiment with
70,000 job applicants, AI voice interviews led to more job offers, and most
applicants chose the AI when offered.

**Skills:** [voice-conversation-design](../skills/foundations/voice-conversation-design/SKILL.md) ·
[what to build](what-to-build.md)
**Sources:** [HN: AI receptionist for a car shop](https://news.ycombinator.com/item?id=47487536) ·
[HN: drive-thru loops and hard limits](https://news.ycombinator.com/item?id=45162220) ·
[Jabarian and Henkel field experiment](https://arxiv.org/abs/2607.28222)

## 7. Tool calls in the middle of a conversation

**What happens.** Silence while a slow API runs. An agent that says "connecting
you" and never transfers. A booking tool fired five times in one turn, leaving
a clinic with duplicate appointments. Speech-to-speech models that skip tools
or read field names aloud.

**What works.** Say something before slow steps, run slow tools in the
background and add a watchdog. Put routing and other irreversible decisions in
code: one builder's transfer success went from 58% to 92% after doing this.
Make side-effecting endpoints idempotent so a repeat does nothing. Use fewer,
simpler tools and return small results. Test tool success on your own traffic
before switching models.

**Skills:** [voice-conversation-design](../skills/foundations/voice-conversation-design/SKILL.md) ·
[voice-call-reliability](../skills/foundations/voice-call-reliability/SKILL.md)
**Sources:** [the receptionist that couldn't transfer](https://www.ashank.tech/blog/ai-receptionist-that-couldnt-transfer) ·
[Amadeus: demo to production](https://amadeus.com/en/engineering-blog/articles/from-demo-to-production-3-key-lessons-developing-voice-to-voice-ai-agent) ·
[Retell forum: five bookings in one turn](https://community.retellai.com/t/book-appointment-tool-calls-fired-in-a-single-llm-turn-after-streaming-timeout-resulted-in-multiple-appointments-booked-for-one-requested-slot/3301)

## 8. Reliability at scale

**What happens.** Rare per call, expensive in aggregate. After a minor
framework upgrade, one team saw about 1% of calls die. A caller hanging up froze a pipeline. A
dropped speech connection went silent until a timeout. Vendor outages with no
status signal. A cheap setup that fell over at a few hundred concurrent calls.

**What works.** Pin versions and roll upgrades out to a small share of calls
first. Cancel the pipeline when the caller disconnects. Use always-on hosting
for agent workers, not scale-to-zero. Add monitoring, alerts and a fallback
provider before real customers depend on it.

**Skill:** [voice-call-reliability](../skills/foundations/voice-call-reliability/SKILL.md)
**Sources:** [LiveKit: 1% of calls after an upgrade](https://github.com/livekit/agents/issues/3637) ·
[LiveKit: restarts on Cloud Run](https://github.com/livekit/agents/issues/1692)

## 9. Getting the data right

**What happens.** The agent sounds fine and writes the wrong thing down: phone
numbers, emails, street addresses, and negations ("never took it" becomes "took
it"). A mumbled number gets replaced by one that appears in the prompt.

**What works.** Read back names, numbers and orders every time. Ask for fewer
fields. Check values against real data with code (calendar, customer list,
address lookup). Offer the keypad for long digit strings. Keep transcripts
linked to the audio so a person can check before anything is filed.

**Skills:** [voice-data-capture](../skills/foundations/voice-data-capture/SKILL.md) · [voice-speech-pipeline](../skills/foundations/voice-speech-pipeline/SKILL.md)
**Sources:** [HN: transcript errors treated as fact](https://news.ycombinator.com/item?id=49294441) ·
[Pipecat: number transcription after a default change](https://github.com/pipecat-ai/pipecat/issues/3913)

## 10. Seeing what actually happened on a call

**What happens.** Dashboards stay green while callers hear stutters. Latency
panels disagree with recordings. Merged recordings can be misaligned.

**What works.** Record both sides on one clock and log raw turn events and tool
timings. Use the framework's own tracing (OpenTelemetry in LiveKit Agents and
Pipecat). Listen to real calls before trusting summaries or scores, and turn
every production failure into a test case.

**Skills:** [voice-latency-audit](../skills/foundations/voice-latency-audit/SKILL.md) ·
[voice-agent-evaluation](../skills/foundations/voice-agent-evaluation/SKILL.md)
**Sources:** [LiveKit: tracing request (71 reactions)](https://github.com/livekit/agents/issues/2260) ·
[an ex-vendor team's 14 production failures](https://shav.dev/blog/voice-ai-lessons)

## 11. Interruptions and barge-in

**What happens.** The agent stops for a cough, an echo or "mm-hm", or talks
straight over a caller who is trying to interrupt.

**Why.** Voice activity alone can't tell a real interruption from a backchannel,
background voices or the agent's own echo. Several thresholds interact, and
state can be left half-finished after a cut-off.

**What works.** Trigger barge-in from the transcript rather than raw voice
activity. Require a minimum number of words or duration before stopping. Make
transactions safe to interrupt so a booking doesn't fire after the caller
changed their mind.

**Skills:** [voice-turn-taking](../skills/foundations/voice-turn-taking/SKILL.md) ·
[voice-audio-frontends](../skills/foundations/voice-audio-frontends/SKILL.md)
**Sources:** [OpenAI forum: Realtime turn-taking](https://community.openai.com/t/issues-with-realtime-turn-taking/1369161) ·
[LiveKit: interruption threshold bypassed](https://github.com/livekit/agents/issues/3515) ·
[Pipecat Flows: orphaned function calls](https://github.com/pipecat-ai/pipecat-flows/issues/246)

## 12. Speech-to-speech or a cascade

**What happens.** Advice conflicts and is mostly opinion. Speech-to-speech
models sound more natural; builders report weaker tool use, language drift and
fast version churn. Cascades (speech-to-text, model, text-to-speech) are easier
to control and debug.

**What works.** Many teams use speech-to-speech for web and app agents and keep
phone lines and tool-heavy work on a cascade. Some transcribe separately with a
stronger model. Whichever you pick, pin the model version and test tool success
on your own calls. An independent leaderboard measures speech-to-speech models
through their APIs, though not over phone lines.

**Skill:** [voice-stack-selection](../skills/foundations/voice-stack-selection/SKILL.md)
**Sources:** [HN: pipeline versus full duplex](https://news.ycombinator.com/item?id=47258801) ·
[Artificial Analysis speech-to-speech](https://artificialanalysis.ai/speech-to-speech)

## 13. Echo and background noise

**What happens.** On speakerphone the agent hears itself and interrupts itself.
A greeting is transcribed as the caller speaking. Background noise makes it chat
to itself.

**Why.** Echo cancellation happens in the device, browser or transport, not in
your agent code. Raw WebSocket audio has none. Browsers differ: in one Pipecat
thread a commenter's agent heard its own audio in Firefox but worked in Edge, and
a maintainer pointed to Chrome and Safari for their echo cancellation.

**What works.** Use WebRTC or an SDK that applies echo cancellation. Add a
denoiser before voice detection. Mute or gate the microphone while the agent
speaks if you can live with weaker barge-in. Check whether a noise filter only
works on a vendor's cloud before you plan to self-host.

**Skill:** [voice-audio-frontends](../skills/foundations/voice-audio-frontends/SKILL.md)
**Sources:** [LiveKit: iPhone speaker echo](https://github.com/livekit/agents/issues/3758) ·
[Pipecat: greeting heard as the caller](https://github.com/pipecat-ai/pipecat/issues/4383) ·
[HN: a practitioner at 6,000 calls a day](https://news.ycombinator.com/item?id=48051951)

## 14. Languages, accents and switching

**What happens.** After a model upgrade, Spanish and German agents drift into
English. A caller's name makes the agent switch language. Mid-sentence switches
between languages break detection.

**What works.** Force the starting language and make switching explicit. Keep
all injected context in the target language. Filter transcripts in an
unexpected script before they reach the model. Pin model versions and test each
language with your own names, terms and accents.

**Skill:** [voice-speech-pipeline](../skills/foundations/voice-speech-pipeline/SKILL.md)
**Sources:** [OpenAI forum: language drift](https://community.openai.com/t/gpt-realtime-2-1-exhibits-language-drift/1386953) ·
[OpenAI forum: names flip the language](https://community.openai.com/t/realtime-api-language-switching/1366289) ·
[LiveKit: language switching pattern](https://github.com/livekit/agents/issues/1335)

## 15. Hallucination, guardrails and security

**What happens.** A confident wrong price or an invented appointment slot ends
the call. An agent read its system prompt aloud at a transfer. Public demos run
up bills within hours.

**What works.** Keep anything with consequences in ordinary code: the model
proposes, code validates against real data and enforces hard limits. Use fixed
text for announcements such as transfers. Keep API keys on a server and put
spend caps on public demos. Never let a transcript of unverified audio trigger a
privileged action.

**Skill:** [voice-agent-security](../skills/foundations/voice-agent-security/SKILL.md)
**Sources:** [Retell forum: system prompt spoken aloud](https://community.retellai.com/t/agent-spoke-its-system-prompt-aloud-to-the-caller-at-a-transfer-call-node-gpt-4-1-conversation-flow/3478) ·
[HN: adversarial audio against transcribers](https://news.ycombinator.com/item?id=48178378)

## 16. Testing that predicts real calls

**What happens.** Simulators and scripted tests pass; real calls fail. One
builder's ordering agent went from passing to 3 of 14 scenarios over 21 days
with no code change. A speech-to-text update changed accuracy overnight.

**What works.** Build your test set from production failures and keep adding to
it. Replay saved real calls against every prompt, model or vendor change. Check
tool calls exactly and use a model grader only for the conversation. Pin
versions so a silent alias change can't move your pass rate. Most public
material on testing comes from companies that sell testing, so read it with
that in mind.

**Skill:** [voice-agent-evaluation](../skills/foundations/voice-agent-evaluation/SKILL.md)
**Sources:** [fixing a voice agent, 3/14 to 13/13](https://jankoritak.com/blog/fixing-a-voice-agent-using-karpathy-s-autoresearch-blueprint) ·
[six months of production voice AI](https://dev.to/autor_tech/6-months-of-running-a-production-voice-ai-what-changed-what-broke-what-wed-rebuild-5621)

## 17. Fast-moving APIs and silent model changes

**What happens.** An SDK upgrade leaves the agent silent. A model is retired, or
an alias quietly points at a new version. Tutorials use names that no longer
exist.

**What works.** Pin SDK versions and dated model IDs. Put new versions through
saved real calls before switching. Read the vendor's deprecation page when a
tutorial's code won't run, and check a tutorial's date before copying it. The
skills here record when their sources were last checked.

**Sources:** [Deepgram SDK: overnight breakage](https://github.com/deepgram/deepgram-python-sdk/issues/668) ·
[Pipecat: resampler regression](https://github.com/pipecat-ai/pipecat/issues/1054)

## 18. Handing the call to a person

**What happens.** Transfers drop context, time out or ring nowhere. A carrier's
"press any key" message gets transcribed as the caller. The caller is stranded.

**What works.** Decide routing in code. Prefer a warm transfer that keeps the
caller until a person accepts; use a blind (cold) transfer only when your
platform can't do that. Pass structured context, not a
transcript dump, to whoever picks up. Offer a callback as the fallback. Test
transfers against real carriers, including call screening and phone menus.

**Skills:** [voice-call-reliability](../skills/foundations/voice-call-reliability/SKILL.md) ·
[voice-conversation-design](../skills/foundations/voice-conversation-design/SKILL.md)
**Sources:** [LiveKit: transfer timeout and SIP REFER](https://github.com/livekit/agents/issues/3187) ·
[Retell forum: silence after a forwarded call](https://community.retellai.com/t/agent-doesnt-speak-after-pressing-digit-until-customer-speaks-first/2087)

## 19. Outbound calling: voicemail, screening and spam labels

**What happens.** In one deployment about 30% of answered outbound calls were
voicemail or call-screening bots. Answering-machine detection that starts after
the call connects adds seconds of delay. Numbers get labelled "Spam Likely".

**What works.** Start detection before the call connects and hold the first
line until it decides. Use dedicated, verified numbers and keep volume per
number modest. Consent and calling-hour rules apply to AI outbound calls: see
the next item.

**Skills:** [voice-phone-compliance](../skills/foundations/voice-phone-compliance/SKILL.md)
**Sources:** [LiveKit: 30% voicemail or screening](https://github.com/livekit/agents/issues/3643) ·
[LiveKit: detection delay](https://github.com/livekit/agents/issues/5616)

## 20. Compliance and consent

**What happens.** Builders rarely raise it, and lawyers write about it
constantly. That mismatch is the risk.

**What the rules say** (orientation, not legal advice). In the US, the FCC ruled
in 2024 that AI-generated voices count as "artificial" voices, so calls using
them to mobile phones and homes generally need the person's prior consent, and
prior written consent for telemarketing. An artificial-voice message must name
the business at the start. Telemarketing must also honour do-not-call requests
and calling hours (8 a.m. to 9 p.m. the called person's time under federal rules;
some states are stricter, for example Florida ends at 8 p.m. and Texas starts at 9 a.m.). Courts and the FCC are still changing parts of the
consent rules, so check the current state before you dial.
Wiretap lawsuits over recording and AI transcription are moving fast, and courts are split on whether an AI vendor in the audio path counts as a third-party eavesdropper. In the
EU, the AI Act's rule that people must be told they're talking to an AI applies from
August 2, 2026, and the
Commission's guidelines use a spoken statement at the start of the call as the
example for voice. A HIPAA business associate agreement alone doesn't make a
voice agent compliant.

**Skill:** [voice-phone-compliance](../skills/foundations/voice-phone-compliance/SKILL.md)
**Sources:** [47 CFR 64.1200](https://www.law.cornell.edu/cfr/text/47/64.1200) ·
[Holland & Knight on AI class actions](https://www.hklaw.com/en/insights/publications/2026/05/recent-genai-class-actions-build-on-early-successes)

---

**How this page was made.** Researched on September 30, 2026. Problems are
ranked by judgement, weighing how many builder sources report them, how loudly,
and how first-hand the reports are. The sample is English-language and
search-ranked, and Reddit, Discord and Slack were largely out of reach, so small
agencies and no-code users are under-represented. Found something wrong or
missing? [Open an issue](https://github.com/RBStrayer/nl-voice-skills/issues/new/choose).
