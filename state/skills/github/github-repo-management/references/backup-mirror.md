# Backup mirror from a local tree

Use this when the source project already exists on disk and should be mirrored into a private GitHub repo.

## Checklist
- Ensure the target repo exists and is private.
- Copy the source tree into a writable workdir if the original tree is root-owned or read-only.
- Add or update `.gitignore` before the first commit.
- Set `git config user.name` and `git config user.email` once.
- Initialize git, add the SSH remote, create the initial commit, and push `main`.

## Pitfalls observed in this session
- Root-owned source trees may refuse writes, so work from a writable copy instead.
- `rsync` may be unavailable; `python`/`shutil` copy logic is a good fallback.
- Commit identity is required even for an internal backup repo.
