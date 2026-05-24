# Obsidian on constrained Linux environments

Use this when installing the official Obsidian AppImage on a Linux host where normal desktop assumptions do not hold.

## Typical portable workflow

- Download the latest official AppImage from the Obsidian releases page.
- If FUSE is unavailable, extract it with:
  - `./Obsidian.AppImage --appimage-extract`
- Run from the extracted `squashfs-root` / AppDir.
- If `ldd` reports missing shared libraries, satisfy them with either:
  - system packages, or
  - a local library directory placed on `LD_LIBRARY_PATH`.
- On containerized or sandbox-restricted hosts, Electron/Chromium may require `--no-sandbox`.

## Verification

- Confirm the launcher resolves the extracted AppImage binary.
- Run a minimal startup check such as `--version` or a non-destructive launch probe.
- If the UI still fails due to missing desktop services, treat the app files as installed but the host as unsuitable for a full GUI session.

## Notes

This is a portable-install pattern, not a desktop-integration recipe. For desktop integration, use the host OS package conventions instead.
