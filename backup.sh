#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Mirror the Hermes-related state into the repo-local snapshot.
python3 ./backup_state.py --dest ./state

# Use the repo-specific SSH key configured in git core.sshCommand.

# Stage everything that is not ignored.
git add -A

if git diff --cached --quiet; then
  echo "STATUS: NO_CHANGES"
  exit 0
fi

stamp="$(TZ=Europe/Brussels date '+%Y-%m-%d %H:%M:%S %Z')"
if git commit --quiet -m "Backup: ${stamp}"; then
  git push --quiet origin main
  echo "STATUS: PUSHED"
  echo "Backup pushed at ${stamp}"
fi
