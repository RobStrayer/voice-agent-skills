# Voice atlas figures

Created **2026-09-30 UTC**. These original illustrations explain engineering
decisions using synthetic examples. They contain no measured latency, audio
amplitude, production call records, or vendor performance comparisons.

| Figure | What it teaches | Canonical HTML | SVG |
| --- | --- | --- | --- |
| A pause, a continuation, a correction | A pause can belong to an unfinished turn; stopping old speech and resolving an external action have different lifetimes. | [Source](conversation-score.html) | [Image](conversation-score.svg) |
| Echo needs a reference | Endpoint echo cancellation needs its render reference; noise cleanup, VAD, and recognition have different jobs. | [Source](audio-cutaway.html) | [Image](audio-cutaway.svg) |
| Corrected intent and the original action | Preserve both records while reconciling an unknown outcome. | [Source](action-reconciliation.html) | [Image](action-reconciliation.svg) |

## Technical basis

The drawings summarize the repository's dated guides. Follow those guides to the
current original documentation before implementing a provider integration:

- [Turn-taking guide](../../skills/foundations/voice-turn-taking/references/turn-taking-guide.md): commitment, playback stopping, late output, and independently tracked tools.
- [Audio frontend guide](../../skills/foundations/voice-audio-frontends/references/audio-frontends-guide.md): render-reference placement, echo, optional enhancement, double-talk, and speech preservation.
- [Transactions and handoffs](../../skills/foundations/voice-conversation-design/references/transactions-and-handoffs.md): unknown outcomes, authoritative reconciliation, idempotency, and corrected intent.

An original key is usable only under the business API's documented idempotency support.
Application deduplication does not create exactly-once behavior for an external
API. An authoritative lookup may be unavailable; in that case the action remains
unknown and needs the configured recovery owner. The cutaway is a conceptual
endpoint path, not a requirement to add a second audio processor to an already
processed capture stream.

## Editing and portability

HTML is canonical, with an accessible inline SVG and a local horizontal scroller
on narrow screens. The adjacent SVG is exported with Diagram Design's packaged
`export_svg.py`; edit and export them together. A README embeds the SVG and should
keep a readable text explanation beside it for small screens.

The compact README figures use a cool surface, blue speech paths, teal control
and established outcomes, and amber actions or uncertainty. Node names are 20 px;
body labels are 18 px and supporting text is 16 px on a 960 px canvas. Geist and
Geist Mono have explicit system sans-serif and Consolas fallbacks. No remote font
loading is required. See the [complete figure library](../../docs/diagram-style.md)
for sources, palette, synthetic timing data, and portability notes.

These are original repository assets covered by the root [MIT license](../../LICENSE).
