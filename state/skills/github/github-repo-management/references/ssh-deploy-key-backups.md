# SSH deploy key backup notes

- Deploy keys are best for unattended pushes to a single repo.
- Enable write access on the deploy key if the agent should push.
- Use an ed25519 key pair.
- Add GitHub to `known_hosts` once with `ssh-keyscan github.com` to avoid host verification failures.
- Set `core.sshCommand` to the deploy key path when multiple keys or repos are in play.
- Prefer timestamped commits and a quiet push so cron output stays readable.
