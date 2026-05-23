# GitHub backup workflow for Hermes state

This reference captures the durable backup pattern for Hermes environments that mirror persistent state into a private GitHub repo.

## Backup scope
Mirror Hermes state that matters across sessions:
- `~/.hermes/` or the profile-equivalent Hermes home
- `skills/`
- `cron/`
- `sessions/`
- `memories/`
- top-level config/state files such as `config.yaml`, `channel_directory.json`, `SOUL.md`, and `.skills_prompt_snapshot.json`

## Exclusions
Do **not** back up secrets or runtime junk:
- `.env`
- `auth.json`
- `.ssh/`
- lock files, pid files, caches, temp files
- any tokens, private keys, or provider credentials

## Workflow notes
- Prefer a private GitHub repo for backups.
- Use SSH deploy keys or equivalent repo-scoped access, ideally a repo-specific Ed25519 key with write access.
- Keep the private key local only; do not mirror `.ssh/` into the backup tree.
- Manual trigger phrases can be mapped to a backup action when the user has established one; in this session the phrase is **"şimdi yedek al"**.
- Backups should capture the live persistent state, not task progress or transient logs.
- A useful automation contract is `STATUS: PUSHED` or `STATUS: NO_CHANGES`.
- In this environment, the backup mirror stores Hermes state under repo-local `state/`.

## Restore notes
- A restore should be able to reconstruct the same state layout from the repo mirror.
- Keep restore logic separate from backup logic so the backup path stays simple and safe.
- Support restoring from an older git ref and dry-running before writing files.
- Verify that restored files land in the same Hermes home/profile paths used by the running instance.

## Backup scope recap
- `.hermes/`
- `skills/`
- `cron/`
- `sessions/`
- `memories/`
- `config.yaml`
- `channel_directory.json`
- `SOUL.md`
- `.skills_prompt_snapshot.json`

## Exclusions recap
- `.env`
- `auth.json`
- `.ssh/`
- lock / pid / cache files
- any tokens, private keys, or provider credentials

## Practical pitfall
Hermes-specific state is often split across multiple directories and top-level files. If only the repo root or one subdirectory is mirrored, the backup is incomplete even if git push succeeds.

## Cron wrapper placement
If a cron job uses the `script` field, the executable must be reachable under `HERMES_HOME/scripts/` at runtime. A wrapper that only exists in a mirrored state tree (for example, under `state/hermes-home/scripts/`) is not enough on its own.

Recommended pattern:
- keep the canonical script in the backed-up state tree if you want it mirrored,
- and expose a live copy or symlink at `HERMES_HOME/scripts/<name>` so the cron runner can resolve it.

Quick verification:
- confirm the path exists and is executable,
- then run the wrapper directly with the same working directory the job expects before waiting for the next schedule tick.