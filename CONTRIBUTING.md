# Contributing

Bring a skill that helps someone build, operate, or evaluate a voice AI agent.
A smaller, useful collection beats a larger collection of overlapping prompts.

## Add a skill

1. Check the [catalog](docs/catalog.md) for an existing skill that covers the task.
2. Put the complete skill folder under `skills/<provider>/<name>/`. Keep its
   `SKILL.md`, required references, scripts, and assets together.
3. Provide a precise trigger in the frontmatter description. State prerequisites
   and any tool, service, runtime, or platform dependency.
4. For upstream material, record the original repository, file path, immutable
   commit, license, and file checksums in `sources.json`. Preserve upstream notices.
   Public visibility and stars alone do not establish redistribution permission.
5. Review scripts and hooks before including them. Never include account data,
   recordings, credentials, internal URLs, or project-specific operational notes.
6. Update the catalog and relevant README entry. Run `python scripts/verify.py`.

## Add a resource

Prefer official documentation, maintained repositories, reproducible evaluations,
and useful engineering writeups. Explain what the link helps someone do. Separate
frameworks, models, tools, skills, and community discussions. Record the retrieval
date for changing facts such as stars and licenses in `resources.json`.

Community recommendations can suggest candidates. Verify technical claims against
the original project. Avoid blanket rankings or incomparable benchmark scores.

## Review expectations

New and substantially changed skills should get a realistic task review. Check
whether the skill preserves the user's scope, identifies necessary prerequisites,
and produces a useful result without assuming permission to spend, dial, record,
deploy, or modify a live account. Structure validation does not prove behavior.

Keep third-party snapshots unchanged where possible. Record any necessary local
patch and its reason. Refresh deliberately at a new pinned commit, review the diff,
and rerun the checks. Do not silently replace the collection with upstream latest.
