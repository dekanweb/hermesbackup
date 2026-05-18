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
- Use SSH deploy keys or equivalent repo-scoped access.
- Manual trigger phrases can be mapped to a backup action when the user has established one.
- Backups should capture the live persistent state, not task progress or transient logs.

## Restore notes
- A restore should be able to reconstruct the same state layout from the repo mirror.
- Keep restore logic separate from backup logic so the backup path stays simple and safe.
- Verify that restored files land in the same Hermes home/profile paths used by the running instance.

## Practical pitfall
Hermes-specific state is often split across multiple directories and top-level files. If only the repo root or one subdirectory is mirrored, the backup is incomplete even if git push succeeds.