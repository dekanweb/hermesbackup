#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 ./restore_state.py "$@"
