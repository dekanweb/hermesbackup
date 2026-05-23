This Hermes environment runs inside Docker, and `hermes gateway install` reports that service installation is not needed inside a Docker container.
§
Hermes config at /opt/data/config.yaml is set to use browser.cloud_provider: browser-use.
§
Bu ortamda `hermes` CLI PATH'te değil; doğrudan `hermes` komutu çalışmıyor. `python3` mevcut (/usr/bin/python3, sürüm 3.13.5).
§
User's GitHub backup repository is github.com/dekanweb/hermesbackup, used for Hermes backups.
§
User backs up Hermes to the GitHub repo dekanweb/hermesbackup and prefers nightly automated backups via SSH deploy key.
§
In this Hermes environment, the Python `mcp` package is not installed, and `/opt/data/config.yaml` currently has no `mcp_servers` configured.
§
In this Hermes environment, the main Hermes-related persistent data paths are /opt/data/.hermes, /opt/data/skills, /opt/data/cron, /opt/data/sessions, /opt/data/memories, plus top-level files like /opt/data/config.yaml, /opt/data/channel_directory.json, /opt/data/SOUL.md, and /opt/data/.skills_prompt_snapshot.json. The backup workflow mirrors these into the GitHub backup repo and excludes secrets/runtime junk such as .env, auth.json, .ssh, lock files, pid files, and cache directories.
§
The Hermes GitHub backup mirror now stores Hermes-related state under repo-local state/: /opt/data/.hermes, /opt/data/skills, /opt/data/cron, /opt/data/sessions, /opt/data/memories, plus /opt/data/config.yaml, /opt/data/channel_directory.json, /opt/data/SOUL.md, and /opt/data/.skills_prompt_snapshot.json. The repo includes ./backup.sh to push snapshots and ./restore.sh (with --ref and --dry-run) to restore an older backup from git history. Secrets such as .env, auth.json, .ssh, pid/lock files, and caches remain excluded.
§
In this Hermes environment, HERMES_HOME and HOME are /opt/data, so cron script paths resolve under /opt/data/scripts; backup wrapper scripts may also exist under /opt/data/.hermes/scripts, and a symlink or copy into /opt/data/scripts is needed for cron jobs to find them.