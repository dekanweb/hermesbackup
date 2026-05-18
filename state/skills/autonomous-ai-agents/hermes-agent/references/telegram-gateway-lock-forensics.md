# Telegram gateway lock forensics

Use this alongside `references/telegram-gateway-lock-recovery.md` when Telegram startup says a bot token is already in use.

Observed lock file shape:
```json
{
  "pid": 900,
  "kind": "hermes-gateway",
  "argv": ["/opt/hermes/hermes", "gateway", "run", "--replace"],
  "start_time": 1340946,
  "scope": "telegram-bot-token",
  "identity_hash": "6abeb51c1c77ee55",
  "metadata": {"platform": "telegram"},
  "updated_at": "..."
}
```

Checklist:
1. Read the lock file under `${XDG_STATE_HOME:-$HOME/.local/state}/hermes/gateway-locks/telegram-bot-token-*.lock`.
2. Parse the JSON and extract `pid` and `start_time`.
3. Verify the PID via `/proc/<pid>/status`.
4. Treat `State: Z (zombie)` as stale; a zombie process cannot own the token anymore.
5. Remove only the matching `telegram-bot-token-*.lock` file after confirming no live gateway owns it.
6. Restart the gateway with `hermes gateway run --replace`.

Useful commands:
```bash
cat ~/.local/state/hermes/gateway-locks/telegram-bot-token-*.lock
python3 - <<'PY'
import json, pathlib
p = next(pathlib.Path.home().joinpath('.local/state/hermes/gateway-locks').glob('telegram-bot-token-*.lock'))
print(json.loads(p.read_text()))
PY
cat /proc/<pid>/status | sed -n '1,6p'
```
