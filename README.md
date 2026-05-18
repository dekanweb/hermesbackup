# Hermes backup mirror

This repo stores a private backup mirror of Hermes-related state from `/opt/data`.

## What gets backed up
- `/opt/data/.hermes`
- `/opt/data/skills`
- `/opt/data/cron`
- `/opt/data/sessions`
- `/opt/data/memories`
- `/opt/data/config.yaml`
- `/opt/data/channel_directory.json`
- `/opt/data/SOUL.md`
- `/opt/data/.skills_prompt_snapshot.json`

## What does not get backed up
- `.env`
- `auth.json`
- `.ssh/`
- lock files, pid files, caches, and other runtime junk

## Backup
```bash
./backup.sh
```

If nothing changed:
```text
STATUS: NO_CHANGES
```

If the snapshot was pushed:
```text
STATUS: PUSHED
```

## Restore
Restore the current snapshot into `/opt/data`:
```bash
./restore.sh --dry-run
./restore.sh --target /opt/data --no-prune
./restore.sh --target /opt/data
```

Restore an older backup from Git history:
```bash
./restore.sh --ref HEAD~1 --dry-run
./restore.sh --ref <commit-or-tag> --target /opt/data
```

Notes:
- `--dry-run` shows the plan only.
- Default restore mode prunes the included target paths first, then copies the backup back.
- Secrets are not restored because they are intentionally excluded from the backup.
