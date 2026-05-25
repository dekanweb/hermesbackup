---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Assistant-managed usage and portability

Obsidian vaults are plain folders of markdown files, not a closed database. If the user wants Hermes to manage notes conversationally, a GUI and Obsidian account are not required for day-to-day capture, organization, search, and planning.

Treat the vault folder itself as the portable/exportable unit:
- copying the vault directory is effectively export
- opening that directory in Obsidian elsewhere is effectively import
- iPhone or desktop use later requires only that the vault be synchronized into a location that device can access

If the user has a generic Hermes GitHub backup workflow, include the vault directory in that mirrored backup scope so new notes/subfolders are captured automatically without per-folder requests.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

If the vault path contains spaces and the `.env` file may be sourced by a shell, quote the value in `.env`, for example:

```bash
OBSIDIAN_VAULT_PATH="/opt/data/Documents/Obsidian Vault"
```

Without quotes, shell-sourcing the env file can mis-parse the path and break downstream commands even though file tools can still use the raw absolute path.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Portable Linux installs in constrained environments

When asked to install Obsidian on Linux and the normal package route is unavailable, prefer the official AppImage and treat it as a portable app:

1. Download the latest official AppImage from the Obsidian releases page.
2. If FUSE is unavailable, extract the AppImage with `--appimage-extract` and run from the extracted directory.
3. If the binary is missing shared libraries, inspect with `ldd` and satisfy them with the system package manager or a local library directory.
4. On sandboxed/containerized desktops, pass `--no-sandbox` when required by Electron/Chromium packaging.
5. Verify with a small launch command before declaring success.

If a GUI still cannot start because the host lacks desktop services, stop at the portable-install boundary and report that the app files are installed even if the full UI cannot be launched in that environment.

## Assistant-managed use without GUI

A GUI is not required when the user wants the assistant to manage notes through conversation. For filesystem-first workflows, the assistant can create, search, edit, and organize vault notes directly with file tools while the user interacts only via chat.

This is a good fit for mixed-use vaults that combine business and personal material, such as:
- competitor lists and social accounts for a brand
- brand-specific price tracking and competitor pricing
- multiple brands in parallel
- personal planning, life notes, and future design

When bootstrapping a vault for this pattern, prefer a lightweight top-level structure the assistant can route notes into immediately, for example:
- `Inbox/` for quick capture
- `Planlama/` or `Planning/` for future design and goals
- `Projeler/` for active brand or work streams
- `Alanlar/` for ongoing life/business areas
- `Kaynaklar/` for references
- `Templates/` for reusable note shells

If the user later wants to open the same vault on iPhone, explain that the vault contents must be synchronized to a location the phone can access, such as Obsidian Sync or iCloud Drive. The vault being manageable by the assistant does not imply it is automatically reachable from the phone.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.
