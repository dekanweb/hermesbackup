# Deploy-key backup notes

Use a deploy key when the user wants a single GitHub repo to receive recurring backups without repeated credential prompts.

- Deploy keys are repo-scoped.
- Use write access if the agent should push backups.
- Keep the private key local to the backup machine.
- Add the host key once with `ssh-keyscan github.com` to avoid host verification failures.
- Prefer an explicit SSH command per repo when multiple repos/keys may exist:
  - `git config core.sshCommand 'ssh -i /path/to/key -o IdentitiesOnly=yes'`
