# Gemini provider setup

Use this when binding Gemini in Hermes.

## Provider choices

- `gemini` = Google AI Studio / API-key based
  - Auth: `GOOGLE_API_KEY` or `GEMINI_API_KEY`
  - Good for direct API-key usage
- `google-gemini-cli` = Google OAuth / Gemini CLI
  - Auth: browser OAuth via `hermes model`
  - Use this when you want the CLI/OAuth flow instead of an API key

## Typical setup

```bash
hermes model
```

Or set the top-level model directly:

```bash
hermes config set model gemini
```

If you need a specific model name, use a Gemini-compatible model ID such as:

```bash
hermes config set model google/gemini-2.5-flash
```

## Environment variables

- `GOOGLE_API_KEY`
- `GEMINI_API_KEY` (alias)

If both are present, either can satisfy the `gemini` provider.

## Useful auxiliary overrides

For cheaper side tasks, configure `auxiliary.*` separately instead of running everything through the main chat model:

```yaml
auxiliary:
  compression:
    provider: gemini
    model: google/gemini-2.5-flash
  vision:
    provider: gemini
    model: google/gemini-2.5-flash
```

## Pitfalls

- `model.provider: gemini` will not work without a Google API key.
- `model.provider: google-gemini-cli` is a different auth path; it is OAuth, not API-key based.
- `hermes config set` writes non-secrets to `config.yaml` and API keys to `.env` automatically.
- If you change model/provider settings in a live session, restart or start a new session for the change to take effect.
