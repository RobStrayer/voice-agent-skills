# Maintaining the collection

Reviewed: 2026-09-30 UTC.

Keep source links current, repair stale guidance, and add skills that help with
real voice engineering work. A review should produce a change only when there is
useful new evidence. Stars alone are not a reason to add an entry, and a review
with nothing new needs no date-only commit.

## What to review

| Source | Look for | Update when |
| --- | --- | --- |
| Original skill repositories in the catalogs | Renamed skills, changed instructions, new references, scripts, license or ownership changes | The selected skill changes or a new skill fills a useful gap. |
| Provider documentation and release notes | API/SDK migrations, deprecations, model availability, turn behavior, limits | A documented change affects an instruction, example, or architecture decision here. |
| Voice frameworks and models | Releases, maintenance status, new integrations, model-card terms | An entry's description or qualification needs correction. |
| Community discussions | Repeated failure reports, useful new tools, overlooked workflows | A lead can be verified from the original project. |

Resolve the relevant library in Context7 and query the specific feature being
checked. Open the canonical page behind the result. Indexes can lag a release or
return an older SDK example; compare the installed or cited version with the
current reference. If Context7 has no relevant source, use official documentation
directly and record the fallback. Never infer a provider's publication date from
the date you fetched a page.

## Review an update

1. Check local changes, the configured remote, and remote branch state. Preserve
   concurrent work. Confirm the target repository and branch before pushing.
2. Compare the new source with the last observed commit or review record. Read the
   changed instruction and its supporting material. Check whether a reference has
   moved, a default changed, or a model name become an alias for different behavior.
3. Write the smallest useful correction in original prose. Link the claim to its
   exact primary source. Quote only short passages when the precise wording matters;
   label comparisons and design recommendations as engineering judgment.
4. For a new skill, verify the original owner and actual skill path. Prefer a direct
   default-branch link. Avoid plugin mirrors, duplicate names presented as new work,
   generic skills with a voice keyword, and unfinished examples presented as ready.
5. Before copying or refreshing files, inspect their redistribution terms and any
   nested notices. Preserve complete skill folders and record every copied file in
   `sources.json`. Update a snapshot deliberately at an immutable commit. Linking a
   useful source does not require bundling it.
6. Update the affected page's review date and source metadata in `sources.json`,
   `linked-skills.json`, or `resources.json`, as appropriate. Leave unrelated star
   observations and snapshot dates intact. If an upstream URL moves, update its
   primary link while retaining the historical commit as evidence.
7. Read the final diff for accuracy, readable navigation, executable examples,
   private data, and unintended scope changes. Do not run installers, embedded
   telemetry commands, paid model requests, or example calls as part of research.

Keep the engineering handbook substantive as it grows. Turn taking, audio
frontends, recognition, synthesis, tools, telephony, and operations each need
direct navigation and practical guidance. A new source link does not replace a
worked case, failure analysis, or test worksheet. Keep a skill's required guides
inside its folder so installing it preserves those instructions. Check diagrams
against the revised state and event contracts, and keep each figure's alt text
and `<desc>` in step with the drawing.

Keep the README a front door, not the whole library. It opens with a banner, then
a "Start here" table, a short "how it works" figure, a "where to start" chart,
the install steps, the skill finder and the common problems. Longer explanations
live in guides under `docs/`: the [walkthrough](walkthrough.md) and the
[handbook](handbook.md) carry the implementation depth, and the skills carry the rest.

Figures follow [diagram style](diagram-style.md): one hand-written SVG per idea,
readable at README width, with a `<title>`, a `<desc>` and a plain-text explanation
beside it. Match the figure to the problem: a timeline for concurrent work, a call
tree for routing, an audio cutaway for echo. Review changed pages at their rendered
reading width. Synthetic traces must say that their values are illustrative, not
measurements or targets.

## Checks before publication

Run from the repository root:

```sh
python scripts/verify.py
python scripts/test_verify.py
git diff --check
```

The verifier checks snapshot hashes and retained licenses, skill names and local
Markdown paths, source records, Python syntax, and a bounded set of credential
patterns. Its regression check must reject tampered source content. The verify
check runs on every pull request and must pass before merging. Review new links
against the live original sources; a local link check cannot prove that an
external API or skill still works.

Inspect the changed text for credentials, private account data, local usernames,
internal URLs, recordings, and copied project instructions. Pattern matching is
only part of that review. Keep private research artifacts outside the repository.

Land validated, task-owned changes through a pull request from a topic branch
based on reconciled `origin/main`, with the verify check passing. Preserve
unrelated branches and edits. Reconcile a concurrent remote update before opening
the pull request; never force-push over other work. After the merge, read back the
remote commit. Record any unverified source or blocked operation precisely.
