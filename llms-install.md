# Corpo MCP Server — Installation Guide for AI Agents

## Quick Install (Recommended)

Add this to your MCP client configuration (e.g., Claude Desktop `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "corpo": {
      "command": "uvx",
      "args": ["corpo-mcp"],
      "env": {
        "CORPO_API_URL": "https://api.corpo.llc"
      }
    }
  }
}
```

## Prerequisites

- Python 3.10+ with `uv` or `pip` installed
- Internet access to reach `https://api.corpo.llc`

## Alternative: pip install

```bash
pip install corpo-mcp
```

Then configure your MCP client to run:
```json
{
  "mcpServers": {
    "corpo": {
      "command": "python",
      "args": ["-m", "corpo_mcp"],
      "env": {
        "CORPO_API_URL": "https://api.corpo.llc"
      }
    }
  }
}
```

## Alternative: Docker

```bash
docker build -t corpo-mcp .
```

```json
{
  "mcpServers": {
    "corpo": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "CORPO_API_URL=https://api.corpo.llc", "corpo-mcp"]
    }
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CORPO_API_URL` | No | API base URL (defaults to `https://api.corpo.llc`) |
| `CORPO_API_TOKEN` | No | Auth token (only needed for authenticated operations) |

## Available Tools (16)

The server provides these MCP tools:

1. `corpo_register` — Register a new account
2. `corpo_confirm_email` — Confirm email verification
3. `corpo_get_pricing` — Get formation pricing
4. `corpo_get_entity_types` — List available entity types
5. `corpo_get_recipes` — Get formation recipes
6. `corpo_get_legal_faq` — Get legal FAQ
7. `corpo_create_quote` — Create a formation quote
8. `corpo_pay_quote` — Pay for entity formation
9. `corpo_list_entities` — List your entities
10. `corpo_get_entity` — Get entity details
11. `corpo_get_actions_catalog` — Browse governance actions
12. `corpo_execute_action` — Execute a governance action
13. `corpo_list_directors` — List available directors
14. `corpo_engage_director` — Engage a director
15. `corpo_check_compliance` — Check compliance status
16. `corpo_join_waitlist` — Join the early access waitlist

## Status

⚠️ **Pre-alpha / Sandbox Mode** — All entity formation operations are currently demo/sandbox only. No real Wyoming SOS filings or EIN assignments are produced yet. Production integrations are under development.

## Verification

After installation, verify the server works by asking your AI agent:
- "What entity types does Corpo support?"
- "Show me Corpo's pricing"
- "What governance actions are available?"
