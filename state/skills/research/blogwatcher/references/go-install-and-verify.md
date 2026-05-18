# Go install and verify for blogwatcher

Use this when you want a user-writable install without relying on a system package manager.

## Install

```bash
export GOBIN="/opt/data/.npm-global/bin"   # or another writable bin dir on PATH
export GOPATH="/opt/data/go-work"
mkdir -p "$GOBIN" "$GOPATH"

go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest
```

## Verify

```bash
command -v blogwatcher
blogwatcher --help
blogwatcher --version
```

## Notes

- The Hyaxia fork installs a `blogwatcher` binary (not `blogwatcher-cli`) when built via `go install`.
- If you want the binary visible immediately in the current shell, prepend `GOBIN` to `PATH`.
- Prefer `blogwatcher --help` as the primary smoke test after installation.
