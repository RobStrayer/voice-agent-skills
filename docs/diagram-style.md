# Diagram style

Every figure in this repo is a hand-written SVG in [`assets/diagrams/`](../assets/diagrams/)
(or a skill's own `assets/` folder). The SVG is the source: open it in any editor,
change the text, and save. No build step and no export step.

![Reference figure](../assets/diagrams/voice-agent-anatomy.svg)

## Rules that make them work on GitHub

GitHub shows README images through an `<img>` tag. That means **no scripts, no
web fonts, no external files, and no hover**. What does work: inline `<style>`,
CSS custom properties, and `@media (prefers-color-scheme: dark)`.

- **One file, both themes.** Each SVG draws its own rounded background card and
  switches its colour variables in a dark-mode media query. If a reader's GitHub
  theme and OS theme disagree, they see a light card on a dark page (or the
  reverse). It is still readable.
- **System fonts only.** Use GitHub's own stack for text and its monospace stack
  for code-like labels. Both are in the style block below.
- **Readable at README width.** The README column is about 880 px wide, so a
  1080-wide figure shrinks to about 80%. Keep text at 14 px or more (15 px or more
  for body copy). Titles are 27 px, card titles 20 px, item names 16 px.
- **Accessible.** Always add `role="img"`, a `<title>`, and a `<desc>` that says
  what the figure shows in words. Colour never carries meaning alone: every
  coloured thing also has a text label.
- **Honest.** No invented numbers. A figure with timings or prices labels itself
  as illustrative and cites its source in the surrounding Markdown.
- **No logos.** Providers appear as plain text names.

## Colour roles

The three stages of a voice agent each get one hue. Infrastructure is neutral.
The set passes the colour-vision checks in the `dataviz` validator (all pairs,
both modes).

| Role | Meaning | Light | Dark | Tint light / dark |
| --- | --- | --- | --- | --- |
| `listen` | Capture, VAD, turn detection, speech-to-text | `#0b7a53` | `#2fb784` | `#dff3ea` / `#12301f` |
| `think` | Language model, tools, state, logic | `#4a3aa7` | `#a29af0` | `#eae8f8` / `#262045` |
| `speak` | Text-to-speech, playback | `#b3441a` | `#ec7a45` | `#fbe9e0` / `#3a2014` |
| `net` | Phone network, WebRTC, servers, infrastructure | `#57606a` | `#8b949e` | `#eaeef2` / `#21262d` |
| `warn` | Risk, interruption, unknown outcome | `#8a5c00` | `#d29922` | `#fff8c5` / `#2e2508` |
| `bad` | Failure | `#cf222e` | `#f85149` | `#ffebe9` / `#3a1618` |
| `good` | Confirmed outcome | `#1a7f37` | `#3fb950` | `#dafbe1` / `#12301a` |

Surfaces and ink follow GitHub's Primer colours: background `#f6f8fa` / `#0d1117`,
cards `#ffffff` / `#161b22`, borders `#d0d7de` / `#30363d`, text `#1f2328` / `#e6edf3`,
secondary text `#59636e` / `#9198a1`.

## Starting style block

Copy this into a new figure and delete the classes you don't use.

```css
svg{--bg:#f6f8fa;--card:#fff;--line:#d0d7de;--ink:#1f2328;--ink2:#59636e;--net:#57606a;--net-t:#eaeef2;--listen:#0b7a53;--listen-t:#dff3ea;--think:#4a3aa7;--think-t:#eae8f8;--speak:#b3441a;--speak-t:#fbe9e0;--warn:#8a5c00;--warn-t:#fff8c5;--bad:#cf222e;--bad-t:#ffebe9;--good:#1a7f37;--good-t:#dafbe1}
@media (prefers-color-scheme:dark){svg{--bg:#0d1117;--card:#161b22;--line:#30363d;--ink:#e6edf3;--ink2:#9198a1;--net:#8b949e;--net-t:#21262d;--listen:#2fb784;--listen-t:#12301f;--think:#a29af0;--think-t:#262045;--speak:#ec7a45;--speak-t:#3a2014;--warn:#d29922;--warn-t:#2e2508;--bad:#f85149;--bad-t:#3a1618;--good:#3fb950;--good-t:#12301a}}
text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;fill:var(--ink)}
.mono{font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace}
.bg{fill:var(--bg);stroke:var(--line)}.card{fill:var(--card);stroke:var(--line)}
.h1{font-size:27px;font-weight:700}.sub{font-size:16px;fill:var(--ink2)}
.eyebrow{font-size:14px;font-weight:700;letter-spacing:1.4px}.h2{font-size:20px;font-weight:700}
.name{font-size:16px;font-weight:600}.desc{font-size:15px;fill:var(--ink2)}
```

## Anatomy of a figure

Copy the structure of [`voice-agent-anatomy.svg`](../assets/diagrams/voice-agent-anatomy.svg):

1. Background card: `<rect class="bg" rx="16">` covering the whole viewBox.
2. Title (`.h1`) and one-line subtitle (`.sub`) at the top left, 32 px in.
3. Content cards: `rx="14"`, a 5 px coloured bar on top for a stage, an icon in
   a tinted circle, a small uppercase eyebrow in the stage colour, a card title in ink.
4. Arrows: 2 px `--ink2` lines with a filled triangle marker. Use a dashed
   `--warn` line for interruptions and other exceptions.
5. Labels on arrows in the monospace style, 14 px.

Icons are simple line drawings on a 24-unit grid (2 px stroke, round caps),
drawn for this repo. Reuse the microphone, sparkle, speaker, person and phone
shapes from existing figures.

## Checking a figure

Open the SVG in a browser with the OS set to light, then dark. Check that nothing
overflows a card, that no text is under 14 px, and that each colour has a label.
Figures describe concepts, not any provider's event schema or a benchmark.
