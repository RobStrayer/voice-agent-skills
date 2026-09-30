# Diagram style and source files

Updated **2026-09-30 UTC**. The diagrams use a medium stone-gray surface, charcoal
text, and muted teal emphasis. The fixed palette is intended to remain readable
inside both light and dark documentation pages. Labels and line styles carry
meaning independently of color.

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

Typography follows Diagram Design: Instrument Serif for figure titles, Geist
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

The front page uses two simpler assets at the same 960-pixel width: a 304-pixel
editorial cover and a 620-pixel architecture comparison. The cover waveform is an
original illustration, not measured audio. The comparison uses larger 16-pixel
node names and 12-pixel supporting labels. It introduces three speech patterns;
the full guide supplies transport, hosting, authority, and recovery decisions.

## Figure library

| Figure | Editable source | Portable image |
| --- | --- | --- |
| Field guide cover | [HTML](../assets/voice-field-guide.html) | [SVG](../assets/voice-field-guide.svg) |
| Three speech architecture patterns | [HTML](../skills/foundations/voice-stack-selection/assets/speech-architectures.html) | [SVG](../skills/foundations/voice-stack-selection/assets/speech-architectures.svg) |
| Audio, call control, and business state | [HTML](../skills/foundations/voice-stack-selection/assets/voice-system-map.html) | [SVG](../skills/foundations/voice-stack-selection/assets/voice-system-map.svg) |
| Turn commitment and interruption | [HTML](../skills/foundations/voice-turn-taking/assets/turn-controller.html) | [SVG](../skills/foundations/voice-turn-taking/assets/turn-controller.svg) |
| Echo reference and audio processing | [HTML](../skills/foundations/voice-audio-frontends/assets/echo-processing.html) | [SVG](../skills/foundations/voice-audio-frontends/assets/echo-processing.svg) |
| Interrupted speech and pending actions | [HTML](../skills/foundations/voice-conversation-design/assets/interrupted-action.html) | [SVG](../skills/foundations/voice-conversation-design/assets/interrupted-action.svg) |
| Human handoff and failure recovery | [HTML](../skills/foundations/voice-call-reliability/assets/recoverable-handoff.html) | [SVG](../skills/foundations/voice-call-reliability/assets/recoverable-handoff.svg) |
