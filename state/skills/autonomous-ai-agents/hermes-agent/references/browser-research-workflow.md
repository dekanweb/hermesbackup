# Browser research workflow

Use this when researching a topic through Browser Use / browser automation.

## Practical sequence

1. Start broad with a search engine query in the target language and common aliases.
   - Example: search both the exact name and likely spelling variants.
2. Use `browser_snapshot` to inspect result structure and identify the most promising sources.
3. Click a source result, then read the page body and headings first.
4. Use `browser_console` for fast extraction when the snapshot is long or truncated:
   - `document.body.innerText`
   - anchor text lists
   - contact details / structured text snippets
5. If the target site shows a cookie dialog or overlay, dismiss it before extracting details.
6. Prefer primary sources:
   - official site
   - contact page
   - company / government / registry pages
   - then corroborating social/profile sources

## Query refinement tips

- Try multiple spellings, especially for names that may be transliterated or language-specific.
- Add country/location terms when the target is regional.
- If the query is ambiguous, search the brand alone and then the brand + country.

## What to extract

- identity: what the business or entity says it is
- services: stated offerings
- contact details: email, phone, address
- proof points: testimonials, portfolio, client counts, launch dates
- corroboration: other sources mentioning the same entity

## Output style

- Summarize with confidence levels when the evidence is partial.
- Separate direct evidence from inference.
- If you only found the website and no registry proof, say so clearly.
