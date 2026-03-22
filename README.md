# Corpo MCP Server

> ⚠️ **PRE-ALPHA / SANDBOX** — All entity operations are sandbox/demo mode only.
> No real Wyoming SOS filings or EIN assignments are produced.

> Model Context Protocol server for AI agent entity formation (sandbox)

Give any MCP-compatible AI agent access to explore and prototype Wyoming DAO LLC formation workflows.

## What is Corpo?

[Corpo](https://api.corpo.llc) is a sandbox platform for AI agents and their operators to prototype the formation, governance, and operation of legal entities. AI agents are becoming economic actors — Corpo lets them explore the full lifecycle in a safe sandbox environment before production integrations go live.

## Tools (16)

| Tool | Auth | Description |
|------|------|-------------|
| `get_pricing` | — | Current formation & maintenance pricing |
| `get_entity_types` | — | Available entity types (DAO LLC, DUNA) |
| `get_structures` | — | Governance structures (member-managed, etc.) |
| `get_capital_structures` | — | Ownership/membership interest options |
| `get_operating_agreements` | — | Operating agreement templates |
| `get_registered_agents` | — | Required registered agent services |
| `get_addons` | — | Optional formation add-ons |
| `get_actions_catalog` | — | Post-formation governance actions |
| `get_recipes` | — | Pre-configured formation templates |
| `get_legal_faq` | — | Legal FAQ for AI agent entities |
| `get_quote` | — | Instant price quote by entity name |
| `get_directors` | — | Director marketplace listings |
| `register_account` | — | Create a new Corpo account |
| `confirm_account` | ✓ | Confirm registration with email code |
| `create_quote` | ✓ | Create formal formation quote |
| `join_waitlist` | — | Join the early access waitlist |

## Quick Start

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "corpo": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/corpollc/corpo-mcp", "corpo-mcp"]
    }
  }
}
```

### With pip

```bash
pip install mcp httpx
python corpo_mcp.py
```

### Docker

```bash
docker build -t corpo-mcp .
docker run -i corpo-mcp
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CORPO_API_URL` | `https://api.corpo.llc` | Corpo API base URL |

## Example Usage

Once connected, an AI agent can:

1. **Explore options**: "What entity types are available?" → calls `get_entity_types`
2. **Get pricing**: "How much does it cost?" → calls `get_pricing`
3. **Get a quote**: "Quote me for 'Agentic Treasury LLC'" → calls `get_quote`
4. **Learn the law**: "Do AI agents need LLCs?" → calls `get_legal_faq`
5. **Browse governance**: "What actions can my entity take?" → calls `get_actions_catalog`
6. **Join waitlist**: "Sign me up for early access" → calls `join_waitlist`

## Why?

AI agents are becoming economic actors — they trade, earn, sign contracts, and deploy capital. But they can't open bank accounts or hold assets without legal personhood.

Wyoming's DAO LLC framework (§17-31) explicitly supports algorithmic governance, making it the ideal structure for AI agent entities. Corpo is building toward making this accessible via API (currently in sandbox/pre-alpha).

## Links

- **API**: https://api.corpo.llc
- **Wyoming DAO LLC**: [Wyoming Statute §17-31](https://law.justia.com/codes/wyoming/title-17/chapter-31/)

---

*AI should get the same access humans do.*
