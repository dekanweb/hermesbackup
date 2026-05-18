# Browser Use cloud browser setup

Use this when Hermes should drive a Browser Use cloud session.

## Direct setup

1. Add your API key to `~/.hermes/.env`:
   ```bash
   BROWSER_USE_API_KEY=...
   ```
2. Set the browser provider in `~/.hermes/config.yaml`:
   ```yaml
   browser:
     cloud_provider: browser-use
   ```
3. Restart Hermes / start a fresh session so the browser config is re-read.

## Notes

- If `browser.cloud_provider` is unset, Hermes may auto-pick another cloud provider when credentials exist.
- If Browserbase and Browser Use are both configured, Browserbase takes priority unless `browser.cloud_provider` explicitly selects Browser Use.
- `browser.cloud_provider: local` disables cloud fallback and keeps browser automation local.
- `browser.allow_private_urls: true` is a separate setting; it affects whether private/LAN URLs may be attempted by the browser tool.
