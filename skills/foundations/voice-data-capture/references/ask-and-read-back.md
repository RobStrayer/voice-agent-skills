# Asking, correcting and reading back

[Handbook](../../../../docs/handbook.md) / [Data capture skill](../SKILL.md)

Reviewed **2026-09-30 UTC** using current provider documentation. This is the review date, not a publication date. Provider facts are linked where they appear. Paragraphs marked *Inference* are engineering judgment, not documented provider behavior. Numbers such as retry counts and group sizes are starting defaults to tune on your own calls, not findings. Provider settings change, so check the current page before you rely on one. [Sources](#sources) lists each page and the date it shows.

## Ask one field at a time

A good question names the field, says the format, gives one example and ends there.

| Part | Do | Example |
| --- | --- | --- |
| Field | Ask for one field. If the caller volunteers more, take it and confirm each field on its own | "What's the ZIP code?" |
| Format | Say the shape and the length | "Five digits." "Eight characters, letters and numbers." |
| Example | Give one, spoken the way you want to hear it | "You can say it in groups, like four one five, five five five, zero one two three." |
| Way out | Name the keypad before a long digit string | "Or type it on your keypad and press pound." |
| End | Finish on the question. No list of options after it | "What number should we call you on?" |

*Inference:* keep each field's prompt in code or in a fixed template, not free text from the model each time. The format and the example then stay the same on every call, and you can test them.

Write every prompt for the ear. Short sentences, the question last.

## Accept corrections

People correct by saying "no" and then the right part. Google's conversation design guidance says to expect this, to allow the correction in one step ("No, 7 AM"), and not to make the caller start the dialog again ([Google confirmations](https://developers.google.com/assistant/conversation-design/confirmations)). Build for it.

Keep the value in pieces (groups or single characters) so a correction can replace one piece. Then read the whole corrected value back, because the correction can be misheard too.

| The caller says | Code does |
| --- | --- |
| "No, the last four are two zero one three" | Replace the last group. Read the whole value back |
| "No, that's a five, not a nine" | Find the piece with that symbol. If more than one matches, ask "Which group?" |
| "The third digit is a P, as in Papa" | Replace that position. Read the whole value back |
| "No" and nothing else | Ask "Which part is wrong?" If they cannot say, ask again in smaller groups |
| "Start over" | Clear the field. Keep the attempt in the record |

A "no" is data. Keep it with its audio offset, because the fields that get corrected most are the ones to add recognition aids and fixtures for.

## Give the caller a way out

Cap the attempts, then change channel. A starting default is two voice attempts per field, counted per field and not per call. This is judgment and not a measured value, so tune it on your own calls.

| Step | What you do | Move on when |
| --- | --- | --- |
| 1 | Ask the normal way, with the format and an example | The value is read back and confirmed, or the first miss |
| 2 | Ask again with help: one group at a time, or letter by letter with the spelling alphabet | The second miss, or a third correction on the same field |
| 3 | Change channel: keypad, a link, or a person | |

| Channel | Good for | Watch |
| --- | --- | --- |
| Keypad (DTMF) | Digit strings: phone numbers, ZIP codes, account numbers, dates as digits | No letters. The caller needs a hand free. Some frameworks turn keypresses into transcript text for the model ([by framework](#keypad-input-by-framework)) |
| Text a link | Emails, names, addresses, anything long or spelled | Needs a mobile number and permission to text. See [Text a link](#text-a-link) |
| Person | Anything that still fails, and anything costly | Hand over the partial value, why it failed and the audio offsets, so the caller does not start again. See the [call reliability skill](../../voice-call-reliability/SKILL.md) for transfers |

When you switch channel, say why in plain words: "I'm having trouble with that one. Let's use your keypad instead."

### Text a link

For long or spelled fields, a link to a short form beats three failed voice attempts. The caller types it, sees it and fixes it.

- Sending a text is a message you send on the business's behalf, so check consent and carrier rules with the [phone compliance skill](../../voice-phone-compliance/SKILL.md) and counsel before you send one.
- **Where to send it.** Prefer the number the call came from, confirmed by its last digits, and remember that caller ID is a claim ([security guide](../../voice-agent-security/references/security-guide.md#caller-id-is-a-claim)). A number the caller says aloud is text the caller produced: parse it to E.164, check it against the countries you serve, and cap sends per call, per number and per account, as the security guide advises for outbound numbers and verification messages ([cost abuse and toll fraud](../../voice-agent-security/references/security-guide.md#cost-abuse-and-toll-fraud)). *Inference:* take a spoken number only for a form that collects data for a new record, such as an email address. If the link can read or change an account, treat it like a one-time code: send it only to a contact on file after the caller is verified, and never to a number given during this call ([security guide](../../voice-agent-security/references/security-guide.md#verify-in-steps-in-the-backend)).
- *Inference:* make the link short-lived and single-use, tie it to this call on your server, and keep names, numbers and codes out of the URL. A link is a credential until it is used.
- Treat what comes back from the form as unverified input, the same as a spoken value: validate it in code ([validate and store](validate-and-store.md)).

## Read the value back

1. **Read from the stored value, not from memory.** Code turns the canonical value (an E.164 number, a code, an ISO date) into the words the voice will say. The model does not retype it. The read-back also shows the caller anything your normalization changed.
2. **Pick explicit or implicit confirmation by cost.** Google's guidance uses explicit confirmation of parameters only when a misunderstanding costs a lot, and gives "names, addresses, texts to be shared" as examples. It uses implicit confirmation most of the time: you use the value in your next sentence, and the caller can still correct it ([Google confirmations](https://developers.google.com/assistant/conversation-design/confirmations)).
3. **Say it in groups, with a pause between groups.** Twilio's `<Say>` page says commas and periods are read as natural pauses ([Twilio](https://www.twilio.com/docs/voice/twiml/say)), and Cartesia's prompting guide says the same about punctuation ([Cartesia](https://docs.cartesia.ai/build-with-cartesia/capability-guides/prompting-tips.md)). Put the question after the value, and stop.
4. **Wait for the answer.** A yes, a no or a correction. *Inference:* silence is not a yes. Repeat the read-back once, then change channel.
5. **Let the caller cut in.** A caller who hears a wrong digit will interrupt. Treat a cut-in as "not confirmed" and parse the speech as a correction. Never count speech heard during the read-back as a yes. Check how your stack reports input while the agent is speaking. In Twilio's ConversationRelay, `reportInputDuringAgentSpeech` defaults to `none` (it was `any` before May 2025). `interruptible` controls whether caller input stops playback. `ignoreBackchannel` (default `false`) can filter "yeah", "uh-huh" and "okay" ([ConversationRelay](https://www.twilio.com/docs/voice/twiml/connect/conversationrelay)). The `interrupt` message says how much of the text was played before the caller cut in ([message reference](https://www.twilio.com/docs/voice/conversationrelay/websocket-messages)). *Inference:* a confirmation covers only what the caller heard.
6. **Bind the confirmation to the value.** "Yes" confirms the value just read, for this field. If the value changes after the yes (a late correction, a retry), confirm again.
7. **Never read on-file data to an unverified caller.** Read back what the caller just said. Let them say a new value, and compare it in code ([security guide](../../voice-agent-security/references/security-guide.md#social-engineering-by-voice)).
8. **Do not read back cards, PINs or ID numbers.** They are not in the transcript to begin with ([privacy](../SKILL.md#keep-sensitive-data-off-the-model-path)).

| Field | Confirm | Why |
| --- | --- | --- |
| Phone, email, name, address, code | Explicitly: read back, wait for yes, no or a correction | Wrong values cost a failed callback, a lost account or a wrong delivery |
| A choice from your own list (a slot, a service) | Implicitly: use it in the next sentence ("Tuesday at two. What name is it under?") | The caller can still say "no, Wednesday" |
| An action that is hard to undo (cancel a booking, pay, delete) | Explicitly, with the exact values in the read-back | Google lists actions that are difficult to undo as needing explicit confirmation |
| A global command to the agent, such as "stop" | Act, then say you did. If "cancel" could mean a booking and not the flow, ask which | Google lists global commands like "stop" and "cancel" as needing no confirmation, and the [compliance skill](../../voice-phone-compliance/SKILL.md) says to honor a stop request at once |

*Inference:* with implicit confirmation, hold the write until the end of the flow or until an explicit confirmation, so a later "no" does not leave a wrong value already saved.

## Make the voice say it correctly

The job is to have every digit and letter said as you meant it, in groups, with pauses. Start by building the spoken form in code and sending plain words and commas: `python scripts/readback.py phone "+14155550123"` prints `plus one, four one five, five five five, zero one two three`. [`readback.py`](../scripts/readback.py) does the same for codes (with the spelling alphabet) and, letter by letter, for email addresses. Some providers recommend the conventional written form for phone numbers and similar sequences instead (see the Cartesia row). *Inference:* plain words and commas do not depend on any provider's markup or normalization, which is why they are the place to start. Keep the spoken form in one function, so you can change it for one voice without touching the flow.

Markup and built-in normalization differ by provider, by voice and by mode. Some pages document behavior that surprises callers: Google's `telephone` speaks zero as the letter O by default, and Polly's `characters` is not supported on neural voices. Test the exact text with the exact voice you ship.

| Provider | What the page says |
| --- | --- |
| [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech/docs/ssml) | `say-as` values include `telephone`, `verbatim` or `spell-out`, `characters`, `cardinal`, `ordinal`, `currency`, `time`, `unit` and `date` with a `format`. For `telephone`, zero is spoken as the letter O unless you set `google:style='zero-as-zero'`, which works only in English locales |
| [Google Chirp 3: HD](https://cloud.google.com/text-to-speech/docs/chirp3-hd) | SSML is Preview. It is supported for synchronous requests and not for streaming requests |
| [Microsoft Azure Speech](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-pronunciation) | `characters` and `spell-out` work in all text-to-speech locales. `alphanumeric` with `format="spell"` pauses at a hyphen ("AB-CD-EF"). Other `say-as` values work in all locales of a listed set of languages. In `<say-as interpret-as="date">`, `10-12-2016` is spoken as October twelfth when no format is given and as December tenth with `format="dmy"` |
| [Amazon Polly](https://docs.aws.amazon.com/polly/latest/dg/say-as-tag.html) | `say-as` works with generative, long-form, neural and standard engines. `characters` and `spell-out` are not supported on neural voices: the sentence is synthesized with the standard voice and still billed as neural. `digits` says each digit. `telephone` is documented for 7-digit and 10-digit numbers and is not in every language. UK English says repeated digits as "double five" and "triple four" |
| Twilio `<Say>` ([usage](https://www.twilio.com/docs/voice/twiml/say), [voices and SSML](https://www.twilio.com/docs/voice/twiml/say/text-speech)) | `say-as` is supported for Amazon and Google voices, and not for ElevenLabs voices, where the listed tags are `<break>` and `<phoneme>`. Digits written without spaces are read as one number (`12345` as "twelve thousand, three hundred forty-five"), and digits separated by spaces are read one by one. Without `say-as`, `4155551212` is read as "four billion, one hundred fifty-five million" and so on. With `interpret-as="telephone"` it is read digit by digit |
| [Cartesia Sonic](https://docs.cartesia.ai/build-with-cartesia/capability-guides/ssml-tags.md) | `<spell>` reads codes, IDs and names character by character. The page says to avoid other punctuation inside the tag and not to chain `<spell>` with `<break>`. For phone numbers and card-like sequences it says to write a plain string and let text normalization group them, and to use `<spell>` only for a strict character-by-character read-out. The [prompting tips](https://docs.cartesia.ai/build-with-cartesia/capability-guides/prompting-tips.md), written for Sonic 3.5, list space- and comma-delimited characters as alternatives, call pre-normalizing a fallback for edge cases, and say to keep numbers and codes inside a full sentence. Their starter prompt says NATO words help the listener tell letters apart. The [Sonic 3.6 page](https://docs.cartesia.ai/build-with-cartesia/tts-models/latest.md) says it is generally available and fully backwards compatible with 3.5 |
| [ElevenLabs](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) | Eleven v4 and v3 do not support SSML break tags, and the [v4 page](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4) says SSML is not supported. The pages disagree on normalization, see below. The best-practices page shows Flash v2.5 reading "$1,000,000" as "one thousand thousand dollars" and tells you to expand numbers, phone numbers and symbols into words in your own text or in the LLM prompt |
| [OpenAI text to speech](https://developers.openai.com/api/docs/guides/text-to-speech) | The page documents an `instructions` field for delivery, such as tone. It does not document SSML or number normalization, so send plain words |

**ElevenLabs normalization, four statements.**

- The [best-practices page](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) says normalization is enabled by default for all models.
- The [models page](https://elevenlabs.io/docs/overview/models) says it is disabled by default for Flash v2.5 to maintain low latency, and that Enterprise customers can turn it on for v2.5 models by setting `apply_text_normalization` to "on". For low-latency or Agents Platform applications it says the best practice is to have your LLM normalize the text before it reaches the voice, or to use that parameter (Enterprise plans only for v2.5 models).
- The [API reference](https://elevenlabs.io/docs/api-reference/text-to-speech/convert) shows `apply_text_normalization` with a default of `auto`.
- Twilio's [ConversationRelay page](https://www.twilio.com/docs/voice/twiml/connect/conversationrelay) sets `elevenlabsTextNormalization` to `off` by default and says `auto` has the same effect as `off` there.

They cannot all hold in every setting, so do not depend on ElevenLabs normalization. Normalize in your own text. *Inference:* for a captured value, build that text in code and not with the LLM, so the model never retypes the digits.

Spoken-form rules to start from. A provider can advise otherwise, so test them with the shipped voice:

- Digits as words in groups: "zero" for 0. Do not send "oh" for digits. Some voices read an unspaced digit string as one number (Twilio's page shows this), so do not send one until you have heard the shipped voice read it.
- Letters that are easy to confuse are said with the spelling alphabet. Group a code in fours as a starting point, and tune to your code length.
- Email punctuation is said as "dot", "dash", "underscore" and "at".
- Dates in words ("Tuesday, March fourteenth"), times with AM or PM, amounts in words.
- No provider markup unless you have heard the shipped voice say that exact text, and you have a plain-text fallback for when the markup is ignored, read aloud or fails the request. Twilio's page says an unsupported SSML tag might fail the `<Say>`.

*Inference:* test the spoken form end to end. Synthesize the read-back text with the shipped voice, run the audio through a phone-quality path and your recognizer, and assert that the digits you meant come out ([test fixtures](test-fixtures.md)).

## Keypad input by framework

| Framework | How digits arrive | Settings that matter |
| --- | --- | --- |
| [Twilio `<Gather>`](https://www.twilio.com/docs/voice/twiml/gather) | The digits are posted to your `action` URL in `Digits`, without the finish key | `input` is `dtmf` by default and can be `dtmf speech`. `numDigits` submits when that many digits are in. `finishOnKey` defaults to `#`, and an empty string waits for `timeout`. With `dtmf speech`, the first input wins and speech first makes Twilio ignore `finishOnKey`. Speech runs up to 60 seconds |
| [Twilio ConversationRelay](https://www.twilio.com/docs/voice/twiml/connect/conversationrelay) | One `{"type":"dtmf","digit":"1"}` message per keypress ([messages](https://www.twilio.com/docs/voice/conversationrelay/websocket-messages)) | `dtmfDetection="true"` turns the messages on. `reportInputDuringAgentSpeech` is `none` by default, so digits keyed while the agent talks are not reported unless you set `dtmf` or `any`. Your code joins the digits and decides when the entry ends |
| [Twilio Media Streams](https://www.twilio.com/docs/voice/media-streams) | `{"event":"dtmf","dtmf":{"track":"inbound_track","digit":"1"}}` ([messages](https://www.twilio.com/docs/voice/media-streams/websocket-messages)) | Only on bidirectional streams, and only in the inbound direction. Unidirectional streams do not support DTMF |
| [LiveKit Agents](https://docs.livekit.io/agents/prebuilt/tasks/get-dtmf/) (Python, beta) | `GetDtmfTask` returns `user_input`, a string of digits. It takes keypad or spoken digits. SIP DTMF is sent as `telephone-event/8000` ([LiveKit DTMF](https://docs.livekit.io/telephony/features/dtmf/)) | `num_digits`, `ask_for_confirmation` (default `False`), `dtmf_input_timeout` (default 4.0 seconds per digit) and `dtmf_stop_event` (default `#`) |
| [Pipecat](https://docs.pipecat.ai/api-reference/server/utilities/dtmf-aggregator.md) | `DTMFAggregator` joins keypresses into one `TranscriptionFrame`, prefixed "DTMF: ", for the LLM | `timeout` (default 2.0 seconds) and `termination_digit` (default `#`) |

Two rules for keypad capture:

1. **Say the length or the end key, and set a timeout.** "Enter the ten digits, then press pound." Without one, the system does not know the entry is over.
2. **Decide where the digits go before you build.** Pipecat's aggregator is built to turn keypresses into text for the language model, and LiveKit's `GetDtmfTask` example returns the digits from a function tool to the model. Keypad digits are therefore not private by default. For card numbers and PINs, send the keypresses to the payment or verification service and not to the model ([privacy](../SKILL.md#keep-sensitive-data-off-the-model-path)).

## Sources

Retrieved 2026-09-30 by fetching each page. "Shown" is a date printed on the page, when there was one. A retrieval date is not a publication date. Context7 used `/websites/elevenlabs_io` for the ElevenLabs normalization question. Every page cited here was retrieved directly.

| Source | Supports | Shown |
| --- | --- | --- |
| [Google Conversation Design: Confirmations](https://developers.google.com/assistant/conversation-design/confirmations) | Explicit and implicit confirmation, one-step corrections. The page belongs to Conversational Actions, which Google deprecated on 13 June 2023, so it is used for the pattern only | Updated 2024-09-18 |
| [Google Cloud TTS SSML](https://cloud.google.com/text-to-speech/docs/ssml) | `say-as` values, `telephone` zero handling | Updated 2026-09-24 |
| [Google Chirp 3: HD](https://cloud.google.com/text-to-speech/docs/chirp3-hd) | SSML Preview, synchronous only | Updated 2026-09-24 |
| [Azure say-as](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-pronunciation) | `say-as` values, locales, date example | Updated 2026-02-25 |
| [Amazon Polly say-as](https://docs.aws.amazon.com/polly/latest/dg/say-as-tag.html) | Engine support, `characters` limit on neural voices, `digits`, `telephone` | none shown |
| Twilio [Say](https://www.twilio.com/docs/voice/twiml/say), [Say text-to-speech](https://www.twilio.com/docs/voice/twiml/say/text-speech) | Pauses, digit grouping, `say-as` support by voice provider, phone number example, unsupported tags | none shown |
| [Cartesia SSML tags](https://docs.cartesia.ai/build-with-cartesia/capability-guides/ssml-tags.md), [prompting tips](https://docs.cartesia.ai/build-with-cartesia/capability-guides/prompting-tips.md), [Sonic 3.6](https://docs.cartesia.ai/build-with-cartesia/tts-models/latest.md) | `<spell>`, plain written forms, pre-normalizing as a fallback, pauses, current model | none shown |
| ElevenLabs [best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices), [models](https://elevenlabs.io/docs/overview/models), [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4), [API reference](https://elevenlabs.io/docs/api-reference/text-to-speech/convert) | SSML support, number reading, normalization statements | none shown |
| [OpenAI text to speech](https://developers.openai.com/api/docs/guides/text-to-speech) | `instructions` field | none shown |
| Twilio [Gather](https://www.twilio.com/docs/voice/twiml/gather), [ConversationRelay](https://www.twilio.com/docs/voice/twiml/connect/conversationrelay), [ConversationRelay messages](https://www.twilio.com/docs/voice/conversationrelay/websocket-messages), [Media Streams](https://www.twilio.com/docs/voice/media-streams), [Media Streams messages](https://www.twilio.com/docs/voice/media-streams/websocket-messages) | Keypad input and interruption settings | none shown |
| LiveKit [GetDtmfTask](https://docs.livekit.io/agents/prebuilt/tasks/get-dtmf/), [DTMF](https://docs.livekit.io/telephony/features/dtmf/) | `GetDtmfTask` parameters, SIP DTMF | none shown (the pages print a render time only) |
| [Pipecat DTMFAggregator](https://docs.pipecat.ai/api-reference/server/utilities/dtmf-aggregator.md) | Aggregation defaults | none shown |

No provider requests, audio tests or accuracy measurements were run to write this file. The script self-test is the only code that ran.
