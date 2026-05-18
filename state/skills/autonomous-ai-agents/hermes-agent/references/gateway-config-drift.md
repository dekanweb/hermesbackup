# Gateway config drift and Telegram troubleshooting

Use this when a user shares `config.yaml` plus one or more recent backups and asks whether Telegram/gateway setup changed.

Workflow:
1. Read the current config and the nearest backups.
2. Diff the gateway-related regions first:
   - `agent.*`
   - `display.platforms`
   - platform blocks such as `telegram`, `discord`, `slack`, `matrix`, `whatsapp`
   - `approvals`, `security`, `sessions`, `model`, and `terminal` only if the issue is broader than messaging.
3. Look for behavioral drift, not just obvious credentials:
   - `telegram.allowed_chats`
   - `telegram.reactions`
   - platform mention / free-response settings
   - `display.platforms` overrides
4. If the config looks fine, check the gateway log next.
5. If the user is asking about connectivity, remember that the YAML usually contains platform behavior, while credentials and tokens are often in `~/.hermes/.env` or managed through Hermes auth setup.

Useful commands:
```bash
diff -u old.yaml new.yaml | sed -n '1,160p'
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

Notes:
- Small onboarding-only diffs can be red herrings; verify whether they affect the gateway path.
- Multiple backups with identical hashes usually mean the interesting change is between the latest backup and current config, not among the backups themselves.
