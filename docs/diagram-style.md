# Diagram style and source files

Updated **2026-09-30 UTC**. The README uses compact teaching diagrams with a cool
surface and a consistent semantic palette. Blue follows the speech path, teal
marks conversation control or established outcomes, and amber marks actions or
uncertainty. Text and line styles carry the meaning independently of color.

The front page is a skills and learning directory. Graphics explain a specific
engineering idea; they do not serve as decorative banners. Keep titles brief,
avoid repeating the surrounding section heading, and fit the canvas around the
diagram. The six front-page figures are 306 to 472 pixels tall on a 960-pixel-wide
canvas, with 20-pixel node names and 16 to 18-pixel supporting labels.

| README token | Value | Role |
| --- | --- | --- |
| Surface | `#eef3f8` | Compact figure background |
| Ink | `#23344b` | Main labels |
| Muted | `#50627a` | Annotations and routes |
| Blue / tint | `#365f9c` / `#dce8f8` | Speech and media |
| Teal / tint | `#176d6a` / `#d9efeb` | Control and established outcomes |
| Amber / tint | `#815313` / `#f5e8ce` | Actions and unresolved outcomes |

The portable exports use Geist and Geist Mono with system sans-serif and Consolas
fallbacks. No font download is required. Embedded images keep their own contrast
on light and dark GitHub pages. Native explanations and full-size links retain
the information when a phone screen makes a detailed image too small.

### Detailed guide figures

Earlier guide illustrations retain their medium stone surface and muted teal
palette. They remain available within the relevant skill folders. The table
below documents those older assets, rather than imposing their skin on the README.

| Token | Value | Role |
| --- | --- | --- |
| Paper | `#b9beb8` | Diagram surface |
| Paper 2 | `#d2d6cf` | Neutral node fill |
| Ink | `#202823` | Primary text |
| Strong ink | `#18201c` | Highest-contrast text |
| Muted | `#3e4a42` | Secondary text and connectors |
| Soft | `#414e44` | Source and boundary annotations |
| Rule | `rgba(32,40,35,0.18)` | Hairlines |
| Solid rule | `#8e9b90` | Node and group outlines |
| Accent | `#2d6358` | One or two focal elements |
| Accent tint | `#c9d9cf` | Focal node fill |
| Link | `#3f5f54` | External request path |

The earlier guide typography follows Diagram Design: Instrument Serif for figure titles, Geist
for names, and Geist Mono for technical labels. Arial, Georgia, and system
monospace fallbacks keep exports usable when a host blocks remote fonts. GitHub
image rendering may substitute those fallbacks. Detailed diagrams use a 960 × 600 viewBox;
their HTML has a local horizontal scroller on narrow screens and a print rule
that fits the complete figure on the page.

Exports also declare their intrinsic size so an image host does not treat
them as small thumbnails. The primary and secondary text colors exceed 4.5:1
contrast against the stone surface; the light and dark surrounds do not change
that internal contrast. Open a figure at full size for its smaller technical labels.

HTML is the editable source, with an inline accessible SVG. The adjacent SVG is
exported from that HTML using Diagram Design's `export_svg.py`, then checked as
XML and inspected visually. Edit and export them together. Keep each skill's
figures inside its own `assets/` folder so a complete skill installation retains
its supporting material.

The figures describe conceptual responsibilities and application policies. They
are not provider event specifications, benchmark results, or a claim that one
deployment has implemented those behaviors. Follow the dated references in the
associated guide when turning a diagram into code.

The front page uses six teaching figures with different visual forms: a speech
cascade, a conversational score, an audio cutaway, an action ledger, a call tree,
and a timing chart. Native text beside each explains the result and links to
skills for that part of the system. The earlier three-pattern comparison remains
available in the architecture guide. The original waveform cover is retained as
an earlier asset, not used as the front-page cover.

The front page has no decorative cover. Its title, skill directory, and
navigation are native Markdown. All six teaching figures are original repository
illustrations covered by the root MIT license; no provider logo, stock image,
private call record, or external artwork was used.

### Timing example

The [timing chart](../assets/atlas-latency.svg) uses an explicitly fabricated
trace on one assumed relative clock. The caller stops at 0 ms, the turn commits
at 260 ms, a speakable phrase becomes ready at 720 ms, synthesis produces its
first chunk at 900 ms, that chunk arrives at 950 ms, playback begins at 1,060 ms,
and useful speech begins at 1,120 ms. These values are neither measurements nor
recommended targets. The continuing bars illustrate overlap; adding their
lengths would not recover either response time. First token and first speakable
phrase are different events.

The cascade and call tree are hypothetical application designs. The call tree
assumes a supported warm handoff that can retain the caller when the destination
is unavailable. Other telephony mechanisms need their own recovery contract.
The compact figures keep the same engineering distinctions while removing the
earlier oversized titles and large background fields.

## Figure library

| Figure | Editable source | Portable image |
| --- | --- | --- |
| Streaming speech cascade | [HTML](../assets/atlas-cascade.html) | [SVG](../assets/atlas-cascade.svg) |
| Overlapping stages and audible timing | [HTML](../assets/atlas-latency.html) | [SVG](../assets/atlas-latency.svg) |
| Call routing and recovery | [HTML](../assets/atlas-call-tree.html) | [SVG](../assets/atlas-call-tree.svg) |
| Conversational score | [HTML](../assets/atlas/conversation-score.html) | [SVG](../assets/atlas/conversation-score.svg) |
| Acoustic capture cutaway | [HTML](../assets/atlas/audio-cutaway.html) | [SVG](../assets/atlas/audio-cutaway.svg) |
| Correction and action reconciliation | [HTML](../assets/atlas/action-reconciliation.html) | [SVG](../assets/atlas/action-reconciliation.svg) |
| Field guide cover | [HTML](../assets/voice-field-guide.html) | [SVG](../assets/voice-field-guide.svg) |
| Three speech architecture patterns | [HTML](../skills/foundations/voice-stack-selection/assets/speech-architectures.html) | [SVG](../skills/foundations/voice-stack-selection/assets/speech-architectures.svg) |
| Audio, call control, and business state | [HTML](../skills/foundations/voice-stack-selection/assets/voice-system-map.html) | [SVG](../skills/foundations/voice-stack-selection/assets/voice-system-map.svg) |
| Turn commitment and interruption | [HTML](../skills/foundations/voice-turn-taking/assets/turn-controller.html) | [SVG](../skills/foundations/voice-turn-taking/assets/turn-controller.svg) |
| Echo reference and audio processing | [HTML](../skills/foundations/voice-audio-frontends/assets/echo-processing.html) | [SVG](../skills/foundations/voice-audio-frontends/assets/echo-processing.svg) |
| Interrupted speech and pending actions | [HTML](../skills/foundations/voice-conversation-design/assets/interrupted-action.html) | [SVG](../skills/foundations/voice-conversation-design/assets/interrupted-action.svg) |
| Human handoff and failure recovery | [HTML](../skills/foundations/voice-call-reliability/assets/recoverable-handoff.html) | [SVG](../skills/foundations/voice-call-reliability/assets/recoverable-handoff.svg) |
