# Cron backup wrapper path pitfall

Observed during Hermes backup automation:

- The cron job `script` field resolves relative to `HERMES_HOME/scripts/`.
- A symlink can be rejected if it resolves outside that directory.
- The safe pattern is to keep a *real file* at `HERMES_HOME/scripts/<name>`.
- If the canonical copy lives elsewhere for mirroring purposes, mirror that directory too so restore can round-trip the wrapper.

Practical verification:
1. Confirm the file exists at `HERMES_HOME/scripts/<name>`.
2. Confirm it is executable (`chmod 755` if needed).
3. Run it directly from the expected working directory before waiting for the scheduled tick.
4. If the cron runner emits a path-resolution error, replace symlinks with a real file under `HERMES_HOME/scripts/`.