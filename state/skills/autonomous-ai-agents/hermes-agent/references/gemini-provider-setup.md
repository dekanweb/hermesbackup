# Gemini provider setup

Use this when binding Gemini in Hermes.

## Provider choices

- `gemini` = Google AI Studio / API-key based
  - Auth: `GOOGLE_API_KEY` or `GEMINI_API_KEY`
  - Good for direct API-key usage
- `google-gemini-cli` = Google OAuth / Gemini CLI
  - Auth: browser OAuth via `hermes model`
  - Use this when you want the CLI/OAuth flow instead of an API key

If you need a specific model name for the native `gemini` provider, use Google AI Studio model IDs without the `google/` prefix, such as:

```bash
hermes config set model gemini-2.5-flash
```

The `google/gemini-*` form is for OpenRouter-style routing and can produce Gemini native API HTTP 404 errors when `model.provider: gemini`.

Or set the top-level model directly:
If you need a specific model name for the native `gemini` provider, use Google AI Studio model IDs without the `google/` prefix, such as:

```bash
hermes config set model gemini-2.5-flash
```

The `google/gemini-*` form is for OpenRouter-style routing and can produce Gemini native API HTTP 404 errors when `model.provider: gemini`.

If using an environment where `hermes` is not on `PATH`, edit `$HERMES_HOME/config.yaml` directly and set:

```yaml
model:
  provider: gemini
  default: google/gemini-2.5-flash
```

For API-key auth, ensure `$HERMES_HOME/.env` has at least one of:

```dotenv
GOOGLE_API_KEY=...
GEMINI_API_KEY=...
```

For Telegram gateway conversations, there usually is no separate Telegram model override; Telegram uses the global `model.*` settings unless a platform/profile-specific override has been configured. After changing `model.*` or `.env`, restart the gateway (`/restart` from Telegram or `hermes gateway restart`) so new Telegram conversations pick up Gemini.

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
- If you change model/provider settings in a live CLI session, restart or start a new session for the change to take effect.
- For gateway platforms such as Telegram, changing `.env` or `model.*` does not affect the already-running gateway process; use `/restart` from the gateway or restart the gateway service.
