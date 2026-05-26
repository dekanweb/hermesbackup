# GitHub backup: include session transcripts safely (push protection)

## Problem
Backing up Hermes `sessions/` can fail on GitHub with GH013 **push protection** when a session transcript contains secrets (common examples: Notion tokens like `ntn_…` or `secret_…`, OAuth tokens, API keys). GitHub blocks the push even if the repo is private.

## Recommended modes
1) Safer default: **exclude** `sessions/` from the mirrored backup.
2) Full-history backup: **include** `sessions/` but **scrub secrets during the mirror step** so the repo never receives raw tokens.

If the user explicitly wants “every conversation backed up”, choose mode (2).

## Scrubbing approach (mode 2)
During the filesystem mirror step:
- Detect when copying files under `sessions/`.
- Read as UTF-8 text (fallback to raw copy if decode fails).
- Apply regex substitutions to mask common token formats.
- Write scrubbed text to the destination snapshot.

Example patterns that have caused GH013 in practice:
- Notion integration token: `ntn_[A-Za-z0-9]{8,}`
- Notion legacy token: `secret_[A-Za-z0-9_\-]{8,}`

Also worth scrubbing:
- `sk-…` style API keys
- `ya29.…` OAuth tokens
- `Bearer …` headers
- PEM private key blocks

## When a blocked secret commit already exists locally
If a secret-containing commit exists in the local backup workdir history, GitHub will continue to reject pushes until history is rewritten.

The clean fix (for a dedicated backup workdir repo):
- Reset local repo to remote main:
  - `git fetch origin`
  - `git reset --hard origin/main`
- Re-run the backup script so a fresh commit is created without the secret.

Note: `git reset --hard` is destructive and may require explicit approval in Hermes. If the tool layer blocks it, ask the user to run it manually in the container.

## UX preference
If the user says “don’t give me code, just fix backup and restart”, avoid pasting code blocks. Apply the change (patch scripts/config), then run the backup and report the final status (`STATUS: PUSHED` / `STATUS: NO_CHANGES`) plus any next required action.
