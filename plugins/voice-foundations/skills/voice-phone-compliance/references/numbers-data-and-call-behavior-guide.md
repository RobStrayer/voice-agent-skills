# Numbers, regulated data and call behavior

[Handbook](https://github.com/RobStrayer/voice-agent-skills/blob/main/docs/handbook.md) / [Phone compliance skill](../SKILL.md)

**This is not legal advice.** Confirm your plan with counsel for every place you call, call from, or record. The law behind these steps is in the [legal requirements guide](legal-requirements-guide.md).

Checked against primary documentation on **September 30, 2026 UTC**. This is a check date, not a publication date. "Opened" means I fetched the page that day and read the passage I cite, in full or as an extract returned by a scraper. CFR text came from the eCFR API for September 28, 2026, and the links point to the same sections on the eCFR site. Vendor pages are marked "vendor". Scripts, thresholds and test steps are engineering guidance, not law.

## Contents

- Find the fix
- Why numbers get flagged
- What to do
- New numbers and rotation
- Monitor and pace
- HIPAA
- PCI (payment cards)
- Voiceprints and other biometrics
- Call behavior
  - Start of an outbound call
  - Start of an inbound call
  - When asked "are you a robot?"
  - Stop requests
  - Human transfer
  - Voicemail
  - Recording notice
- Evidence and retention
- Test plan

## Find the fix

| Problem or job | Start here | Evidence to keep |
| --- | --- | --- |
| Calls show "Spam Likely", or answer rates fell | [Why numbers get flagged](#why-numbers-get-flagged), then [monitor and pace](#monitor-and-pace) | Attestation per call, answer rate per number and carrier, label checks on handsets you own |
| New numbers get flagged at once | [New numbers](#new-numbers-and-rotation) | Ramp plan, per-number caps |
| Health information is in the audio path | [HIPAA](#hipaa) | Vendor map with a signed agreement for each |
| A caller may read out a card number | [PCI](#pci-payment-cards) | Proof the LLM, transcript, logs and recording never held card data |
| What do I say at the start, and on "stop"? | [Call behavior](#call-behavior) | Prompt versions, event log |
| What must I log and for how long? | [Evidence and retention](#evidence-and-retention) | Consent, suppression and call records |
| How do I test this safely? | [Test plan](#test-plan) | Tests that fail closed |

## Why numbers get flagged

Three separate systems decide how your call looks. Keep them apart when you debug.

1. **Authentication (STIR/SHAKEN).** The carrier that puts your call on the network signs it with a level of attestation.
   - **A:** the signer started the call on its network, knows the customer, and has verified the customer's right to the number. **B:** it knows the customer but has not verified the number. **C:** it only knows where the call entered, for example an international gateway ([ATIS-0300116 section 5.2](https://atis.org/wp-content/uploads/2020/07/ATIS-0300116-Interoperability_Standards_between_NGN.pdf), [RFC 8588](https://www.rfc-editor.org/rfc/rfc8588)).
   - What counts as "verified" is each signer's policy. ATIS lists examples: the number was assigned to you by the signer, sits in a range assigned to you, or you showed by business agreement or other evidence that you may use it.
   - US providers must implement it ([FCC call authentication page](https://www.fcc.gov/call-authentication), [47 CFR 64.6301](https://www.ecfr.gov/current/title-47/part-64/section-64.6301)).
   - Vendor example: Twilio's page defines the same three levels. A: the caller is known and has the right to use the number. B: the customer is known, but the right to the number is not. C: neither is met, including international calls ([Twilio, vendor](https://www.twilio.com/docs/voice/trusted-calling-with-shakenstir)).
2. **Analytics (behavior scoring).** Carriers and third-party engines score how a number behaves. The FCC says reasonable analytics may weigh large bursts of calls in a short time, low average call duration, many complaints about a line, and neighbor-spoofing patterns, among other factors ([FCC 20-96, paragraph 26](https://docs.fcc.gov/public/attachments/FCC-20-96A1.pdf)). One analytics vendor lists large call bursts, many short unanswered calls, frequent blocks and reports, and frequent hang-ups or low engagement as red flags. It also says inconsistent behavior can get a call tagged even with verified caller ID ([First Orion blog, August 1, 2025, vendor](https://firstorion.com/blog/number-reputation-management-bad-labels)). So an A attestation does not protect a number that behaves like a robocaller.
3. **Display.** Labels and names shown on the handset come from carrier and app data. Caller ID name is a separate setting. The Free Caller Registry does not set it ([Free Caller Registry](https://www.freecallerregistry.com/)).

## What to do

1. **Use numbers the provider can verify for you.** Buy numbers in your provider account, or complete the provider's business and number verification so calls sign at A. Check the attestation in your call logs. Do not send calls from numbers you cannot show authorization for. The TSR expects you to keep proof of authorization for each number and name you present ([16 CFR 310.5(a)(2)(ix)](https://www.ecfr.gov/current/title-16/part-310)).
2. **Register with the analytics vendors.** The [Free Caller Registry](https://www.freecallerregistry.com/) is free. You register up to 20 numbers by form, or upload a file. Your data goes to First Orion, Hiya and TNS. Only the business that uses the numbers may register them. A service provider, BPO or other third party registering for another business is not allowed, and must contact the call protection providers directly. Registration does not guarantee redress, and the site says it is not a replacement for reputation monitoring. The numbers must not be used for calls that break consumer protection law. If you run an agent platform for clients, each client registers its own numbers, or you deal with the vendors directly.
3. **Know the carrier redress path.** A terminating carrier that blocks calls, or that uses caller ID authentication to decide how to deliver them, must publish one point of contact for errors, give a status update within 24 hours. If your claim is credible and the carrier decides the calls should not have been blocked or treated that way, it must promptly stop the treatment for that number. It may not charge for good-faith complaints ([47 CFR 64.1200(k)(8)](https://www.ecfr.gov/current/title-47/part-64/section-64.1200)). This covers carrier blocking and delivery treatment, not every app label. For labels, use the analytics vendors' own contacts from the registry page.
4. **Log blocking signals.** A carrier that blocks on analytics must return SIP 603+ (or the ISUP equivalent) to the origin, and every provider in the path must pass it on ((k)(9)). Count those codes per number. They tell blocked calls apart from calls nobody answered.
5. **Consider branded calling.** Some vendors show a verified business name, and sometimes a logo and call reason, on the handset. Requirements vary by vendor and tier. Twilio offers a Basic tier that shows a business name and an Enhanced tier that adds a logo and call reason. Enhanced also needs STIR/SHAKEN and a signed letter of authorization, and what shows depends on the carrier and device (Twilio, vendor: [enhanced branded calling](https://www.twilio.com/docs/voice/branded-calling/us-enhanced), [setup tutorial](https://www.twilio.com/en-us/blog/developers/tutorials/product/enable-branded-calling-twilio)). Branding helps people decide to answer. It does not replace good behavior.

## New numbers and rotation

- A new number has no good history. A sudden campaign of short, unanswered calls from it looks like the pattern the FCC lists above. Ramp volume slowly, spread calls across the allowed hours, and cap calls per number per day.
- I found no carrier-published safe volume per number. Numbers you may see in blog posts are rules of thumb. Set thresholds from your own baselines and alarm on changes.
- Rotating numbers to shake a label treats the symptom. This is engineering reasoning, not a sourced rule: the behavior that earned the label moves with you, and every new number starts with no history. Fix the cause first: consent, list quality, pacing, call length, hang-ups.
- Never spoof. It is unlawful to cause misleading or inaccurate caller ID with intent to defraud, cause harm, or wrongfully obtain value ([47 U.S.C. § 227(e)](https://www.law.cornell.edu/uscode/text/47/227)).

## Monitor and pace

| Watch | Why | Where to get it |
| --- | --- | --- |
| Attestation per call (A, B, C) | B and C mean your number is not verified | Provider call logs or SIP verification status |
| Answer rate per number, carrier and hour | A drop on one carrier often means a label or block | Your call records |
| Median call length, and the share of very short calls | The FCC lists low average duration as a factor | Your call records |
| SIP 603+ or ISUP 21 counts | Shows analytics blocking | Provider signaling logs |
| Silent, abandoned and hang-up rates, and answering-machine detection errors | Real people hearing silence is a legal issue and a signal | Call events (see the [call reliability skill](../../voice-call-reliability/SKILL.md)) |
| "Stop", "who is this" and "wrong number" rates per list | High rates mean bad consent or a bad list | Intent events |
| Handset checks | Shows what people see | Test calls between numbers and phones you own, on the major carriers, with the user's OK |

Stop a campaign automatically when answer rate, call length or block counts cross your limits. Do not fix a low answer rate by adding numbers.

## HIPAA

Applies when you handle health information for a HIPAA covered entity (a clinic, plan or similar), or for a business associate of one.

- A **business associate** creates, receives, maintains or transmits protected health information on behalf of a covered entity. Subcontractors that do so for a business associate are included ([45 CFR 160.103](https://www.ecfr.gov/current/title-45/part-160/section-160.103)).
- A covered entity may let a business associate handle that data only with satisfactory assurances, documented in a written contract. A business associate needs the same from its subcontractors ([45 CFR 164.502(e)](https://www.ecfr.gov/current/title-45/part-164/section-164.502), [164.308(b)](https://www.ecfr.gov/current/title-45/part-164/section-164.308)).
- HHS says a cloud provider that stores or processes protected data for you is a business associate even if it holds only encrypted data and has no key. The "conduit" exception is limited to transmission-only services with transient storage. Using such a provider without an agreement is a violation ([HHS cloud computing guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html)).

What to do:

1. Draw the audio and text path: carrier, recorder, speech-to-text, LLM, text-to-speech, transcript store, analytics, logging and tracing tools, CRM. Mark which vendors see health information.
2. Each vendor that stores or processes it needs a signed business associate agreement that covers the exact product and region you use. Do not assume a vendor's HIPAA claim covers every tier.
3. A vendor with no agreement gets no health information. Redact before sending, or pick another vendor.
4. Put no health detail in a greeting or a voicemail. Say nothing until the person confirms who they are in a way you set. This is engineering guidance.
5. A HIPAA covered entity's "health care" messages get special treatment under the TCPA and the TSR. See the legal guide.
6. Required Security Rule documentation must be kept six years ([45 CFR 164.316(b)(2)](https://www.ecfr.gov/current/title-45/part-164/section-164.316)). That rule covers documentation of your policies and actions. I found no federal period for call audio itself, so ask counsel about state rules and your contracts.

A proposed HHS update to the Security Rule (January 2025) is not final. A law-firm note dated July 13, 2026 says HHS moved it to its long-term agenda with July 2027 as the target (secondary: [Clark Hill](https://www.clarkhill.com/news-events/news/hipaa-security-rule-update-delayed-until-2027/); proposal: [Federal Register](https://www.federalregister.gov/documents/2025/01/06/2024-30983/hipaa-security-rule-to-strengthen-the-cybersecurity-of-electronic-protected-health-information), a proposed rule at 90 FR 898, published January 6, 2025).

## PCI (payment cards)

PCI DSS v4.0.1 (June 2024) calls itself the current version in its own version table. PCI SSC's PDF link returned an error to my fetcher, so I read the text in a copy hosted at [middlebury.edu](https://www.middlebury.edu/sites/default/files/2025-01/PCI-DSS-v4_0_1.pdf). The [PCI SSC document library](https://www.pcisecuritystandards.org/document_library/) still lists PCI DSS v4.0.1 (June 2024) as the standard, on a page it shows as updated on September 14, 2026. PCI rules are set by the payment brands and enforced through your acquirer, not by statute.

- Sensitive authentication data, including the card verification code, must not be stored after authorization, even if encrypted (requirement 3.3.1, and 3.3.1.2 for the code).
- The card number must be unreadable anywhere it is stored (3.5.1). The test procedures name logs and payment application logs.
- Keep account data storage to a minimum with retention and disposal rules (3.2.1).
- PCI SSC's telephone guidance says to keep card data out of recordings where you can, using pause-and-resume or DTMF masking. It also says pause-and-resume does not reduce PCI DSS applicability to the agent, the agent desktop environment or any other system in the telephone environment (section 6.5.1). If a tool cannot stop the audio being stored, the card verification code must be deleted from the recording once the transaction is processed. Where pause-and-resume is used, check the recordings regularly; the guidance suggests weekly ([PCI SSC, Protecting Telephone-Based Payment Card Data, November 2018](https://listings.pcisecuritystandards.org/documents/Protecting_Telephone_Based_Payment_Card_Data_v3-0_nov_2018.pdf)). That paper predates v4.0.1 and uses older requirement numbers.

For an AI agent, a transcript or an LLM prompt is storage. Design so card digits never reach them. Card digits go only to a payment provider that captures keypad tones itself, so speech-to-text, the model, transcripts and logs never receive them. Pausing a recording is not a substitute: it keeps digits out of the recording only, while spoken or keyed digits still reach speech-to-text, the model and vendor logs. Use pause-and-resume only as an extra layer on the recorder, and check weekly that recordings hold no card data.

1. Hand the payment step to a provider that captures keypad tones itself, so the agent never hears the digits. The [Twilio compliance skill](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-compliance-traffic/SKILL.md) shows one such pattern for Twilio.
2. Pausing is not an alternative for an AI agent. Pause-and-resume keeps digits out of the call recording only. Spoken digits still reach speech-to-text, the LLM prompt and vendor logs. PCI SSC says pause-and-resume can take the recorder and storage out of scope, but not the agent or other systems in the telephone environment (section 6.5.1 of the November 2018 paper above). If you also pause the recorder around step 1, check weekly that recordings hold no card data. The mechanics are in the [Twilio call recordings skill](https://github.com/RobStrayer/voice-agent-skills/blob/main/skills/twilio/twilio-call-recordings/SKILL.md).
3. Add a redaction test for card-shaped numbers in transcripts, traces and analytics events.

Scope is a question for your acquirer or a PCI assessor. This guide does not certify anything.

## Voiceprints and other biometrics

Under the GDPR, biometric data used to identify a person is special-category data ([Article 9(1)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679)). US state biometric laws also apply; Illinois BIPA treats a voiceprint as a biometric identifier and needs a written release before collection. See the [security guide](../../voice-agent-security/references/security-guide.md#do-not-let-a-voice-be-the-password). Other states were not checked. If you use voice to identify or authenticate callers, ask counsel before you launch.

## Call behavior

Wording below is a starting point. Have counsel review it, and replace the brackets.

### Start of an outbound call

```
This is an automated assistant calling for {registered business name}.
You can say "stop" or press 9 at any time to stop these calls.
I'm calling about {purpose, in one sentence. Say it is a sales call if it is}.
This call may be recorded and transcribed. Is this {first name}?
```

- Use the name the business is registered under. Put the opt-out offer second, so it lands within 2 seconds of the name ([legal guide](legal-requirements-guide.md#what-the-call-must-say-and-offer)).
- Only promise the keypad option if your pipeline detects DTMF for the whole call. Test it.
- Start talking within 2 seconds of the person's first "hello".
- Say the call is automated in the person's language.
- For health calls, give no health detail until the person confirms who they are.

### Start of an inbound call

```
Thanks for calling {company}. I'm an AI assistant.
This call is recorded and transcribed to help with your request.
Say "person" at any time to reach someone.
```

### When asked "are you a robot?"

Answer truthfully every time, in the same call, even mid-task:

```
Yes, I'm an AI assistant, not a person. I can connect you to a person if you'd like.
```

Do not let a persona prompt override this. If no human is available, offer a message or a callback.

### Stop requests

1. Detect stop intent by voice and by keypad. Cover "stop", "don't call me", "remove my number", "take me off your list", "do not call", "unsubscribe". Treat "not interested" as a stop for marketing calls unless counsel narrows it. This list is a default, not a legal definition.
2. Stop pitching at once. Do not ask "are you sure". Do not offer alternatives.
3. Write the suppression to the shared store first: number, time, call ID, the words used, scope. Then say the confirmation:

```
Understood. I've added this number to our do-not-call list. Goodbye.
```

If the write failed, do not say it is done. Say "I'll make sure this number is removed", raise an alert, and retry until it lands.
4. End the call. Cancel queued retries. Push the suppression to the dialer, the CRM and every vendor that holds a list. The legal limit is 10 business days; build for seconds.
5. "Wrong number" also suppresses the number and flags it as possibly reassigned. "Call me later" is a callback request. Record the time they gave and call then, if consent still holds.

### Human transfer

Transfer when the person asks, when the agent fails to understand twice, or when the topic is sensitive, legal, or medical. If someone describes an emergency, tell them to hang up and call their local emergency number. Say "I'm connecting you to a person now". Do not say "connected" until a human accepts. If nobody answers, take a message or set a callback, and treat the callback as a consented request. Mechanics are in the [call reliability skill](../../voice-call-reliability/SKILL.md).

### Voicemail

- An AI voicemail is an artificial-voice call. Consent rules apply.
- Keep it short and free of sensitive detail: who is calling, a callback number, one line of purpose.
- Telemarketing voicemail must give a toll-free number that reaches the automated opt-out:

```
This is an automated message from {registered business name}, {callback number}.
{One line of purpose, no sensitive details}.
To stop these calls, call {toll-free opt-out number} at any time.
```

- If answering-machine detection is unsure, do not guess. Follow the policy in the call reliability skill, and log the uncertainty.

### Recording notice

Announce recording and transcription at the start of every call, in every state. If the person objects, stop recording and transcription or move them to a human path that does not record. If the product cannot work without processing audio, say so and end the call politely. See the [legal guide](legal-requirements-guide.md#recording-and-transcripts).

For wording and turn-taking, see the [conversation design skill](../../voice-conversation-design/SKILL.md).

## Evidence and retention

A regulator or a plaintiff will ask you to prove consent, prove the stop request was honored, and show what the caller heard. The TSR lists what a complete consent record holds ([16 CFR 310.5(a)(8)](https://www.ecfr.gov/current/title-16/part-310)). The fields below follow it and add AI-specific ones. Use them for every campaign, not only sales.

| Record | Fields |
| --- | --- |
| Consent | Consent ID; number (E.164); name if given; the seller named; channels covered (say "AI or automated voice" if it does); purpose; a copy of the consent text and form exactly as shown; how it was given (web form, signed document, recorded verbal); date and time in UTC; for web consent, page, IP address and user agent; lead vendor and contract if bought; revoked at, how, and the call ID; date and result of the last reassigned-number check |
| Suppression | Number; time; source call ID; the exact words or key pressed; scope; which systems received it and when |
| List access | Which registry version you used, who accessed it, the date, the subscription account and the campaign ([16 CFR 310.5(a)(11)](https://www.ecfr.gov/current/title-16/part-310)) |
| Call | Call and attempt IDs; campaign; calling and called numbers; caller ID name and number shown; start time in UTC plus the recipient's local time and how you found their time zone; duration; disposition (answered, machine, voicemail, transferred, dropped); transfer destination; prompt and script version; timestamps for the AI disclosure, recording notice and opt-out offer; consent ID; list versions |
| Vendors | Contracts and agreements for each provider in the audio path, with dates in force ([16 CFR 310.5(a)(9)](https://www.ecfr.gov/current/title-16/part-310)) |

Keep card numbers, health detail and other sensitive data out of these records.

| Data | Keep for | Source |
| --- | --- | --- |
| Do-not-call requests | At least 5 years | [47 CFR 64.1200(d)(6)](https://www.ecfr.gov/current/title-47/part-64/section-64.1200) |
| Telemarketing records: scripts, unique prerecorded messages, call records, consent records, registry versions, service-provider contracts | 5 years from creation, last use, or contract expiry | [16 CFR 310.5](https://www.ecfr.gov/current/title-16/part-310) |
| Other consent evidence (not telemarketing) | At least 4 years after the last call, longer if counsel says so | [28 U.S.C. § 1658(a)](https://www.law.cornell.edu/uscode/text/28/1658), my reading |
| HIPAA Security Rule documentation | 6 years | [45 CFR 164.316(b)(2)](https://www.ecfr.gov/current/title-45/part-164/section-164.316) |
| Call audio and transcripts | The shortest period that meets a stated purpose. In the EU, storage must be limited to what is necessary | [GDPR Article 5(1)(e)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679) |
| Card verification codes | Not after authorization | PCI DSS 3.3.1 |

Evidence rules and deletion rules can collide. Keep consent, suppression and call metadata in a separate store from audio and transcripts. Delete audio and transcripts on schedule. Do not keep audio "just in case". Ask counsel how to keep a minimal suppression record when someone asks you to erase their data.

## Test plan

Never place a test call to a real person, turn on recording for one, or change carrier or registry settings without the user's OK. Use numbers and phones the user owns.

- **Dry run.** A mode that runs every gate and writes the attempt record but never dials.
- **Fail closed.** Kill the consent lookup, the registry file and the time-zone service. Each failure must block the call and log why.
- **Windows.** Test 7:59 a.m. and 9:01 p.m. recipient time, daylight-saving changes, and a number whose area code disagrees with where the person is.
- **Consent.** No consent, revoked consent, consent for a different seller, consent for SMS only. None may dial.
- **Stop.** Spoken, keyed, hedged ("please don't ring again") and noisy. Each must write the suppression before the confirmation line, cancel queued calls, and end the call.
- **Truthful AI.** Ask "are you a robot?" at the start, mid-task and during a transfer. The answer is always yes.
- **Timing.** Measure the time from "hello" to the first word, and from the name to the opt-out offer. Both under 2 seconds.
- **Data.** Read a fake card number and a fake health detail to the agent. Search transcripts, logs, traces and analytics for them. The count must be zero.
- **Voicemail.** Leave the message on a mailbox you own. Check the toll-free opt-out line works.

See the [agent evaluation skill](../../voice-agent-evaluation/SKILL.md) for building scored test sets.
