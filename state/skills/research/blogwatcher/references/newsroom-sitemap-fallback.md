# Newsroom / article-fallback recipe

Use this when a target site has a newsroom page but no usable RSS/Atom feed.

## Pattern
1. Inspect the newsroom page in a browser to confirm it is reachable and to discover whether pagination or a "See more" link exists.
2. Fetch `sitemap.xml` and enumerate URLs under the newsroom/news prefix.
3. Sort URLs by `<lastmod>` to get the most recent items.
4. Fetch individual article pages with a browser-like User-Agent if direct requests are blocked.
5. Extract article metadata from:
   - `meta[property="og:title"]`
   - `meta[name="description"]` / `meta[property="og:description"]`
   - article `<h1>` and body paragraphs
6. If the page is JS-rendered, use browser snapshot/console to collect visible titles and hrefs first, then fetch the article URLs directly.

## Pitfalls
- Some sites expose a generic homepage description in `og:description`; prefer page-specific body text when available.
- The visible newsroom list may show only the latest N items; sitemap can reveal a deeper archive.
- Always cap the number of fetched pages when the user asks for a summary bundle (e.g. 15–20 items).

## Example signals from Anthropic newsroom
- `https://www.anthropic.com/sitemap.xml` exposes `/news/` URLs with `<lastmod>` timestamps.
- The newsroom page itself may show the latest items and a `See more` control, but the sitemap is the better source for archive coverage.
- `curl -A 'Mozilla/5.0'` is a practical fallback when direct fetches are blocked by anti-bot checks.
