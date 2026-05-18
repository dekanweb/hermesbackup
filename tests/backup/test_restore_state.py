from __future__ import annotations

from pathlib import Path

from restore_state import restore_snapshot


def _write(path: Path, content: str = "x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_restore_snapshot_prunes_only_backed_up_paths(tmp_path: Path) -> None:
    snapshot = tmp_path / "snapshot"
    target = tmp_path / "target"

    # Build a minimal backup snapshot.
    _write(snapshot / "skills" / "blogwatcher" / "SKILL.md", "skill-v2")
    _write(snapshot / "cron" / "jobs.json", '{"jobs": []}')
    _write(snapshot / "sessions" / "session.json", '{"session": 1}')
    _write(snapshot / "memories" / "USER.md", "prefers Turkish")
    _write(snapshot / "hermes-home" / "scripts" / "hermesbackup_daily.sh", "echo backup")
    _write(snapshot / "config.yaml", "model: test")
    _write(snapshot / "channel_directory.json", "{}")
    _write(snapshot / "SOUL.md", "soul")
    _write(snapshot / ".skills_prompt_snapshot.json", "{}")

    # Pretend the target already contains old data plus secrets that must survive.
    _write(target / "skills" / "blogwatcher" / "SKILL.md", "old-skill")
    _write(target / "skills" / "old" / "REMOVE_ME.txt", "old")
    _write(target / "cron" / "jobs.json", '{"jobs": [1]}')
    _write(target / ".hermes" / "scripts" / "old.sh", "old")
    _write(target / ".env", "SECRET=keep")
    _write(target / ".ssh" / "id_ed25519", "private-key")

    stats = restore_snapshot(snapshot, target, prune=True)

    assert (target / "skills" / "blogwatcher" / "SKILL.md").read_text(encoding="utf-8") == "skill-v2"
    assert (target / "cron" / "jobs.json").read_text(encoding="utf-8") == '{"jobs": []}'
    assert (target / "sessions" / "session.json").exists()
    assert (target / "memories" / "USER.md").exists()
    assert (target / ".hermes" / "scripts" / "hermesbackup_daily.sh").exists()
    assert (target / "config.yaml").read_text(encoding="utf-8") == "model: test"

    # Secrets / runtime-only files are not touched by restore.
    assert (target / ".env").read_text(encoding="utf-8") == "SECRET=keep"
    assert (target / ".ssh" / "id_ed25519").read_text(encoding="utf-8") == "private-key"

    # Pruned paths should be replaced, not merged.
    assert not (target / "skills" / "old").exists()
    assert not (target / ".hermes" / "scripts" / "old.sh").exists()

    assert stats.copied_files >= 6
    assert stats.removed_paths >= 3
