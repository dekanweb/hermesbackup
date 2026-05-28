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
Hermes GitHub backup repo dekanweb/hermesbackup mirrors durable state under repo-local state/ (/.hermes, skills, cron, sessions, memories + config.yaml/channel_directory.json/SOUL.md/.skills_prompt_snapshot.json); excludes secrets (.env/auth.json/.ssh) and caches; includes backup.sh + restore.sh. Deployment is Hostinger/Hostingetr Ubuntu VPS running Hermes in Docker (image ghcr.io/hostinger/hvps-hermes-agent:latest); container may lack nano/vi so /opt/data/.env edits may require non-editor methods (e.g., python3).
§
In this Hermes environment, HERMES_HOME and HOME are /opt/data, so cron script paths resolve under /opt/data/scripts; backup wrapper scripts must be real files there because cron blocks symlinks that resolve outside the scripts directory.
§
Hermes is running in a Docker container and cannot be updated with 'hermes update'. It requires pulling a new Docker image (e.g., 'docker pull nousresearch/hermes-agent:latest') and restarting the container.