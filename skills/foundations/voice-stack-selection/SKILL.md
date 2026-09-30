---
name: voice-stack-selection
description: Choose a voice AI architecture, speech engine, transport, and hosting model from real constraints. Use when comparing platforms, planning browser or phone agents, estimating total cost, or migrating an existing stack.
license: MIT
---

# Voice stack selection

Recommend the smallest architecture that meets the user's task and operating constraints.
Read [the architecture guide](references/architecture-guide.md) before recommending a stack.
It covers ownership, media paths, interruptions, capacity, cost, a worksheet, and a proof of concept.

Start with channel, languages, tool actions, traffic, deployment limits, budget, and caller
experience. Ask only for missing facts that change the decision; label other assumptions.

Compare two or three complete call paths. Keep speech engine, orchestration, transport,
hosting, and business state separate. A provider name alone does not specify an architecture.

Use Context7 to resolve the relevant library and query current official documentation,
then open the primary sources. Check installed SDK versions and the exact integration.
Record review dates and source URLs. An example does not prove an untested combination
works or meets a latency target.

Deliver one recommendation, its deciding tradeoff, a condition for switching, the worksheet,
a media/control flow sketch, and the smallest useful comparison test. Separate documented
behavior, engineering recommendations, and unknowns. Reuse existing user authorization;
run paid or live tests only within that scope.
