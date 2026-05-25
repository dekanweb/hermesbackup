#!/usr/bin/env python3
"""Mirror Hermes-related state into a repo-local snapshot directory.

This intentionally backs up *Hermes-related* state from /opt/data while
skipping secrets and runtime junk. The snapshot is designed to be committed
by the repo's backup.sh wrapper.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

SOURCE_ROOT = Path("/opt/data")
DEFAULT_DEST = Path(__file__).resolve().parent / "state"

ROOT_FILES = [
    "config.yaml",
    "channel_directory.json",
    "SOUL.md",
    ".skills_prompt_snapshot.json",
]

SOURCE_DIRS = [
    (SOURCE_ROOT / ".hermes", "hermes-home"),
    (SOURCE_ROOT / "skills", "skills"),
    (SOURCE_ROOT / "cron", "cron"),
    (SOURCE_ROOT / "scripts", "scripts"),
    # Sessions ARE backed up, but secrets are scrubbed during copy.
    (SOURCE_ROOT / "sessions", "sessions"),
    (SOURCE_ROOT / "memories", "memories"),
    (SOURCE_ROOT / "Documents" / "Obsidian Vault", "obsidian-vault"),
]

EXCLUDED_DIR_NAMES = {
    ".git",
    ".ssh",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    ".venv",
    "venv",
    "env",
}

EXCLUDED_FILE_NAMES = {
    ".env",
    ".env.local",
    ".envrc",
    "auth.json",
    "google_token.json",
    "google_client_secret.json",
    "gateway.pid",
    "cron.pid",
}

EXCLUDED_SUFFIXES = (
    ".pyc",
    ".pyo",
    ".pyd",
    ".db-wal",
    ".db-shm",
    ".db-journal",
    ".log",
    ".pid",
    ".lock",
    ".key",
    ".pem",
    ".token",
)


# Common secret patterns to scrub from backed-up text (especially sessions).
# Goal: keep conversation history while preventing GitHub push-protection blocks.
SCRUB_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # Notion tokens often appear as `secret_...` or `ntn_...`
    (re.compile(r"secret_[A-Za-z0-9_\-]{8,}"), "secret_[REDACTED]"),
    (re.compile(r"ntn_[A-Za-z0-9]{8,}"), "ntn_[REDACTED]"),
    # OpenAI-style keys
    (re.compile(r"sk-[A-Za-z0-9]{16,}"), "sk-[REDACTED]"),
    # Google OAuth access/refresh tokens
    (re.compile(r"ya29\.[A-Za-z0-9_\-]+"), "ya29.[REDACTED]"),
    # Generic bearer tokens in JSON/logs
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9_\-\.]{16,}"), "Bearer [REDACTED]"),
    # Private keys blocks
    (re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----[\s\S]+?-----END [A-Z ]+PRIVATE KEY-----"), "-----BEGIN PRIVATE KEY-----\n[REDACTED]\n-----END PRIVATE KEY-----"),
]


def scrub_text(text: str) -> str:
    out = text
    for pattern, repl in SCRUB_PATTERNS:
        out = pattern.sub(repl, out)
    return out


@dataclass
class MirrorStats:
    copied_files: int = 0
    copied_dirs: int = 0
    skipped_files: int = 0
    skipped_dirs: int = 0


def should_skip(path: Path) -> bool:
    parts = path.parts
    if any(part in EXCLUDED_DIR_NAMES for part in parts[:-1]):
        return True
    name = path.name
    if name in EXCLUDED_FILE_NAMES:
        return True
    if any(name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES):
        return True
    return False


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def copy_file(src: Path, dst: Path) -> None:
    """Copy a file to dst.

    For session transcripts, scrub common secret patterns before writing.
    This preserves conversation history while reducing secret-scanning blocks.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)

    # Scrub text only for session files (which may contain tool outputs / tokens).
    if "sessions" in src.parts:
        try:
            raw = src.read_bytes()
            text = raw.decode("utf-8")
        except Exception:
            shutil.copy2(src, dst)
            return

        scrubbed = scrub_text(text)
        dst.write_text(scrubbed, encoding="utf-8")
        try:
            shutil.copystat(src, dst)
        except Exception:
            pass
        return

    shutil.copy2(src, dst)


def mirror_tree(src: Path, dst: Path, stats: MirrorStats) -> None:
    if not src.exists():
        return

    if src.is_file():
        if should_skip(src):
            stats.skipped_files += 1
            return
        copy_file(src, dst)
        stats.copied_files += 1
        return

    for item in src.rglob("*"):
        rel = item.relative_to(src)
        if should_skip(rel):
            if item.is_dir():
                stats.skipped_dirs += 1
            else:
                stats.skipped_files += 1
            continue
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            stats.copied_dirs += 1
        else:
            copy_file(item, target)
            stats.copied_files += 1


def mirror_root_files(dst: Path, stats: MirrorStats) -> None:
    for name in ROOT_FILES:
        src = SOURCE_ROOT / name
        if not src.exists() or should_skip(src):
            continue
        copy_file(src, dst / name)
        stats.copied_files += 1


def build_manifest(stats: MirrorStats) -> dict:
    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_root": str(SOURCE_ROOT),
        "included": [
            {"source": str(src), "dest": dest}
            for src, dest in SOURCE_DIRS
            if src.exists()
        ],
        "root_files": [
            name for name in ROOT_FILES
            if (SOURCE_ROOT / name).exists() and not should_skip(SOURCE_ROOT / name)
        ],
        "stats": asdict(stats),
        "exclusions": {
            "directories": sorted(EXCLUDED_DIR_NAMES),
            "files": sorted(EXCLUDED_FILE_NAMES),
            "suffixes": list(EXCLUDED_SUFFIXES),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Mirror Hermes state into a repo-local directory")
    parser.add_argument("--dest", default=str(DEFAULT_DEST), help="Destination directory")
    args = parser.parse_args()

    dest = Path(args.dest).expanduser().resolve()
    if dest.exists():
        remove_existing(dest)
    dest.mkdir(parents=True, exist_ok=True)

    stats = MirrorStats()

    for src, dest_name in SOURCE_DIRS:
        if not src.exists():
            continue
        if src.is_dir():
            (dest / dest_name).mkdir(parents=True, exist_ok=True)
            stats.copied_dirs += 1
            mirror_tree(src, dest / dest_name, stats)
        else:
            copy_file(src, dest / dest_name)
            stats.copied_files += 1

    mirror_root_files(dest, stats)

    (dest / "MANIFEST.json").write_text(
        json.dumps(build_manifest(stats), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
