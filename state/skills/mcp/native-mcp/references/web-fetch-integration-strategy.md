# Web fetch / search integration strategy

Use this when the user wants an advanced web search/fetch capability like Felo Search.

## Decision tree
1. If Hermes already has enough with browser or web tools, prefer that first.
2. If the user wants a reusable search API inside Hermes, add an MCP server.
3. If the target service has an API but no MCP server, write a small MCP wrapper around the API.
4. If no API exists, use a search backend such as SearxNG, Brave Search, Tavily, or a browser-based fetch workflow.

## Practical options
- Built-in Hermes web/browser tools: fastest to use, least setup.
- MCP wrapper over a search API: best for a named service the user wants to integrate.
- Community MCP search server: good if the user wants a ready-made service.

## Setup checklist for MCP-based web tools
- Ensure the Python `mcp` package is installed in the Hermes environment.
- Add `mcp_servers:` entries to the active Hermes config.
- Restart Hermes after editing config; MCP discovery happens at startup.
- Verify the discovered tool names use `mcp_<server>_<tool>`.
- Pass only the minimum required credentials to the MCP subprocess.

## Common patterns
- Search server: query -> results -> optional fetch/extract tool.
- Fetch server: URL -> cleaned article/text -> structured output.
- Hybrid server: search + fetch + browser fallback.

## Good fit signals
- The user wants a repeatable, first-class tool inside Hermes.
- The user wants structured results, not just raw browser automation.
- The user wants one integration point they can reuse across sessions.
