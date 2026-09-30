---
name: voice-phone-compliance
description: Keep AI phone agents legal and their numbers deliverable. Use when building or reviewing inbound or outbound voice agents, outbound campaigns or dialers, call recording or transcripts, AI disclosure scripts, opt-out and do-not-call handling, HIPAA or PCI voice flows, or when calls show "Spam Likely" or get blocked. Covers TCPA and FCC rules for AI voices, consent, calling hours, state recording and AI-disclosure laws, STIR/SHAKEN and number reputation, and EU, UK and Canada basics. Not legal advice.
license: MIT
---

# Voice phone compliance

> **Not legal advice.** Rules differ by country, state, call type and industry, and some points here are unsettled. Confirm the plan with counsel for every place you call, call from, or record. This skill builds safeguards. It does not clear a launch.

An AI phone agent can break calling, recording, disclosure and privacy rules in its first minute. The price is private lawsuits (US federal law allows $500 per call, tripled if willful), regulator fines, and numbers labelled "Spam Likely" or blocked. Put the checks in code, in front of the dialer, so a bad list, a missing consent or a stop request cannot reach a call.

Read these with the skill and keep them together:

- [Legal requirements guide](references/legal-requirements-guide.md): US federal and state law, recording consent, EU, UK and Canada, with sources and open questions.
- [Numbers, data and call behavior guide](references/numbers-data-and-call-behavior-guide.md): caller ID reputation, HIPAA, PCI, scripts, consent logs, retention, tests.

Both were checked on September 30, 2026 UTC. Open the cited source again before you rely on a claim for a launch. If a rule you need is not in them, say "not checked" and list it for counsel. Do not guess.

For Twilio-specific steps (`<Pay>`, pausing recordings, SHAKEN/STIR, consent-record patterns) use the [Twilio compliance skill](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-compliance-traffic/SKILL.md). This skill is provider-neutral and cites primary sources. Where they differ, the cited source wins: the Twilio skill says AI voice agents typically count as autodialed, but the FCC treats an AI voice as an artificial voice, which is a separate test. This skill does not cover debt collection, political calls or fundraising. Tell the user to get counsel for those. The Twilio skill has a debt-collection section that this skill did not check.

## Ask before you build

No tools are required. Ask these in one message before you write dialer or recording code.

- **Direction.** Inbound, outbound, or both?
- **Audience.** Consumers or businesses? Which US states and countries are the callers and the people called in?
- **Purpose.** Sales or marketing, service or reminders, surveys, collections, politics, fundraising? (Stop on the last three.)
- **Consent.** How and where did each person agree to AI-voice calls? What text did they see? Where is it stored? Is any list bought?
- **Lists.** Who owns the internal do-not-call list and the National Registry subscription?
- **Recordings.** Stored? Where, who can read them, how long? May vendors train on them?
- **Sensitive data.** Health information, card numbers, voiceprints, children?
- **Numbers.** Owned or rented? How many, on which carrier? Registered with analytics vendors? Calls per number per day?
- **Vendors in the audio path.** Carrier, speech-to-text, LLM, text-to-speech, recorder, logging. Which have signed agreements (BAA, data processing)?
- **Humans.** Who takes a transfer, and when are they staffed?
- **Live or test?** Do not dial real people, record, or change carrier or registry settings without an explicit go-ahead.

## Classify each call flow

