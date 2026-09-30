# Security policy

This repo is documentation, skills and two small Python scripts. The main risks
are a skill that tells a coding agent to do something unsafe, a script with a
bug, or a secret that slipped into a file.

## Report a problem privately

Use GitHub's private reporting: open the **Security** tab of this repo and choose
**Report a vulnerability**. Please don't open a public issue for security problems.

Include the file path, what could go wrong, and how to reproduce it if you can.
You should get a reply within a week.

## What's in scope

- Original skills in `skills/foundations/` and the scripts in `scripts/` and in
  any skill's `scripts/` folder.
- Instructions in any skill here that could lead an agent to leak data, spend
  money, place calls, or change live accounts without the user asking.
- Credentials, private data or internal URLs committed to this repo.

## Third-party skills

Bundled provider skills are dated copies of other people's work, and the linked
index points to skills we don't host. Report problems in those to the original
project (each entry links its source). Tell us too if we should stop bundling or
linking it.
