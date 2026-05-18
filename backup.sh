#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Use the repo-specific SSH key configured in git core.sshCommand.

# Stage everything that is not ignored.
git add -A

if git diff --cached --quiet; then
  exit 0
fi

stamp="$(TZ=Europe/Brussels date '+%Y-%m-%d %H:%M:%S %Z')"
git commit --quiet -m "Backup: ${stamp}"
git push --quiet origin main

echo "Backup pushed at ${stamp}"
