# Maintaining the collection

Reviewed: 2026-09-30 UTC.

Keep source links current, repair stale guidance, and add skills that help with
real voice engineering work. A daily review should produce a change only when
there is useful new evidence. Stars alone are not a reason to add an entry.

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
   concurrent work. Confirm the target repository is still private before pushing
   under the current private-maintenance authorization.
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

## Checks before publication

Run from the repository root:

```sh
python scripts/verify.py
python scripts/test_verify.py
git diff --check
```

The verifier checks snapshot hashes and retained licenses, skill names and local
Markdown paths, source records, Python syntax, and a bounded set of credential
patterns. Its regression check must reject tampered source content. Review new
links against the live original sources; a local link check cannot establish that
an external API or skill still works.

Inspect the changed text for credentials, private account data, local usernames,
internal URLs, recordings, and copied project instructions. Pattern matching is
only part of that review. Keep private research artifacts outside the repository.

Publish validated, task-owned changes with a descriptive commit. Reconcile a
concurrent remote update before pushing; never force-push over other work. After
publication, read back the remote commit and private visibility. Record any
unverified source or blocked operation precisely.

## Autonomous daily maintenance

The maintainer has authorized daily research, validated content updates, commits,
and pushes to this private repository. Routine maintenance does not require a new
approval. This authority does not cover making the repository public, changing
credentials or account permissions, paid calls, live provider changes, or unrelated
repositories.

The scheduled review runs at 09:00 America/New_York in the maintainer's Codex
environment. Its authentication stays in the local credential store; no token or
account configuration belongs in this repository. The schedule and credentials are
external to the checkout and are not installed by cloning it.

Notify the maintainer when useful content changes, a material deprecation affects
the collection, or an authentication or policy failure blocks an update. An
unchanged review needs no notification or date-only commit.
