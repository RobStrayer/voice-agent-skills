# Voice agent security: identity, injection, data, secrets, and abuse

[Handbook](https://github.com/RobStrayer/voice-agent-skills/blob/main/docs/handbook.md) / [Voice agent security skill](../SKILL.md)

Reviewed against current primary documentation on **September 30, 2026 UTC**. This is a review date, not a publication date. Provider, standards, and law statements are linked. Paragraphs marked *Inference* are engineering judgment, not documented provider behavior. Provider controls, retention terms, and laws change, so check the current page and your contract before relying on a setting or a number. This is engineering guidance, not legal advice. No live call, payment, or attack was run to write it.

## Contents

- Find the problem
- What is different on a phone call
- Caller ID is a claim
- Verify in steps, in the backend
- Do not let a voice be the password
- The prompt is not a control
- Authorize tools in the backend
- Untrusted text reaches the model
- Social engineering by voice
- Sensitive data in every store
- Keep cards, PINs, and IDs off the model path
- Redaction is best effort, so do not collect first
- Set retention, access, and deletion on purpose
- Keep keys off the client and mint short-lived credentials
- Authenticate events and media streams
- Cost abuse and toll fraud
- Voice cloning, impersonation, and disclosure
- Abuse, emergencies, and minors
- Test before launch

## Find the problem

| Problem or job | Start here | Evidence required |
| --- | --- | --- |
| The agent opens an account because the caller ID matches | [Caller ID is a claim](#caller-id-is-a-claim) | A call from the number on file, with no proof, gets no private data |
| Voice is used as a password | [Do not let a voice be the password](#do-not-let-a-voice-be-the-password) | A non-voice factor, consent records, and capped voice-only actions |
| A caller says "ignore your rules" or asks for the prompt | [The prompt is not a control](#the-prompt-is-not-a-control) | Refusals across repeated runs, and tools that still enforce the rules |
| The agent can reach another customer's data or act beyond its role | [Authorize tools in the backend](#authorize-tools-in-the-backend) | Denials logged by the gateway, not by the model |
| Retrieved text or a tool result steers the agent | [Untrusted text reaches the model](#untrusted-text-reaches-the-model) | Injected fixtures that change nothing |
| Pressure, urgency, or claimed authority works on the agent | [Social engineering by voice](#social-engineering-by-voice) | The same refusal on every run |
| Card numbers or IDs show up in transcripts, recordings, or logs | [Sensitive data in every store](#sensitive-data-in-every-store) | A search of every store for a known test value |
| A provider key is in a browser bundle or repo | [Keep keys off the client](#keep-keys-off-the-client-and-mint-short-lived-credentials) | Bundle and repo scan; token lifetime and scope |
| Fake webhook or media-stream traffic is accepted | [Authenticate events and media streams](#authenticate-events-and-media-streams) | Forged and replayed requests rejected |
| A bill spike, odd destinations, or calls that never end | [Cost abuse and toll fraud](#cost-abuse-and-toll-fraud) | Caps, alerts that fire, and a sandbox flood test |
| Cloned voices, "are you a person?", or impersonation | [Voice cloning, impersonation, and disclosure](#voice-cloning-impersonation-and-disclosure) | Consent records and a disclosure test |
| Abuse, an emergency, or a child on the line | [Abuse, emergencies, and minors](#abuse-emergencies-and-minors) | Scripted tests with mocked transfers |
| Run the pre-launch attack pass | [Test before launch](#test-before-launch) and [the scripts](red-team-scripts.md) | A results log with repeat runs |

## What is different on a phone call

- **Identity arrives as a number and a voice.** Both can be forged, and neither shows consent to act.
- **The attacker talks to the model directly** and can retry as often as they like, at your cost.
- **Every answer is spoken.** The voice is an output channel, so anything the model can see can be said aloud.
- **Audio becomes text in many places.** Recordings, transcripts, traces, vendor logs, and summaries each keep a copy.
- **Telephony has its own fraud economy.** Attackers can earn money per minute from calls to numbers they control.

*Inference:* this list is the skill's framing, assembled from the sources below, not a quotation from one of them. It maps onto the OWASP Top 10 for LLM Applications (2025) like this:

| OWASP entry | Where it shows up here |
| --- | --- |
| [LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | Spoken instructions, tool results, knowledge pages |
| [LLM02 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) | PII and card data in transcripts, logs, and speech |
| [LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) | Tools that act without backend authorization |
| [LLM07 System Prompt Leakage](https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/) | Secrets or access rules placed in the prompt |
| [LLM10 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) | Denial of wallet, endless calls, bot traffic |

## Caller ID is a claim

A caller ID is a number the network reports. It can be spoofed, and a household, an office, or a forwarding service can share it. ElevenLabs' guidance for voice agents says caller-ID authentication should require prior customer opt-in or be combined with another method, because callers may use other numbers and stored numbers may be reachable by unauthorized people ([ElevenLabs](https://elevenlabs.io/blog/designing-secure-caller-identity-authentication-flows-for-voice-agents)). Use the number to find a candidate record, to route, to rate limit, and to decide how much friction to add. Do not use it to unlock private data, to skip a factor, or to choose where a code is sent. *Inference:* even a first-name greeting tells whoever dialed that the number is on file, so skip it for sensitive services.

STIR/SHAKEN adds a signal, not proof of who is speaking. Twilio passes `StirVerstat` (and `X-Twilio-VerStat` on SIP) only when the call carries SHAKEN identity headers, and its page says support is deployed only in the United States and France. Attestation `A` means the originating provider knows the customer and their right to use the number, `B` means the customer is known but the right to use the number is not, and `C` covers everything else, including international calls ([Twilio](https://www.twilio.com/docs/voice/trusted-calling-with-shakenstir)). *Inference:* even an `A` describes what the carrier knows about the line, not who holds the phone now. Use attestation to add friction or to route, for example by requiring a second factor when the value is `C` or missing, never to skip verification.

Treat every other caller-supplied field the same way: caller name, SIP headers, and custom parameters. OpenAI's SIP guide says to treat `data.sip_headers` as untrusted caller metadata, not authorization ([OpenAI](https://developers.openai.com/api/docs/guides/voice-sip)).

## Verify in steps, in the backend

Decide what each action needs, then refuse the tool call until the session holds that level. The levels are in [the skill](../SKILL.md#verification-levels).

| Mechanism | Fits | Watch for |
| --- | --- | --- |
| One-time code to a contact on file | Levels 2 and 3 | Never send it to a number or address given during this call. A SIM change or number port can redirect a code (see the NIST note below), and *Inference:* so can call or message forwarding. Cap sends (see cost abuse). |
| Callback to the number on file | Levels 2 and 3 when a code is impractical | *Inference:* a spoofer never receives the return call, but forwarding and SIM changes can still redirect it. |
| Signed-in session handed to the call | Calls started from your app or site | Pass a signed session reference that the backend verifies, not a claim the model repeats. |
| Knowledge questions | A supplement at level 2, never the only factor above it | OWASP says security questions are no longer recognized as an acceptable authentication factor under NIST SP 800-63, and lists a date of birth as a bad question because it is easy to find ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Choosing_and_Using_Security_Questions_Cheat_Sheet.html)). |
| Voice match | Nothing on its own | See the next section. |

ElevenLabs describes five patterns, built as server-side tools and not as native features: a host-application session passed in as variables, knowledge-based questions checked by a backend tool, caller ID from a system variable, a required count of correct security answers, and a one-time code by SMS or email ([ElevenLabs](https://elevenlabs.io/blog/designing-secure-caller-identity-authentication-flows-for-voice-agents)). Twilio Verify offers SMS, voice, email, passkey, TOTP, and other channels through one API ([Twilio Verify](https://www.twilio.com/docs/verify/authentication-channels)). Rules for every mechanism:

1. **Run the check in a backend tool, not in the model's reasoning.** ElevenLabs says caller authentication should be deterministic and tool-based rather than left to the model's inference, and describes a tool that returns success or failure and gates the route to a sub-agent that can see account data.
2. **Let the tool result set the level.** Keep state on the server, keyed to the call ID: `level`, `verified_at`, `expires_at`, and which factors passed. Tools read it. The model cannot write it.
3. **Limit attempts** per call and per account, then lock out with a neutral message that does not say which answer was wrong or whether an account exists. *Inference.*
4. **Expire levels.** Re-verify before a level 3 or 4 action when the earlier check is old or the subject changed. *Inference.*
5. **Use a fresh factor for level 4.** OWASP's transaction authorization guidance says each transaction should use unique authorization credentials and that authentication and authorization should not be the same action ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html)).
6. **Change a contact on file only with the current contact.** The same OWASP guidance says a change of authorization token should be authorized with the current one, and its example is a phone number for SMS codes: the authorization code goes to the current number. NIST likewise treats setting or changing a pre-registered telephone number as binding a new authenticator ([NIST](https://pages.nist.gov/800-63-4/sp800-63b.html)). Never authorize the change with a code sent to the new number.
7. **Log each decision** with the level asked, the level held, and the outcome, never the answers themselves.

NIST's 2025 digital identity guidelines (SP 800-63B-4), written for U.S. federal systems, classify out-of-band authentication over the telephone network as a restricted authenticator. They require verifiers to keep alternative authenticator types available and say verifiers should consider risk indicators such as device swap, SIM change, and number porting before sending a code that way. *Inference:* the reasoning applies to any service. Twilio Lookup can return line type (mobile, landline, fixed or non-fixed VoIP, toll-free) as a paid package ([Lookup](https://www.twilio.com/docs/lookup/quickstart)), and a SIM swap package whose page describes limited access ([SIM swap](https://www.twilio.com/docs/lookup/lookup-sim-swap)). Check availability before designing around either.

## Do not let a voice be the password

In a November 2024 BBC test, the reporter had their own voice cloned from a radio interview and played the clone through a speaker to the phone lines of two UK banks that use voice ID. Both accepted it. The call came from the reporter's registered number, and Santander's line said it recognized that number before it asked for the voice check. The reporter noted that a thief would need their unlocked phone to repeat the trick. *Inference:* a number can also be spoofed, so this design stacks two signals that can both be forged. Santander told the BBC it had seen no fraud from voice ID and called it one element of several checks. Halifax called it optional and pointed to layered security. Both said it was stronger than knowledge-based checks ([BBC](https://www.bbc.com/news/articles/c1lg3ded6j9o)). OpenAI, in March 2024, encouraged phasing out voice-based authentication for bank accounts and other sensitive information ([OpenAI](https://openai.com/index/navigating-the-challenges-and-opportunities-of-synthetic-voices/)). NIST SP 800-63B-4 says biometric comparison based on voice shall not be used, and that biometric characteristics are not secrets and can often be obtained online without consent ([NIST](https://pages.nist.gov/800-63-4/sp800-63b.html)). Its scope is U.S. federal digital identity, but the threat is general.

Voiceprints are also regulated data. GDPR Article 9 makes processing biometric data for unique identification a special category, prohibited unless an exception such as explicit consent applies ([GDPR Art. 9](https://gdpr-info.eu/art-9-gdpr/)). Illinois' Biometric Information Privacy Act treats a voiceprint as a biometric identifier and requires a public retention policy, written notice, and a written release before collection, with a private right of action ([BIPA](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=3004&ChapterID=57)). Ask counsel before enrolling anyone.

- **No voice-only access,** and do not lower other checks because a voice matched.
- **If a voiceprint program already exists,** enroll only with documented consent, combine it with another factor, cap what a voice-only session can do, keep a non-voice path, and keep match scores for review. *Inference:* assume an attacker can make a convincing clone from a short public clip.
- **Do not add voice enrollment to a new product by default.** It adds legal exposure and a data class the customer cannot change after a breach. *Inference.*

## The prompt is not a control

OWASP lists prompt injection as LLM01: direct injection through user input and indirect injection through external content, including multimodal content. Its mitigations include constraining model behavior, validating outputs, least privilege with credentials held by the application, human approval for high-risk actions, separating external content, and adversarial testing that treats the model as an untrusted user ([LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)). LLM07 says the system prompt should not be treated as a secret or as a security control, and that the real risk is delegating authorization or sensitive logic to it ([LLM07](https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/)). LLM06 names excessive functionality, permissions, and autonomy as root causes and recommends complete mediation: enforce authorization in downstream systems rather than relying on the model ([LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)).

Two framings help place the gates. Simon Willison's "lethal trifecta" is the combination of private data, exposure to untrusted content, and a way to communicate externally. He argues that guardrail products claiming to catch most attacks are not enough, because 95% is a failing grade in application security ([Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)). Meta's Agents Rule of Two says that until injection can be reliably detected and refused, an agent must satisfy no more than two of three properties in one session: [A] it processes untrustworthy input, [B] it can reach sensitive systems or private data, [C] it can change state or communicate externally. An agent that needs all three should not run autonomously and needs human approval or another reliable validation. Meta also says the rule is not sufficient alone and supplements least privilege ([Meta](https://ai.meta.com/blog/practical-ai-agent-security/)). Twilio's own guidance for LLM-backed APIs is to treat the LLM as an untrusted client behind a gatekeeper that enforces input validation, rate limiting, authentication and authorization, and least privilege. Its example passes identity in headers generated outside the LLM, so the phone number is looked up from your database and not chosen by the model ([Twilio](https://www.twilio.com/en-us/blog/rogue-ai-agents-secure-your-apis), October 2024).

*Inference:* a voice agent is always in state [A], because the caller is untrusted by definition. If it also reads customer data [B] and can transfer, text, email, refund, or book [C], it has all three, so the gates must be code. Speaking counts as [C]. Limit what sits in the model's context to what the caller may hear at their current level: fetch private data through a tool after verification, return only the fields needed, and do not preload a full customer record when the call connects. Use the prompt for task, tone, and short neutral refusal wording. A refusal instruction lowers how often an attack works. The gateway is what stops it.

## Authorize tools in the backend

Every tool call passes through a gateway that decides, whatever the model says. OWASP's agent guidance for high-impact actions says to separate decision from execution: the agent proposes, and a policy service or execution component independently validates scope, privilege, and approval state. It also says to bind approval to the exact action, to require step-up authentication for critical actions such as account recovery and payment initiation, and to fail closed when risk classification, approval validation, policy lookup, or audit logging fails ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)).

```python
# Conceptual. The model proposes; the backend decides.
def authorize(session, tool, args):
    policy = POLICY[tool.name]                     # static table, not prompt text
    if session.level < policy.min_level or session.expired():
        return deny("verification_required", needs=policy.min_level)
    args["customer_id"] = session.customer_id      # never taken from model output
    if policy.confirm and not session.confirmed(tool.name, digest(args)):
        return ask_confirmation(tool.name, read_back(args))
    if not policy.within_limits(args, session):    # caps, allowlists, rate
        return deny("limit")
    return allow(args)
```

- **Policy as data.** A static table keyed by tool: minimum level, argument limits, confirmation rule, allowed destinations. Unknown tools are denied.
- **Set identity arguments in the gateway.** Do not put `customer_id`, `account_id`, or a free-form destination number in the tool schema the model sees. When the model must choose among the caller's own records, let it pass an opaque index that the gateway resolves inside the verified customer's records. This follows OWASP's guidance on insecure direct object references: check access for each object, take the current user from session information and not from a parameter, and look objects up within the set the user may access ([OWASP IDOR](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)).
- **Confirm consequential actions the way a signature works: you see what you sign.** OWASP says the user must be able to identify and acknowledge a transaction's significant data, such as the target account and the amount, and lists invalidating earlier authorization when the transaction data changes as a defense against tampering ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html)). Its agent guidance adds that approval is bound to the exact action: tool name, target, and normalized parameters ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)). In a voice flow, read back the significant values (amount, target, date), take a yes from the caller's next turn, and bind it to a digest of the exact arguments, so any change voids it. *Inference:* take the yes from the input channel (a DTMF event or a transcript turn tagged as the caller's), not from model-written text or a tool result that claims the caller agreed. Meta's hypothetical travel assistant gets the same control: human confirmation of any action, such as making a reservation or paying a deposit ([Meta](https://ai.meta.com/blog/practical-ai-agent-security/)). *Inference:* a caller's yes limits damage from text injected by a page, note, or tool result. It does not stop the caller, so it is no substitute for the verification levels.
- **Separate read and write tools,** and scope credentials to the smallest surface: read-only database roles and no shared admin token. OWASP's example of a bad tool is one with wildcard access, such as a shell that runs any command; its good example limits paths and operations ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)).
- **Cap damage per call:** maximum amounts, counts per day, and tool calls per minute.
- **Isolate privileged work.** ElevenLabs recommends gating account-data work behind an authentication tool result in its workflow builder, so the sub-agent that can see account data is unreachable before verification ([ElevenLabs](https://elevenlabs.io/blog/designing-secure-caller-identity-authentication-flows-for-voice-agents)). *Inference:* in other stacks, attach the privileged tool set only after the gateway raises the level.
- **Keep per-call state out of the model's context.** LiveKit tools receive a `RunContext` that exposes the session and its `userdata` ([LiveKit](https://docs.livekit.io/agents/logic/tools/definition.md)). *Inference:* that is a natural home for the verification level, because the model does not see it unless you put it in the prompt.
- **Treat client-set overrides as caller input.** ElevenLabs lets you enable per-field overrides, including system prompt, tools, knowledge base, and voice, that the client supplies when a conversation starts ([ElevenLabs](https://elevenlabs.io/docs/eleven-agents/customization/personalization/overrides)). *Inference:* on a public agent, leave the prompt and tools overrides off, and pass personalization from your server.
- **One handler per action.** OpenAI's SIP guide says to give each action one handler so duplicate webhook deliveries or events seen on several connections do not run a tool twice ([OpenAI](https://developers.openai.com/api/docs/guides/voice-sip)). See the [telephony guide](../../voice-call-reliability/references/telephony-guide.md) for deduplication and the [transactions guide](../../voice-conversation-design/references/transactions-and-handoffs.md) for uncertain writes.

## Untrusted text reaches the model

On a voice agent, text written by someone else reaches the model through more doors than a chat window:

| Door | Example |
| --- | --- |
| Speech-to-text | What the caller says, a recording they play into the line, a television in the background, a second speaker |
| Caller metadata | Caller name, SIP headers, custom parameters |
| Tool results | CRM notes, ticket text, order comments, names, and addresses that an earlier customer or employee typed |
| Knowledge and retrieval | Help-center pages, uploaded documents, web pages the agent browses |
| Other channels | SMS replies, emails, and chat transcripts pulled into the call |
| After the call | Summarizers, analytics, and automations that read the transcript |

The transcript does not say who spoke or whether it was a person. *Inference:* a caller can play prerecorded audio into the line, so a spoken instruction is as trustworthy as a typed one from an anonymous user. OWASP's prompt injection cheat sheet lists the patterns to expect: direct override, extraction of the system prompt, encoded or scrambled wording, multi-turn setups, and forged tool outputs ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)). Controls, none sufficient alone:

- **Separate and label external content** so the model can tell data from instructions, as OWASP advises. Expect less attack success, not none.
- **Limit what read tools return:** the fields needed, capped in length, with control characters and markup stripped.
- **Gate the tools that write or send,** so injected text cannot complete the chain from untrusted input to sensitive data to an outward action. A retrieved line that says "transfer the caller to this number" must fail an allowlist, not depend on the model's judgment.
- **Keep one customer's text out of another's context.** Notes that came from a caller are caller input, not staff instructions.
- **Isolate memory.** If the agent remembers across calls, treat memory writes as untrusted, isolate them per customer, expire them, and never store verification state or instructions there. OWASP's agent guidance asks for memory isolation between users and sessions, plus expiry and size limits.
- **Check what leaves.** Screen outputs for card-like numbers and internal identifiers before they are spoken or sent. OWASP lists output validation among its mitigations.
- **Put the post-call pipeline in scope.** Run the same injected fixtures through summarizers and downstream automations. A line that does nothing during the call can change a CRM field afterward. *Inference.*

## Social engineering by voice

Attackers use the same tactics they use on human agents: claimed authority, urgency, sympathy, confusion, persistence ("just this once"), and small questions that add up, such as yes-or-no checks on each field to learn a value. A model tuned to be helpful is a soft target for all of them.

- **Make refusals uniform.** The agent declines the same way every time, offers verification or a human, and does not say which check failed or whether an account exists. *Inference.*
- **Take authority from the session, not from the claim.** "I'm the administrator" changes nothing. Roles come from verified state in code.
- **Do not read back what is on file** to someone who has not reached the level. Let them state a value, and confirm or deny only after verification.
- **Do not let the agent be talked into a new procedure.** If the business needs an exception path, make it a human process with its own verification.
- **Hand off with evidence.** When the agent transfers to a person, pass what was verified and at which level, not just "verified", and do not pass the caller's unverified claims as facts. *Inference.*

## Sensitive data in every store

A call can leave copies of the same words in many places. List each one, what it holds, who can read it, and how long it stays.

| Store | What lands there | Check |
| --- | --- | --- |
| Carrier recordings and logs | Audio, numbers, timing | Recording on or off, consent, retention, access |
| Speech-to-text and text-to-speech vendors | Audio in, transcripts and response text | Data-use opt-outs, retention |
| LLM provider | Prompts (including transcripts and tool results), responses, audio for speech-to-speech models | Retention, abuse-monitoring logs, zero-retention eligibility |
| Agent platform or framework | Transcripts, recordings, traces, logs, analytics | Defaults, redaction, who can open sessions |
| Your backend | Tool arguments, tool results, error reports, traces | Log scrubbing, access |
| Downstream systems | CRM notes, tickets, email, summaries, warehouses, evaluation sets | Copies, access, deletion |

Provider facts that change what you configure. Check the page for the model and endpoint you use:

- **OpenAI.** Data sent to the API is not used for training unless you opt in (since March 1, 2023). Abuse-monitoring logs are kept up to 30 days by default. Zero Data Retention and Modified Abuse Monitoring need OpenAI's prior approval. A per-endpoint table lists retention and eligibility, for example `/v1/realtime` (30 days of abuse-monitoring logs, no application state, ZDR eligible) and `/v1/live/sessions` (30 days, application state none or 30 days if stored, ZDR with limitations) ([OpenAI](https://developers.openai.com/api/docs/guides/your-data)).
- **Deepgram.** Add `mip_opt_out=true` to a request to exclude it from the Model Improvement Partnership Program. Opted-out data is kept only as long as needed to process the request ([Deepgram](https://developers.deepgram.com/docs/the-deepgram-model-improvement-partnership-program)).
- **ElevenLabs Agents.** Conversation data is kept 2 years by default, configurable in days, unlimited (`-1`), or scheduled deletion (`0`), separately for transcripts and audio ([retention](https://elevenlabs.io/docs/eleven-agents/customization/privacy/retention)). Zero Retention Mode stores no recordings and no transcripts or metadata containing PII after the call, and you get data through post-call webhooks ([ZRM](https://elevenlabs.io/docs/eleven-agents/customization/privacy/zrm)).
- **LiveKit Cloud.** Audio, transcripts, traces, and logs are collected by default (`record=True`), with a 30-day retention window on every plan, and you can turn each category off. LiveKit support can open a session's audio and transcripts when you share it. LiveKit describes models called through LiveKit Inference as zero data retention ([LiveKit](https://docs.livekit.io/testing/observability/insights)).
- **Twilio.** A recording can be paused through the API, with `skip` or `silence` behavior, and silence is the default ([Twilio recordings](https://www.twilio.com/docs/voice/api/recording)).

## Keep cards, PINs, and IDs off the model path

*Inference:* the safest card number is one the model never sees. Card digits go only to a payment provider that captures keypad tones itself, so speech-to-text, the model, transcripts and logs never receive them. Pausing a recording is not a substitute: it keeps digits out of the recording only, while spoken or keyed digits still reach speech-to-text, the model and vendor logs. Use pause-and-resume only as an extra layer on the recorder, and check weekly that recordings hold no card data.

- **Use DTMF and a payment service.** Twilio's `<Pay>` and pay connectors capture a card without your application handling it. In agent-assisted payment the agent cannot hear the tones and sees only the masked result of each entry ([payment resource](https://www.twilio.com/docs/voice/api/payment-resource), [pay connectors](https://www.twilio.com/docs/voice/twiml/pay/pay-connectors)). Turning on Twilio's PCI Mode redacts sensitive data from all of that account's logs and cannot be undone, so Twilio suggests considering a separate account if you do not want that everywhere ([tutorial](https://www.twilio.com/docs/voice/tutorials/how-to-capture-payment-during-a-voice-call-generic-pay-connector)).
- **Watch where collected digits go next.** LiveKit's `GetDtmfTask` collects keypad or spoken digits and is in beta for Python. Its documented example returns the digits to the model as a tool result ([GetDtmfTask](https://docs.livekit.io/agents/prebuilt/tasks/get-dtmf.md), [DTMF](https://docs.livekit.io/telephony/features/dtmf.md)). *Inference:* for card data, send digits from the server to the payment processor and give the model only a masked result or a pass or fail.
- **Keep card data out of free-text fields.** Twilio's ConversationRelay supports PCI workflows when configured with PCI-compliant speech providers, says not all providers are guaranteed to be, and says not to put card data in `welcomeGreeting`, `hints`, `<Parameter>` values, or `handoffData` ([ConversationRelay](https://www.twilio.com/docs/voice/twiml/connect/conversationrelay)).
- **Do not store card verification codes after authorization.** PCI DSS prohibits it ([PCI SSC FAQ](https://www.pcisecuritystandards.org/faqs/1574/)). The PCI Security Standards Council adds that collecting them before authorization is not prohibited and that encryption does not satisfy the rule ([PCI SSC blog](https://blog.pcisecuritystandards.org/faq-can-cvc-be-stored-for-card-on-file-or-recurring-transactions)). The November 2018 supplement on telephone payment data (version 3.0, which replaced the 2011 one written for PCI DSS 2.0) says the card verification code must be deleted from a recording once the transaction is processed if a tool cannot stop it being stored, and that pause-and-resume does not reduce PCI DSS applicability to the agent or other systems in the telephone environment (section 6.5.1) ([supplement](https://listings.pcisecuritystandards.org/documents/Protecting_Telephone_Based_Payment_Card_Data_v3-0_nov_2018.pdf)). It predates PCI DSS v4.0.1, so read it with the current standard and a qualified assessor.
- **Treat other identifiers the same way.** Government ID numbers, full account numbers, and health details: verify through a backend service and let the model see a pass or fail, or the last few digits at most. *Inference.*

## Redaction is best effort, so do not collect first

- LiveKit's PII redaction is off by default, runs on LiveKit Cloud after the session ends, is described as best effort, and detects PII in English-language transcripts only. Data your agent keeps itself, such as `session.history` or Egress recordings, still holds raw PII ([redaction](https://docs.livekit.io/testing/observability/pii-redaction)). Participant identity and room names appear in logs and traces and are not redacted, so keep phone numbers and names out of them ([tokens](https://docs.livekit.io/frontends/reference/tokens-grants/)).
- ElevenLabs' conversation history redaction is for select enterprise clients, runs after the conversation ends, and ElevenLabs says its detection rate is not 100%. Redacting keypad entries is a separate DTMF setting ([redaction](https://elevenlabs.io/docs/eleven-agents/customization/privacy/conversation-history-redaction)).
- Twilio's Conversation Intelligence (classic) limits PII redaction by language and is not PCI or HIPAA compliant ([limitations](https://www.twilio.com/docs/conversation-intelligence-classic/limitations)).

*Inference:* post-call redaction does not reach the model provider, other raw copies, or anything said during the call. Order of preference: do not collect, keep it off the model path, redact what remains, then restrict access and shorten retention.

## Set retention, access, and deletion on purpose

- Write down the retention you chose for each store and the vendor default it replaces (30 days, 2 years, until deleted).
- Give recordings and transcripts their own role. Most engineers who debug calls do not need audio of a customer's card or medical details.
- Plan deletion requests before the first one: which stores, in which order, and who confirms.
- Strip PII before copying transcripts into evaluation sets, prompts, or vendor support tickets.
- Children's voices: COPPA defines a child as under 13 and includes an audio file containing a child's voice in personal information ([16 CFR 312.2](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312/section-312.2)). See the minors section below.

## Keep keys off the client and mint short-lived credentials

- **Never ship a provider key to a browser or mobile app.** OpenAI's key-safety article says to route requests through your backend, not to deploy keys in client-side code, and not to commit them ([OpenAI](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)). Its Node SDK names the browser opt-in `dangerouslyAllowBrowser` for that reason ([openai-node](https://github.com/openai/openai-node)). ElevenLabs likewise says never to expose the API key client-side ([ElevenLabs](https://elevenlabs.io/docs/eleven-agents/customization/authentication)).
- **Set hard spend limits.** OpenAI says alerts alone do not stop traffic, and that hard enforcement is not instantaneous and can block legitimate requests, so combine limits with your own caps ([OpenAI](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)). Keep keys in environment variables or a secret manager and rotate them ([production practices](https://developers.openai.com/api/docs/guides/production-best-practices)).
- **OpenAI Realtime from a browser.** The server creates an ephemeral client secret and the frontend connects with it ([Realtime](https://developers.openai.com/api/docs/guides/realtime)). A secret can create multiple sessions until it expires, with expiry between 10 and 7,200 seconds and a default of 600 ([client secrets](https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create)). Most session properties can be changed mid-session with a `session.update` client event, and a session lasts at most 60 minutes ([conversations](https://developers.openai.com/api/docs/guides/realtime-conversations)). *Inference:* a stolen secret works until it expires and a browser can reconfigure its own session, so mint late, expire early, rate limit minting behind your own authentication, and keep authorization in backend tools, not in client-side settings. OpenAI also recommends a hashed, stable user identifier in the `OpenAI-Safety-Identifier` header, set on the server request that creates the secret, so enforcement can target one user and not your whole organization ([Realtime](https://developers.openai.com/api/docs/guides/realtime)).
- **LiveKit.** Access tokens are JWTs signed with your API secret, so create them on the server. Grants define what the holder may do, including room admin, recording, and SIP grants where `admin` manages trunks and dispatch rules and `call` permits `CreateSIPParticipant`. Give a browser only what it needs, never `admin` or `call`. Expiry applies to the initial connection, not reconnects. On LiveKit Cloud, removing a participant revokes their token with a one-minute buffer unless you pass `revoke_token_ts`. On self-hosted deployments removal does not invalidate the token, so use a short TTL ([tokens](https://docs.livekit.io/frontends/reference/tokens-grants/)).
- **ElevenLabs.** Signed URLs are recommended for client-side apps. A conversation must start within 15 minutes of the URL being issued, and the session can then last longer. ElevenLabs recommends a new signed URL per user session. An allowlist of up to 10 hostnames limits which origins can connect, and the docs say not to configure signed URLs and an allowlist together on one agent ([ElevenLabs](https://elevenlabs.io/docs/eleven-agents/customization/authentication)).
- **Public agents cost money.** *Inference:* require a login or a bot check before minting a token, rate limit minting per account and per IP, and cap session length on the server.

## Authenticate events and media streams

Anyone can send an HTTP request or open a WebSocket to a public URL. Each inbound event that changes state needs proof of origin.

| Channel | Mechanism | Notes |
| --- | --- | --- |
| Twilio webhooks | `X-Twilio-Signature`: HMAC-SHA1 over the URL and all parameters, keyed with your auth token | Twilio adds parameters without notice, so validate with everything received. Use Twilio's SDK validator, not your own, and serve HTTPS with a certificate that is not self-signed ([Twilio](https://www.twilio.com/docs/usage/webhooks/webhooks-security)). |
| Twilio Media Streams and ConversationRelay sockets | The same header on the WebSocket handshake, over `wss://` | Validate with your auth token and the request URL, and accept only connections with a valid signature ([Media Streams](https://www.twilio.com/docs/voice/media-streams), [onboarding](https://www.twilio.com/docs/voice/conversationrelay/onboarding)). |
| OpenAI SIP webhooks | Verify the webhook signature, then deduplicate | One handler per action ([OpenAI](https://developers.openai.com/api/docs/guides/voice-sip), [webhooks](https://developers.openai.com/api/docs/guides/webhooks)). |
| LiveKit webhooks | Signed JWT in the `Authorization` header, including a SHA-256 of the payload | Verify with the SDK's `WebhookReceiver` on the raw body ([LiveKit](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events/)). |
| ElevenLabs post-call webhooks | HMAC in the `ElevenLabs-Signature` header | Use the SDK's `constructEvent` or `construct_event` ([ElevenLabs](https://elevenlabs.io/docs/eleven-agents/workflows/post-call-webhooks)). |

OWASP's webhook guidance adds the general rules: verify on the raw body, compare signatures in constant time, return 401 without saying why, keep one secret per webhook in a secrets manager and out of logs, reject stale timestamps where the protocol has them, and deduplicate by event ID ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html)). A valid signature shows origin and integrity, not freshness or authority, so add state checks ([telephony guide](../../voice-call-reliability/references/telephony-guide.md)).

**Stream tokens.** A Twilio `<Stream>` URL does not support query strings. Custom values go in `<Parameter>` elements ([Twilio](https://www.twilio.com/docs/voice/twiml/stream)). *Inference:* mint a one-time, short-lived stream token in the code that returns your TwiML, pass it as a `<Parameter>`, and check it together with the signature on the socket's first message, so a leaked socket URL is useless on its own.

**Browser sockets.** OWASP's WebSocket guidance: use `wss`, validate `Origin` against an allowlist, guard against cross-site WebSocket hijacking when cookies authenticate, redact tokens that travel in query strings because they appear in access logs (passing the token in a message after connecting avoids that), authorize each message and not only the handshake, limit message size and rate, rotate tokens on long-lived connections, and close connections on logout ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html)).

**Trunks.** LiveKit inbound trunks accept `allowed_numbers`, `allowed_addresses` (which LiveKit support must enable for your project), and `auth_username` with `auth_password`. When `allowed_numbers` is empty, limit access with credentials or allowed addresses. Credentials work only if your SIP provider supports them, and LiveKit says Twilio Elastic SIP Trunking does not. A dispatch rule's `inbound_numbers` rejects calls from other numbers. Its `hide_phone_number` option uses a random participant identity and leaves the number out of attributes. *Inference:* that keeps the number out of the identity field, which LiveKit records in logs and traces ([SIP API](https://docs.livekit.io/reference/telephony/sip-api/), [inbound trunks](https://docs.livekit.io/telephony/accepting-calls/inbound-trunk/)). OpenAI's SIP guide says to keep the API key and SIP credentials on the server and to use TLS and SRTP ([OpenAI](https://developers.openai.com/api/docs/guides/voice-sip)).

## Cost abuse and toll fraud

Three bills can run away: telephony minutes and transfers, model and speech minutes, and verification messages. OWASP calls the cost-driving pattern Denial of Wallet, where an attacker exploits the cost-per-use model of a cloud AI service ([LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)).

**Toll fraud.** Twilio's glossary defines international revenue sharing fraud as exploiting an application to generate many calls to the fraudster's own premium-rate numbers, with the victim paying for each minute. The steps it lists: find an app or PBX that can place outbound calls, place short test calls to find gaps carriers do not block, buy a premium-rate number, and within 30 minutes start dozens of concurrent calls to it ([Twilio glossary](https://www.twilio.com/docs/glossary/what-is-toll-fraud)). Twilio's anti-fraud guide adds that calls are often answered by a recording or silence to look normal, charges are per minute and go to the owner of the calling number, and verification flows are a common target ([Twilio](https://www.twilio.com/docs/usage/anti-fraud-developer-guide)). Twilio's Verify guidance adds that no provider-side solution can guarantee 100% effectiveness against sophisticated attackers, so customer participation is essential ([Verify](https://www.twilio.com/docs/verify/preventing-toll-fraud)).

- **Account level.** Disable outbound calling if you do not use it, allow only the countries you call, and keep high-risk number ranges blocked. Twilio's geographic permissions split each country's ranges into low-risk and high-risk, say most businesses never need the high-risk ones, and offer a console check for whether a specific number falls in a high-risk range. Twilio does not publish the toll-fraud ranges ([geo permissions](https://www.twilio.com/docs/sip-trunking/voice-dialing-geographic-permissions), [dialing permissions API](https://www.twilio.com/docs/voice/api/dialing-permissions-resources)). Set usage triggers that fire on spend or long calls, for example suspending a subaccount above a daily amount.
- **Destination control in the agent.** Transfer and outbound numbers come from an allowlist or a verified record, never from text the caller or the model produced. Validate by country code and prefix, as Twilio advises for form fields. *Inference:* parse numbers into E.164 and check them against your allowed countries before dialing.
- **Caps per call.** `<Dial>` ends at 4 hours by default, the maximum unless you enable the 24-hour option, so set `timeLimit` well below it ([Twilio Dial](https://www.twilio.com/docs/voice/twiml/dial)). LiveKit SIP trunks offer `max_call_duration` and `ringing_timeout` ([SIP API](https://docs.livekit.io/reference/telephony/sip-api/)). For outbound SIP, OpenAI limits ringing to 3 minutes and a connected call to 2 hours and says neither is configurable in the creation request ([OpenAI SIP](https://developers.openai.com/api/docs/guides/voice-sip)). A Realtime session lasts at most 60 minutes ([OpenAI](https://developers.openai.com/api/docs/guides/realtime-conversations)). Also cap turns, tokens, transfers, and tool calls.
- **Caps across calls.** Rate limit per number, account, IP, and destination, and cap concurrency. OWASP's bot guidance says to apply rate limits at multiple keys, not just IP, because each key can be defeated in some way ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Bot_Management_and_Anti-Automation_Cheat_Sheet.html)). Cap verification messages per number and per account.
- **Refuse cheaply.** If `<Reject>` is the first verb in the response, Twilio does not answer the call. If any other verb comes before it, the call is received and your account is billed ([Twilio](https://www.twilio.com/docs/voice/troubleshooting)). *Inference:* reject blocked numbers and over-limit traffic before any speech-to-text or model minutes are spent.
- **Stop loops.** *Inference:* end a call after a set stretch without caller speech, after repeated near-identical turns, or when the other end sounds like an IVR or another bot. Two automated systems can otherwise talk until a cap hits.
- **Alert and cut off.** *Inference:* alert on spend per hour, calls per number, destination mix, many short calls to varied destinations, and calls with no caller speech, and keep a tested kill switch that disables outbound dialing and tools and plays a fixed message.
- **Provider spend limits** and per-key limits, with the caveats above.

## Voice cloning, impersonation, and disclosure

- **Consent for cloned voices.** OpenAI's usage policies prohibit using someone's likeness, including voice, without consent in ways that could confuse authenticity, and prohibit deceit, fraud, and impersonation ([OpenAI](https://openai.com/policies/usage-policies/)). OpenAI's custom voices are for eligible customers and use a recorded consent statement read aloud, matched to the sample, with a consent ID at voice creation ([custom voices](https://developers.openai.com/api/docs/guides/custom-voices)). ElevenLabs' policy bars replicating another person's voice without consent or legal right, deceiving people about whether a voice is AI, evading its guardrails such as Voice CAPTCHA, unauthorized robocalling, and call bombing ([ElevenLabs](https://elevenlabs.io/use-policy)).
- **Vendor checks are weak, so keep your own record.** Consumer Reports tested six cloning products in 2025. Four, including ElevenLabs, required only a checkbox or a similar self-attestation. Descript required a recorded consent statement, and Resemble AI required one after a first clone made from audio recorded in real time. CR noted that a consent statement is not foolproof, because a clone made on a second platform could generate the audio the first platform asks for ([CR press release](https://www.consumerreports.org/media-room/press-releases/2025/03/consumer-reports-assessment-of-ai-voice-cloning-products/), [CR report](https://innovation.consumerreports.org/AI-Voice-Cloning-Report-.pdf)). OpenAI's consent phrase is consent to OpenAI's use of the voice to build a model, so it does not replace your own record. For each cloned voice you use, keep the written consent: who, for what use, for how long, how to revoke, and the date.
- **Do not imitate real people or organizations.** A persona name is fine. Claiming to be a named real person, another company, or a government body is not. The FTC's impersonation rule covers government and business impersonation and took effect on April 1, 2024. Its page also lists a December 2024 notice of an informal hearing on a proposed amendment covering impersonation of individuals, so check the current status ([FTC](https://www.ftc.gov/legal-library/browse/rules/trade-regulation-rule-impersonation-government-businesses)).
- **Do not let callers change the voice.** *Inference:* expose no tool that clones a caller's voice or switches to a voice the caller names.
- **Say it is an AI.** The EU AI Act's Article 50(1) requires providers to design systems that interact directly with people so that people are told they are dealing with an AI, unless that is obvious to a reasonably well-informed person, and applies from 2 August 2026 ([Article 50](https://artificialintelligenceact.eu/article/50/), [Commission FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)). The ElevenLabs policy requires organizations using its agents to disclose AI clearly and prominently. The FCC ruled in February 2024 that AI-generated voices in robocalls are "artificial" under the TCPA ([FCC](https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal)). Whether and where disclosure is required depends on your location, your callers, and whether calls are outbound. Ask counsel, and default to disclosing at the start and whenever someone sincerely asks.

## Abuse, emergencies, and minors

**Abusive callers.** Decide the policy before launch: one calm warning, a second, then end the call with a short message. Log it, rate limit repeat callers, and keep a human review path. The agent should not mirror hostility or argue. It should not disclose personal data to an abuser or place calls for someone who wants to reach a third party: no tool should dial or message numbers a caller supplies. *Inference.* The ElevenLabs policy also bans unauthorized robocalling and call bombing.

**Emergencies and self-harm.** Decide what the agent does and never improvise it. Twilio supports emergency calling in a listed set of countries, requires the emergency number to be from the same country as the `From` number, and supports address registration only in the US, Canada, and the UK, with the address tied to a number. It asks that live test calls be sparing because some localities penalize unscheduled tests, and offers 933 as a US and Canadian test number ([Twilio](https://www.twilio.com/docs/voice/tutorials/emergency-calling-for-programmable-voice)). *Inference:* a bridged emergency call placed by the agent's line would carry the agent's number and address, not the caller's location, so do not build "the agent calls 911 for you" without a reviewed design for location, callback, and failure. The safe default is one short scripted reply: tell the caller to hang up and call the local emergency number now, stay on only if a human handoff is ready, and never say help is on the way unless it is. For self-harm, a US caller can reach the 988 Lifeline by call, text, or chat ([988](https://988lifeline.org/)). Keep the script short and have a qualified person review it. The ElevenLabs policy bans promoting self-harm.

**Minors.** COPPA treats a child as under 13 and includes a child's voice recording in personal information ([16 CFR 312.2](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312/section-312.2)). The ElevenLabs policy says organizations must not make their service available to under-13s, or to 13 to 18 year olds without parental consent, and OpenAI's usage policies include protections for people under 18 ([ElevenLabs](https://elevenlabs.io/use-policy), [OpenAI](https://openai.com/policies/usage-policies/)). Decide who the service is for. If it is not for children, then when a caller says they are a child, stop collecting personal data, do not verify or transact, and ask for a parent or guardian. If it is for children or families, get legal review before launch. *Inference:* do not build age guessing from voice, since that adds biometric processing.

## Test before launch

Use a written plan, not ad hoc calling. OWASP's agent guidance lists the abuse cases to keep as repeatable tests: prompt override, tool misuse, privilege escalation, memory poisoning, data exfiltration, recursive tool abuse, approval bypass, and multi-agent chaining. It also says to run them in CI for changes to prompts and tool policies, keep red-team prompts and expected denials under version control without secrets or live customer data, and block releases when policies change without updated tests ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)).

- **Layers.** Text turns against the real gateway with stubbed tools, then synthesized audio into the speech-to-text path, then a real call to a test number. See [agent evaluation](../../voice-agent-evaluation/SKILL.md) for layers and harnesses. Text tests miss speech recognition, background audio, and the carrier path.
- **Repeat runs.** Models respond differently to small changes in wording, and attackers try many variations until one works ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)). Run each script at least three times with different phrasing, and record the model, prompt revision, and tool policy.
- **Tools.** promptfoo's audio strategy converts text attack prompts to speech audio and needs remote generation, so the prompt text leaves your machine ([promptfoo](https://www.promptfoo.dev/docs/red-team/strategies/audio/)). NVIDIA's garak scans LLMs for weaknesses such as prompt injection and data leakage ([garak](https://github.com/NVIDIA/garak)), and Microsoft's PyRIT is an open-source framework for finding risks in generative AI systems ([PyRIT](https://github.com/microsoft/PyRIT)). They help with the text layer and with generating variants. None of them verifies your telephony path, your gateway, or your vendor settings.
- **Keep the suite.** Add every failed script to the regression suite, and re-run it after a change to the prompt, model, tools, knowledge base, or provider.
- **After launch.** Log gateway denials and refusals, alert on spikes, review a sample of calls, and rehearse the kill switch and key rotation.

The spoken scripts, pass criteria, and a results log are in [the red-team scripts](red-team-scripts.md). Twilio's own skills cover account-level setup for Twilio users; see the list in [the skill](../SKILL.md#related).
