# Private backup repo workflow

When the user wants a recurring backup repo that only they can access:
- create a private repository
- add a repo-scoped SSH deploy key with write access
- set the local repo remote to SSH
- pin the repo to its own private key using `core.sshCommand`
- keep the private key local and ignore `.ssh/`
- use a backup script that emits a clear status line for automation (`STATUS: PUSHED` / `STATUS: NO_CHANGES`)

For scheduling via Hermes cron in this environment, the script must live under `~/.hermes/scripts/` and be referenced by filename.
