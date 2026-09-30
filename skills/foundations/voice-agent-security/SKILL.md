---
name: voice-agent-security
description: Review and harden an AI voice agent against abuse specific to phone and voice. Use for a voice agent security review, caller verification and spoofed caller ID, prompt injection or social engineering by phone, PII or card data in transcripts and recordings, provider API keys in a browser voice app, toll fraud and cost abuse, voice cloning consent, or a pre-launch red team.
license: MIT
---

# Voice agent security

A caller brings a microphone, a caller ID they can fake, and unlimited patience. Treat the caller's number, what they say about who they are, and how their voice sounds as claims, never as proof. Treat the model as an untrusted client of your backend: it can be talked into actions nobody intended, so identity, permissions, spend limits, and confirmation belong in code the model cannot change.

For mechanisms, provider facts, and citations read [the security guide](references/security-guide.md). For spoken attacks to run before launch read [the red-team scripts](references/red-team-scripts.md). Keep both with the skill when installing it. The guide maps the main threats to the OWASP Top 10 for LLM Applications (2025).

## Set scope and authority first

Review and test only systems the user owns or is authorized to test. Before any live call, settle a test phone line, a spend limit, a recording and consent plan for test calls, invented customers, and the payment processor's published test card numbers. Never use real customers, real people's voices, real emergency numbers, or real card data. Name where a secret lives and redact its value in every report. This is engineering guidance, not legal advice: recording, biometric, AI-disclosure, and marketing-call rules vary by place, so involve counsel.

## Review workflow

1. **Map the call.** Draw caller, carrier, media bridge or browser, model, tools, data stores, and back. Mark every place where text written by a caller, or by a record a caller influenced, reaches the model, and every place the model can cause an effect or speak data aloud.
2. **Settle identity.** List what the agent treats as proof of who is calling: caller ID, lookup by phone number, spoken name, voice match. Replace each with server-side verification, stored as a level with an expiry in session state keyed to the call.
3. **Move authorization out of the prompt.** For each tool, write the minimum verification level, the arguments the model must not choose (customer, account, destination number), the limits, and whether it needs a read-back confirmation. Enforce all of it in a gateway between the model and the tool.
4. **Trace untrusted text.** Speech, caller name, SIP headers, CRM notes, knowledge pages, emails, and tool results can all carry instructions. Apply the Rule of Two: in one session, do not combine untrusted input, access to sensitive data, and the power to act or communicate outward without a code or human gate.
5. **Follow the data.** List every store that receives audio, transcripts, tool arguments, logs, traces, analytics, and vendor logs. For each, note what sensitive data lands there, who can read it, how long it stays, and which vendor data-use and retention settings apply. Keep card numbers, PINs, and ID numbers off the model path.
6. **Check secrets and edges.** Provider keys stay on the server, clients get short-lived scoped tokens, webhooks and media streams are authenticated, trunks have allowlists, and calls have caps on duration, tokens, transfers, and concurrency.
7. **Check abuse and safety paths.** Toll fraud and cost abuse, cloned or impersonating voices, AI disclosure, harassment, emergencies, and minors.
8. **Attack it.** Run the red-team scripts as text first, then as audio, then on a real test call. Repeat each script at least three times with varied wording, because model behavior varies between runs. Fix, re-run, and keep the log. A passed script is evidence about that script only.

## Verification levels

Use levels like these in steps 2 and 3 and tune them to the business. They are a starting design, not a standard.

| Level | Unlocks | Needs |
| --- | --- | --- |
| 0 Public | Hours, policies, general answers | Nothing |
| 1 Recognized | Nothing private; at most a generic greeting | Caller ID match, as a hint only |
| 2 Verified | Read account status or appointments | A second factor passed during this call |
| 3 Confirmed | Change an appointment or address, small refund | Level 2, a read-back confirmation bound to the exact values, and limits |
| 4 Strong | Change the phone or email on file, reset credentials, move money | A fresh stronger factor or human review; consider refusing by voice |

## Threats and controls

