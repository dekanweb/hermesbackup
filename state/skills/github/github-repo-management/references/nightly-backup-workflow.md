# Nightly GitHub backup workflow

Use this pattern when the user wants recurring automated backups to a private GitHub repo.

## Recommended setup
- Create a private repo.
- Add a *deploy key* for that single repo with write access.
- Use an SSH remote: `git@github.com:<owner>/<repo>.git`.
- Keep the private key local only; ignore `.ssh/` in the backup tree.

## Repo-local git configuration
- Set `core.sshCommand` to pin the repo to its own SSH key:
  - `ssh -i /path/to/deploy_key -o IdentitiesOnly=yes`
- Set a stable commit identity once; no repeated email prompts.
- If the host is not trusted yet, add GitHub to `~/.ssh/known_hosts` with `ssh-keyscan github.com`.

## Backup script pattern
A good default backup script:
- `git add -A`
- if nothing changed, print `STATUS: NO_CHANGES` and exit 0
- otherwise commit with a timestamp and push quietly
- print `STATUS: PUSHED` on success

Timestamp preference used in this session:
- `TZ=Europe/Brussels date '+%Y-%m-%d %H:%M:%S %Z'`

## Automation note
When scheduling from Hermes cron tooling in this environment, the script must live under `~/.hermes/scripts/` and be referenced by filename, not absolute path.

## Manual trigger phrase
- If the user gives a dedicated phrase meaning “backup now”, run the backup script immediately.
- Do not ask for additional confirmation when the phrase has already been established in-session.
- In this session, the established phrase is **“şimdi yedek al”**.
- Keep the behavior aligned with the same commit/push path as the scheduled job.

## Verification
- `git ls-remote origin HEAD` to test SSH access
- `git push -u origin main` for the first upload
- run the backup script manually once after any workflow change