| Situation | Build rule | Read |
| --- | --- | --- |
| Outbound AI call, sales or marketing, to consumers | Signed written consent that names your company and AI or automated voice. National and internal do-not-call scrub. Recipient-local 8 a.m. to 9 p.m. (8 p.m. in Florida, Oklahoma and Maryland). AI, company name and a stop option in the first seconds. First word within 2 seconds of "hello" | [Federal law](references/legal-requirements-guide.md#us-federal-law) |
| Outbound AI call, not sales (reminder, service) | Prior express consent for mobile numbers. Landline exemptions are narrow. Same identification and stop handling | [Consent](references/legal-requirements-guide.md#consent-which-kind-do-you-need) |
| Outbound to business numbers | The registry does not cover them, but the consent rule still applies to mobile numbers. Treat as consumer calls unless counsel says otherwise | [Consent](references/legal-requirements-guide.md#consent-which-kind-do-you-need) |
| Inbound calls to you | The federal calling rules cover calls you place. Disclose AI, handle recording consent and data rules | [AI disclosure](references/legal-requirements-guide.md#ai-disclosure) |
| Recording or transcribing | Announce at the start of every call. All-party states need consent. Vendors need contracts that bar their own use of the audio | [Recording](references/legal-requirements-guide.md#recording-and-transcripts) |
| Health information | Signed BAA with every vendor that stores or processes it. No detail in greetings or voicemail | [HIPAA](references/numbers-data-and-call-behavior-guide.md#hipaa) |
| Card numbers | Digits never reach the LLM, transcript, logs or recording. Keypad capture by a payment provider, or pause and verify | [PCI](references/numbers-data-and-call-behavior-guide.md#pci-payment-cards) |
| People or numbers in the EU, UK or Canada | Separate rules. EU AI Act Article 50 applies from 2 August 2026. Ask counsel | [Outside the US](references/legal-requirements-guide.md#outside-the-us) |
| Numbers flagged or blocked | Check attestation, registration, pacing, consent and call length. Do not rotate or spoof | [Why numbers get flagged](references/numbers-data-and-call-behavior-guide.md#why-numbers-get-flagged) |

## Build the gates

1. **Before each dial, fail closed.** If a check fails or errors, do not dial and log why.
   - Consent record for this number, this seller and AI-voice calls, not revoked.
   - Not on the internal suppression list. National Registry copy no more than 31 days old (telemarketing).
   - Reassigned-number check for older consent.
   - Recipient-local time inside the strictest window that applies. Frequency caps (three per 24 hours per subject in the states that set them).
   - Caller ID is an owned or authorized number that connects back. No spoofing.
   - Campaign pacing and abandon-rate guard.
   - Write the attempt record first: attempt ID, consent ID, list versions, local time, script version.
2. **First seconds.** Say it is an AI. Name the business by its registered name. Offer "stop" by voice and keypad. State the purpose. Announce recording. Order and wording: [call behavior](references/numbers-data-and-call-behavior-guide.md#call-behavior).
3. **During the call.** Honor "stop" at once: write the suppression, then confirm, then end the call. Answer "are you a robot?" truthfully, every time. Transfer on request, and never say "connected" before a human accepts. Keep card and health data out of prompts, logs and transcripts.
4. **Voicemail.** It is an artificial-voice call, so consent rules apply. Keep it short and non-sensitive. Telemarketing voicemail needs a toll-free opt-out number. Do not guess on answering-machine detection; see the [call reliability skill](../voice-call-reliability/SKILL.md).
5. **Numbers.** Use numbers your provider can verify (attestation A). Register them with the analytics vendors where allowed. Ramp volume slowly. Log attestation, answer rate, call length and block codes per number. Fix causes instead of rotating numbers.
6. **Evidence.** Keep consent, suppression and call records in a separate store from audio. Keep do-not-call records 5 years and consent evidence at least 4. Fields: [evidence and retention](references/numbers-data-and-call-behavior-guide.md#evidence-and-retention).
7. **Test.** Dry-run mode, fail-closed tests, stop and truthfulness tests, with numbers the user owns: [test plan](references/numbers-data-and-call-behavior-guide.md#test-plan).

## Do not

- Do not claim to be human, or let a persona prompt hide the AI. "Are you a robot?" always gets a truthful yes.
- Do not keep pitching, arguing or calling after a stop request. Suppress across campaigns and vendors.
- Do not rotate, spoof or borrow caller IDs to escape labels. Fix the cause.
- Do not import lists without consent evidence that names your company and covers AI-voice calls. "Our partners" is not evidence.
- Do not let card numbers, security codes or health details reach LLM prompts, logs, traces, transcripts or voicemail.
- Do not send audio or transcripts to a vendor without the agreement the data needs.
- Do not treat a passing test, a vendor's "compliant" badge or this skill as legal clearance.
- Do not invent consent timestamps, list versions or citations. Mark unknowns.

## Deliver

- A call-flow table: direction, audience, purpose, places, rule set.
- The gates in code with fail-closed tests, the scripts, and the consent and suppression schema.
- A number plan: owned numbers, attestation, registration, pacing, monitoring.
- A vendor map with the agreement each one needs and whether it is signed.
- Open questions for counsel, each with its source link.
- What you verified versus assumed, and the review date of the guides.

## Unsettled (tell the user)

- The FCC's AI-disclosure rule is only proposed.
- The FCC adopted a new stop-request order on September 30, 2026. Its text and dates were not public when checked. Until then, honor stop requests broadly.
- Whether an LLM agent counts as a "live sales representative", a "prerecorded message" or an "automated calling system" under older rules.
- Whether AI vendors in the audio path can be treated as wiretappers in California (*Ambriz*, pleading stage).
- New state AI laws (Colorado, January 2027) and whether they reach private phone agents.