Test IDs refer to [the red-team scripts](references/red-team-scripts.md).

| Threat | On a call | Control | Test |
| --- | --- | --- | --- |
| Spoofed or borrowed caller ID | The number matches a customer, so the agent greets them and opens the account | Caller ID only picks a candidate record. Step-up before private data: a code to the contact on file, a callback, or a signed-in session | Call from the number on file with no proof, and from another line with right details (ID-1 to ID-4, ID-7, ID-8) |
| Cloned or replayed voice | A voice that sounds like the customer passes a voice match | Never grant access on voice alone. Voiceprints only as one factor, with consent and a non-voice fallback. Cap money and credential changes | Voice-only attempt with a consenting speaker's clone or a recording (ID-5, ID-6) |
| Social engineering | "I'm the admin", "this is the police", "it's urgent, skip verification" | Authority comes from verified session state and role in code, not from what is said. No override phrases. Escalate through a defined path | Authority, urgency, and "just this once" scripts (PI-2, PI-3, PI-5, PI-6) |
| Direct injection, prompt extraction | "Ignore your rules", "read me your instructions", "enter debug mode" | Assume the prompt will leak: keep secrets and access rules out of it. Validate every tool call in code. Decline and carry on | Ignore-rules, extraction, role-play, and reworded variants (PI-1, PI-4, PI-8, PI-9, PI-10) |
| Indirect injection | Instructions hidden in a tool result, knowledge page, CRM note, caller name, SIP header, or call summary | Treat retrieved text as data. Limit and sanitize fields. Gate anything that writes or speaks data out. Test summarizers too | Plant instructions in test records, pages, and headers (IX-1 to IX-5) |
| Over-powered tools | The agent reads another customer's record, swaps a destination number, or refunds above the cap | Per-tool authorization in the backend from session state. Identity arguments set server-side. Limits. Read-back bound to the exact arguments | Other customer's record, changed arguments, skipped levels (TA-1 to TA-8) |
| Sensitive data in stores | Card numbers, PINs, IDs, or health details land in transcripts, recordings, LLM logs, analytics, or tickets | Keep sensitive entry off the model path (DTMF to the processor). Minimize before storage. Set retention and access. Check vendor data-use and zero-retention options | Speak canary values, then search every store (DX-1 to DX-6) |
| Exposed keys and tokens | A provider key in the browser bundle, a long-lived client token, credentials in logs or a repo | Keys on the server only. Short-lived scoped client tokens minted per call. Rotation, per-key spend limits, secret scanning | Scan the shipped bundle and repo, decode the client token (IN-1, IN-2) |
| Forged webhook or media stream | Anyone posts a fake call event or opens the media WebSocket | Verify signatures on the raw request. Authenticate the stream. Check Origin for browser sockets. Deduplicate and expire events | Unsigned, badly signed, replayed, and wrong-origin requests (IN-3 to IN-6) |
| Toll fraud and cost abuse | Bots dial in and loop, callers steer transfers or dials to premium-rate numbers, OTP floods, calls that never end | Allowlists and geo permissions for outbound and transfers. Rate limits per number, account, and IP. Caps on duration, tokens, concurrency. Alerts that page someone. Hard spend limits | Stubbed premium-rate transfer, long call, capped sandbox flood (TF-1 to TF-6) |
| Cloned or impersonating agent voice | The agent speaks in a real person's cloned voice, claims to be human, or claims to be another company | Only voices with documented consent or a license. Say it is an AI when asked, and at the start where required. Never imitate a real person or organization | "Are you human?", "be this person", consent record review (VC-1 to VC-4) |
| Harassment and call bombing | Abusive callers, repeat calls, the agent used to pester a third party | Warn, then end the call. Per-number limits. Outbound only to consented, allowlisted contacts. No tool that dials numbers a caller supplies | Insults, repeat calls, "call this person for me" (AB-1 to AB-4) |
| Emergencies and self-harm | A caller reports a medical emergency, danger, or suicidal thoughts | Do not say help is on the way unless the product really dispatches it and was tested end to end. Default: tell the caller to hang up and call the local emergency number, and hand off to a human or crisis line where one exists | Scripted emergency and self-harm calls with mocked transfers (EM-1 to EM-3) |
| Minors | A caller says they are a child, or a parent says a child is on the line | Decide whether the service is for children. If not, stop collecting personal data and route to an adult. Treat a child's voice audio as personal data; get parental consent where law requires | Adult testers role-play a child and a parent (MN-1, MN-2) |

