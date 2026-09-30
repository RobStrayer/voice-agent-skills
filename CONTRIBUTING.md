# Contributing

Bring a skill that helps someone build, operate, or evaluate a voice AI agent.
A smaller, useful collection beats a larger collection of overlapping prompts.

## Quick start

1. Fork the repo and create a branch.
2. Make your change. For a typo or broken link, that's all.
3. Run `python scripts/verify.py` and `python scripts/test_verify.py`.
4. Open a pull request and fill in the checklist.

By contributing you agree that your original work is released under the repo's
[MIT license](LICENSE).

## Add a skill

1. Check the [catalog](docs/catalog.md) for an existing skill that covers the task.
2. Put the complete skill folder under `skills/<provider>/<name>/`. Keep its
   `SKILL.md`, required references, scripts, and assets together.
3. Provide a precise trigger in the frontmatter description. State prerequisites
   and any tool, service, runtime, or platform dependency.
4. For upstream material, record the original repository, file path, immutable
   commit, license, and file checksums in `sources.json`. Preserve upstream notices.
   Public visibility and stars alone do not establish redistribution permission.
   Link the original default-branch source as the primary catalog/README entry;
   label any bundled copy as a dated snapshot. Skip unverified local-only variants.
5. Review scripts and hooks before including them. Never include account data,
   recordings, credentials, internal URLs, or project-specific operational notes.
6. For original guidance, add a review date and cite the relevant official pages
   beside changing technical claims. Check the provider's current documentation and
   the canonical page, especially for deprecations or contradictory examples. A
   retrieval date is not the provider's publication date.
7. Update the catalog and relevant README entry. Run `python scripts/verify.py`
   and `python scripts/test_verify.py`.

## Add a resource

Prefer official documentation, maintained repositories, reproducible evaluations,
and useful engineering writeups. Explain what the link helps someone do. Separate
frameworks, models, tools, skills, and community discussions. Record the retrieval
date for changing facts such as stars and licenses in `resources.json`.

Community recommendations can suggest candidates. Verify technical claims against
the original project. Avoid blanket rankings or incomparable benchmark scores.

Link-only entries are welcome when a skill is useful but copying it would add
maintenance burden or its redistribution terms are unclear. Link the actual
original skill and record its repository, observed revision, review date, purpose,
and material caveats. Distinguish an official provider pack from a community pack.

## Review expectations

New and substantially changed skills should get a realistic task review. Check
whether the skill preserves the user's scope, identifies necessary prerequisites,
and produces a useful result without assuming permission to spend, dial, record,
deploy, or modify a live account. Structure validation does not prove behavior.

Keep third-party snapshots unchanged where possible. Record any necessary local
patch and its reason. Refresh deliberately at a new pinned commit, review the diff,
and rerun the checks. Do not silently replace the collection with upstream latest.

Follow the [maintenance procedure](docs/maintenance.md) when refreshing several
sources together. Avoid date-only churn: a new review date should reflect a real
source check, and a content update should describe what changed.
