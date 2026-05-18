# Telegram gateway lock recovery

Use when `hermes gateway run` fails with:
- `Telegram bot token already in use (PID N)`
- gateway status says not running, but the token lock still exists

Observed failure pattern:
- the blocking PID may be a zombie or stale process record
- the lock file lives under the machine-local gateway lock dir, typically:
  `~/.local/state/hermes/gateway-locks/telegram-bot-token-<hash>.lock`
- `HERMES_HOME` may point elsewhere; the lock dir is derived from `XDG_STATE_HOME` / `~/.local/state`, not `HERMES_HOME`

Recovery steps:
1. Check `hermes gateway status`.
2. Inspect the lock file contents to confirm PID/start_time.
3. Verify the PID with `/proc/<pid>/status` and `/proc/<pid>/stat`.
4. If the PID is stale/zombie and no live gateway owns it, remove only the matching `telegram-bot-token-*.lock` file.
5. Restart with `hermes gateway run --replace`.
6. Re-check status and send a Telegram test message.

Helpful commands:
```bash
find ~/.local/state/hermes/gateway-locks -maxdepth 1 -name 'telegram-bot-token-*.lock' -print
cat ~/.local/state/hermes/gateway-locks/telegram-bot-token-*.lock
ps -fp <pid>
cat /proc/<pid>/status
```

Related config noise seen during recovery:
- Deprecated `.env` vars such as `TERMINAL_CWD` may appear at startup; they are separate from the Telegram lock issue.
