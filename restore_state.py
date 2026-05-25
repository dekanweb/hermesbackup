#!/usr/bin/env python3
"""Restore Hermes-related state from a repo-local snapshot back into /opt/data.

The backup repo stores mirrored state under ./state. This script can restore
from the current working tree or from an older git ref (commit, tag, or branch)
by materializing that ref's state directory into a temporary extraction area.

Secrets are intentionally excluded from backups and therefore never restored.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_TARGET = Path("/opt/data")
STATE_DIRNAME = "state"

STATE_MAP = [
    ("hermes-home", ".hermes"),
    ("skills", "skills"),
    ("cron", "cron"),
    ("scripts", "scripts"),
    ("sessions", "sessions"),
    ("memories", "memories"),
    ("obsidian-vault", "Documents/Obsidian Vault"),
]

ROOT_FILES = [
    "config.yaml",
    "channel_directory.json",
    "SOUL.md",
    ".skills_prompt_snapshot.json",
]


@dataclass
class RestoreStats:
    copied_files: int = 0
    copied_dirs: int = 0
    removed_paths: int = 0


def run(cmd: list[str], *, cwd: Path | None = None, capture_output: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=True,
        text=True,
        capture_output=capture_output,
    )


def git_ref_to_snapshot(ref: str) -> Path:
    """Materialize ./state from a git ref into a temporary directory."""
    tmp = Path(tempfile.mkdtemp(prefix="hermesbackup-restore-"))
    tar_path = tmp / "snapshot.tar"

    with tar_path.open("wb") as fh:
        subprocess.run(
            ["git", "archive", "--format=tar", ref, STATE_DIRNAME],
            cwd=str(REPO_ROOT),
            check=True,
            stdout=fh,
        )

    extract_dir = tmp / "extract"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path, "r:") as tar:
        tar.extractall(extract_dir)
    return extract_dir / STATE_DIRNAME


def resolve_snapshot_source(ref: str | None) -> Path:
    if ref:
        return git_ref_to_snapshot(ref)
    snapshot = REPO_ROOT / STATE_DIRNAME
    if not snapshot.exists():
        raise FileNotFoundError(f"Snapshot directory not found: {snapshot}")
    return snapshot


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def copy_path(src: Path, dst: Path, stats: RestoreStats) -> None:
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        stats.copied_dirs += 1
        for item in src.iterdir():
            copy_path(item, dst / item.name, stats)
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    stats.copied_files += 1


def restore_snapshot(snapshot_root: Path, target_root: Path, *, prune: bool = True) -> RestoreStats:
    stats = RestoreStats()

    for source_name, target_name in STATE_MAP:
        src = snapshot_root / source_name
        dst = target_root / target_name
        if not src.exists():
            continue
        if prune and dst.exists():
            remove_path(dst)
            stats.removed_paths += 1
        copy_path(src, dst, stats)

    for name in ROOT_FILES:
        src = snapshot_root / name
        if not src.exists():
            continue
        dst = target_root / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        stats.copied_files += 1

    return stats


def load_manifest(snapshot_root: Path) -> dict | None:
    manifest_path = snapshot_root / "MANIFEST.json"
    if not manifest_path.exists():
        return None
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Restore Hermes-related state from a backup snapshot")
    parser.add_argument("--ref", help="Git ref to restore from (commit, tag, branch). Defaults to current state dir.")
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="Target directory to restore into")
    parser.add_argument("--no-prune", action="store_true", help="Overlay without deleting existing included paths first")
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen without writing files")
    args = parser.parse_args()

    snapshot_root = resolve_snapshot_source(args.ref)
    target_root = Path(args.target).expanduser().resolve()
    manifest = load_manifest(snapshot_root)

    plan = {
        "snapshot_root": str(snapshot_root),
        "target_root": str(target_root),
        "prune": not args.no_prune,
        "dry_run": args.dry_run,
        "manifest": manifest,
    }

    if args.dry_run:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    target_root.mkdir(parents=True, exist_ok=True)
    stats = restore_snapshot(snapshot_root, target_root, prune=not args.no_prune)
    print(json.dumps({**plan, "stats": asdict(stats)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