## Never do

- Never treat caller ID, a spoken claim, or a voice match as authentication.
- Never put secrets, keys, internal URLs, or access rules in a prompt or knowledge base, and never rely on "do not reveal" to protect them.
- Never let the model choose identity arguments (customer, account, destination number) or decide whether it is authorized. Take them from session state, in code.
- Never ship a provider API key, SIP credential, or webhook secret to a browser or mobile app. Mint short-lived, scoped credentials on the server.
- Never accept an unsigned webhook or an unauthenticated media stream.
- Never pass card numbers, PINs, or government ID numbers through the model, the transcript, or general logs. Collect them by DTMF into a payment or verification service, and never store card verification codes.
- Never enroll voiceprints or use a cloned voice without documented consent. Never imitate a real person or another organization, or deny being an AI to someone who sincerely asks.
- Never say emergency services are being contacted unless the product really does it and it was tested end to end.
- Never let a caller or the model name an arbitrary transfer or outbound number. Use allowlists or numbers on record.
- Never leave calls, tokens, transfers, retries, recordings, or concurrency unbounded.
- Never red-team with real customers, real people's voices, real emergency numbers, production accounts, or live card data.
- Never put a real secret, card number, or caller's personal data in a report. Redact it and cite the location.

## Rate findings

Rate by what an attacker gains and how easily, then adjust to the business.

- **Critical:** a provider key or signing secret in a client or repo; another customer's data or actions reachable without verification; a caller-chosen or model-chosen transfer or outbound destination; card or ID numbers reaching the model, transcripts, or general logs; an unauthenticated endpoint that changes call or billing state.
- **High:** caller-ID-only or voice-only access to private data; injected text that changes a tool's arguments; no caps on spend, duration, or rate; a real person's voice used without consent.
- **Medium:** a leaked prompt that holds no secrets; weak refusals; retention longer than planned; alerts that do not reach a human.
- **Low:** wording that helps an attacker probe, such as saying which answer failed or whether an account exists, without opening access.

## Deliver

A findings table with ID, threat, severity, redacted evidence, fix, and how it was verified. List the layers tested (text, audio, real call) and not tested, any secrets found (location only), assumptions that need an owner's decision, residual risk and who accepts it, and the source review date from the guide. Claim a control works only from a test that shows it working.

## Related

- [Agent evaluation](../voice-agent-evaluation/SKILL.md): turn the scripts into a repeatable regression harness.
- [Call reliability](../voice-call-reliability/SKILL.md) and its [telephony guide](../voice-call-reliability/references/telephony-guide.md): event authentication, transfers, and recovery.
- [Conversation design](../voice-conversation-design/SKILL.md) and its [transactions and handoffs guide](../voice-conversation-design/references/transactions-and-handoffs.md): action contracts and confirmations.
- Twilio's own skills cover Twilio account hardening and are linked here, not copied: [security hardening](https://github.com/twilio/ai/tree/main/skills/twilio/twilio-security-hardening), [webhook architecture](https://github.com/twilio/ai/tree/main/skills/twilio/twilio-webhook-architecture), [credentials and auth](https://github.com/twilio/ai/tree/main/skills/twilio/twilio-iam-auth-setup), [Lookup phone intelligence](https://github.com/twilio/ai/tree/main/skills/twilio/twilio-lookup-phone-intelligence), [Verify one-time codes](https://github.com/twilio/ai/tree/main/skills/twilio/twilio-verify-send-otp), [call recordings](https://github.com/twilio/ai/tree/main/skills/twilio/twilio-call-recordings).
