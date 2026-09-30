# Validate in code and keep the evidence

[Handbook](../../../../docs/handbook.md) / [Data capture skill](../SKILL.md)

Reviewed **2026-09-30 UTC** using current provider documentation and standards pages. This is the review date, not a publication date. Provider and standards facts are linked where they appear. Paragraphs marked *Inference* are engineering judgment, not documented provider behavior. This is engineering guidance, not legal advice. The authorization gateway is in the [security guide](../../voice-agent-security/references/security-guide.md#authorize-tools-in-the-backend) and is not repeated here.

## Let the model propose and code decide

A speech model writes a guess. A language model may tidy that guess into a structured field. Neither one decides whether the value is real, was said, was confirmed or may be written. Code decides all four.

| Step | Owner | Must be true to move on |
| --- | --- | --- |
| Heard | Recognizer | A final transcript segment, or keypad digits, exist for this question |
| Normalized | Code | Words and numerals are in the canonical form. Number words that cannot be mapped are sent back to the caller |
| Proposed | Model or parser | A structured field, such as `{"field": "phone", "value": "+14155550123"}`. The model may fill it. It cannot commit it |
| Supported | Code | Every digit came from this caller's speech or keypad, in answer to this question ([check](#check-that-the-transcript-supports-the-value)) |
| Validated | Code | Shape, checksum and real-system checks passed ([gate](#gate-every-write)) |
| Read back and confirmed | Code and the voice | A yes arrived after the read-back finished, for this exact value ([how](ask-and-read-back.md#read-the-value-back)) |
| Committed | Backend | The gate passed again at write time, the write went through the gateway with an idempotency key, and the result is stored |

Validate before the read-back, so you never read out a value that cannot be right. Run the gate again at write time, because a lookup result, a verification level or the caller's answer can change during the call.

```python
# Conceptual. The model proposes; code decides.
def commit_field(call, field, proposal):
    value = normalize(field, proposal.value)              # per-field code
    if not supported(value, call.heard(field), call.keypad(field)):
        return re_ask(field, why="not_in_transcript")
    problems = validate(field, value)                     # format, checksum, lookups
    if problems:
        return re_ask(field, why=problems)
    if not call.confirmed(field, digest(value)):          # yes bound to this exact value
        return read_back(field, value)
    return write(call.session, field, value, evidence(call, field))
```

## Gate every write

All of these must pass, and a failure or an error means no write. Fail closed.

1. **Supported.** The value came from this caller, on this call, in answer to this question.
2. **Shape.** A parser or pattern for the field: E.164 for a phone number, an ISO date in a named zone, an amount in integer minor units with a currency code.
3. **Checksum,** where the value has one. A code you issue can carry a check symbol ([codes](entity-protocols.md#codes-and-reference-numbers)). Card numbers are not checked in your code: card handling belongs to the payment service ([privacy](../SKILL.md#keep-sensitive-data-off-the-model-path)).
4. **Lookup in the real system.** The customer list, the calendar, the address service, the code table. The [validators by field](#validators-by-field) table lists them.
5. **Rules.** Ranges, business hours, limits, and whether this caller may take this action.
6. **Confirmation bound to the value.** A digest of the exact value, so a later change voids the yes.
7. **Authorization.** The caller's verification level allows this write.
8. **Safe to repeat.** An idempotency key, so a retry cannot write twice. See the [action contract](../../voice-conversation-design/references/transactions-and-handoffs.md#define-the-action-contract) and the [uncertain write](../../voice-conversation-design/references/transactions-and-handoffs.md#work-through-an-uncertain-booking).

When a check fails, say what to do next and not which check failed, if the reason would tell a caller whether an account or code exists ([security guide](../../voice-agent-security/references/security-guide.md#verify-in-steps-in-the-backend)).

## Validators by field

The reasons and sources for each check are in the [protocols](entity-protocols.md). This is the list to build from.

| Field | Code checks | Real-system check |
| --- | --- | --- |
| Phone | E.164 shape; region rules from a phone library | Line lookup if you need it. A valid number is not proof it is this caller's |
| Email | One `@`, text on both sides, a dot in the domain | DNS lookup for the domain. A message the caller acts on is the only proof the address works |
| Name | Allowed characters and length in your own system | None. A search key only, never a reason to read a record out |
| Address | All parts present | Address validation verdict and the standardized address |
| Date and time | Real calendar date; weekday matches when given; local time exists in the IANA zone | Calendar or availability system |
| Amount | Integer minor units; ISO 4217 currency | Limits, balance, permissions |
| Code | Length, alphabet, check symbol | Lookup scoped to this caller, with no near matches from other records |
| Yes or no | One of yes, no, unclear, bound to the question ID | None |

## Check that the transcript supports the value

Digits nobody said can get into a proposal. *Inference:* a language model can complete a pattern or reuse a number from earlier in the call. If your recognizer formats numbers for you, read the [formatting switches](recognition-aids.md#number-formatting-switches) first: they change what this check can see. A recognizer can also turn noise into text ([rules for every field](entity-protocols.md#rules-for-every-field)). So test the proposal against what the caller actually said.

For a digit field, parse the digits from the final transcript of this question's turn, or from the keypad, and require the value's digits to appear in order and unbroken in them. Allow a prefix that your own code added, such as a country code. Where the answer should hold only this field, require an exact match, so a value cut short fails. [`readback.py`](../scripts/readback.py) has a small version of these steps:

```bash
python scripts/readback.py heard "four one five, five five five, zero one two three"
python scripts/readback.py support +14155550123 "four one five five five zero one two three" --assume 1
python scripts/readback.py support +14155550123 "four one five five five five zero one two three" --assume 1 --exact
```

The first prints `digits: 4155550123`. The second exits with status 1, because the spoken digits are 9 long and the value has 10. The third passes only when the answer holds exactly those digits. Without `--exact`, a value cut short (9 of the 10 digits) still passes, because it sits inside the longer answer. Number words such as "fifteen" or "fifty" are reported and not turned into digits. Each may hide digits, so a number word anywhere in the answer makes the check fail, even before or after the digits, and so does a "double" or "triple" with no digit after it. The right move is to ask for the digits one at a time. Any other word between two digits, such as "um" or a homophone like "for", breaks the run, so the check fails safe and the flow asks again. That is strict on purpose: loosen it only with fixtures that show the looser rule never passes a missing digit.

The check has a ceiling. It shows the digits were said, not that they answer this question, so a ZIP code said earlier could match a phone field by chance. Bind the check to the segments that follow the question, and keep the confirmation. For a spelled value, *Inference:* decode the spelling alphabet and compare the proposal character by character with what was spelled.

*Inference:* a speech-to-speech model takes in the audio itself, so there may be no transcript of the caller's words that is independent of the model (the [security guide](../../voice-agent-security/references/security-guide.md#sensitive-data-in-every-store) lists audio for speech-to-speech models among what an LLM provider receives). Run this check against a transcript of the caller's audio that does not come from the model's own output, such as a separate recognizer, and store that transcript with the value. If there is none, the check cannot run, so take digit fields on the keypad.

Frameworks can hide this. LiveKit's name, email, address, date of birth and phone number tasks take `require_explicit_ask`, which defaults to `False`, so a task "can use" a value from earlier in the session's `chat_ctx` when the caller mentioned it before. Set it to `True` when the value must be an answer to this question ([GetPhoneNumberTask](https://docs.livekit.io/agents/prebuilt/tasks/get-phone-number/)).

## What to store with each value

Keep enough to let a person check the value, to tell a recognition fault from a settings fault, and to answer a dispute. One record per captured field per call:

```json
{
  "call_id": "call_0001",
  "field": "callback_phone",
  "value": "+14155550123",
  "question_id": "q_callback_phone_1",
  "attempt": 2,
  "channel": "voice",
  "transcript": {"segment_ids": ["seg_41", "seg_42"],
                 "text": "four one five five five five zero one two three"},
  "audio": {"ref": "rec_0001", "start_ms": 84210, "end_ms": 89640},
  "stt": {"model": "<provider model id>", "keyterms_version": "v3", "numerals": false,
          "confidence": null},
  "read_back": {"text": "plus one, four one five, five five five, zero one two three",
                "spoken_at_ms": 91200},
  "confirmation": {"text": "yes that's right", "start_ms": 96300, "end_ms": 97100},
  "checks": {"supported": true, "e164": true, "region_valid": true},
  "written": {"record": "crm:contact/789", "idempotency_key": "call_0001:callback_phone:2"}
}
```

- **Value and form.** The canonical value, and the spoken form you read back.
- **Transcript.** The raw final text and the segment IDs for the turn. Keep the raw text next to the value so a wrong value can be traced. It is a copy of the call transcript, so it follows the transcript's retention and access rules and not the value's.
- **Audio offsets.** A recording reference with start and end times for the answer and for the confirmation. Measure them on your own audio clock. OpenAI's `gpt-live-transcribe` returns no word-level timestamps, speaker labels or confidence ([OpenAI](https://developers.openai.com/api/docs/guides/realtime-transcription)), so do not count on the recognizer for them. Dual-channel recordings keep the caller and the agent apart ([Twilio recordings skill](../../../twilio/twilio-call-recordings/SKILL.md)).
- **Recognizer and aids.** The model, the aid list version, `numerals` and turn settings ([recognition aids](recognition-aids.md#record-what-was-on)). Store confidence only when the provider returns it, and mark it `null` when it does not.
- **Attempts and channel.** How many tries, and whether the value came by voice, keypad, link or a person.
- **Check results.** Each validator and its result, with the library or service version.
- **Write.** The record written and the idempotency key.

Audio and transcripts are personal data. Recording needs a notice and, in some places, consent ([compliance skill](../../voice-phone-compliance/SKILL.md)). Keep audio only as long as a stated purpose needs it, and do not keep it "just in case" ([evidence and retention](../../voice-phone-compliance/references/numbers-data-and-call-behavior-guide.md#evidence-and-retention)). *Inference:* when the audio is deleted, keep the value, the checks and the confirmation flag, and let the audio reference expire. A person can no longer re-listen, and the record must say so. Keep card numbers, PINs and ID numbers out of this record altogether.

## Use framework capture tasks with care

LiveKit Agents (Python, beta) ships tasks that collect a field for you. Their pages describe what each handles. The rest stays with you.

| Task | The page says it handles | Still yours |
| --- | --- | --- |
| [GetPhoneNumberTask](https://docs.livekit.io/agents/prebuilt/tasks/get-phone-number/) | Spoken digits to numerals, 7 to 15 digits with an optional `+`, read-back in groups | Country rule, region validation, E.164 storage, the transcript check |
| [GetEmailTask](https://docs.livekit.io/agents/prebuilt/tasks/get-email/) | "dot", "underscore", "dash", "plus" to symbols, spelled-out patterns | Spell-back, domain check, proof by message |
| [GetNameTask](https://docs.livekit.io/agents/prebuilt/tasks/get-name/) | Letter-by-letter and phonetic alphabet input, optional spelling verification (`verify_spelling`, default `False`) | What your systems can store, never correcting to a dictionary word |
| [GetAddressTask](https://docs.livekit.io/agents/prebuilt/tasks/get-address/) | Any country's format, spelled-out numbers, postal codes digit by digit | A lookup against an address service. The page says "validate" and describes format handling |
| [GetDOBTask](https://docs.livekit.io/agents/prebuilt/tasks/get-dob/) | Spoken dates, two-digit years ("90" becomes 1990), rejects future dates | Your century rule for other years, age rules, not reading it out to an unverified caller |

Each task page says the task's LLM sees the `chat_ctx` you pass, and that `require_confirmation` defaults to `True` in audio sessions and `False` in text ([GetEmailTask](https://docs.livekit.io/agents/prebuilt/tasks/get-email/) is one example). *Inference:* a read-back the task's LLM produces is not built from your stored value in code. Treat a task's result as a proposal, and run the gate and your own read-back on it.

**Do not use `GetCreditCardTask` for real card data.** It collects the cardholder name, card number, security code and expiry through a task group, and its page says sensitive information is never repeated back to the user in audio sessions ([GetCreditCardTask](https://docs.livekit.io/agents/prebuilt/tasks/get-credit-card/)). *Inference:* because the tasks are run by an LLM over transcribed speech, the digits are on the model path, which the [security guide](../../voice-agent-security/references/security-guide.md#keep-cards-pins-and-ids-off-the-model-path) says to avoid. Use the keypad-to-processor path in the [compliance guide](../../voice-phone-compliance/references/numbers-data-and-call-behavior-guide.md#pci-payment-cards).

## A second transcriber for hard fields

*Inference:* a second recognizer on the audio for the hardest fields, such as spelled names and codes, may catch errors that one recognizer repeats. I found no provider page or study that measures the gain for this, so it is an option to test and not a recommendation.

*Inference:* if you try it, run the second recognizer only on the fields that still fail after the other controls. Agreement goes on to the read-back. Disagreement goes to a spell-back or a fallback channel. Never average or merge characters from two transcripts. Count the costs first: extra spend ([cost estimation](../../voice-cost-estimation/SKILL.md)), extra latency, and another vendor receiving call audio, which needs its own agreement and data settings ([compliance skill](../../voice-phone-compliance/SKILL.md)). Measure it on your fixtures ([test fixtures](test-fixtures.md)) before you keep it.

## Keep values out of general logs

Log the field name, the attempt number, the outcome and the names of the checks that ran. Do not log the value, the transcript or the audio reference in application logs, traces or analytics. Put evidence in its own store with its own access and retention ([sensitive data in every store](../../voice-agent-security/references/security-guide.md#sensitive-data-in-every-store), [set retention, access and deletion](../../voice-agent-security/references/security-guide.md#set-retention-access-and-deletion-on-purpose)). Redaction is best effort, so do not collect what you do not need ([security guide](../../voice-agent-security/references/security-guide.md#redaction-is-best-effort-so-do-not-collect-first)).

## Sources

Retrieved 2026-09-30. "Shown" is a date printed on the page, when there was one. Context7 was not used for this file. Standards and provider pages for the validators are listed in [the protocols](entity-protocols.md#sources).

| Source | Supports | Shown |
| --- | --- | --- |
| LiveKit [prebuilt tasks](https://docs.livekit.io/agents/prebuilt/tasks/) and the [phone number](https://docs.livekit.io/agents/prebuilt/tasks/get-phone-number/), [email](https://docs.livekit.io/agents/prebuilt/tasks/get-email/), [name](https://docs.livekit.io/agents/prebuilt/tasks/get-name/), [address](https://docs.livekit.io/agents/prebuilt/tasks/get-address/), [date of birth](https://docs.livekit.io/agents/prebuilt/tasks/get-dob/) and [credit card](https://docs.livekit.io/agents/prebuilt/tasks/get-credit-card/) task pages | What each task handles, `require_confirmation` and `require_explicit_ask` (on the task pages), `GetCreditCardTask` | none shown (the pages print a render time only) |
| [OpenAI realtime transcription](https://developers.openai.com/api/docs/guides/realtime-transcription) | No word timestamps, speaker labels or confidence from `gpt-live-transcribe` | none shown |

The second-recognizer idea is an untested engineering option, and no source measured its effect. No provider requests, audio tests or accuracy measurements were run to write this file. The script self-test is the only code that ran.
