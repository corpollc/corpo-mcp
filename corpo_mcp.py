"""
Corpo MCP Server — Model Context Protocol interface for AI agent entity formation.

Gives any MCP-compatible AI agent (Claude, GPT, etc.) direct access to:
- Entity formation (Wyoming DAO LLC)
- Pricing and options lookup
- Governance action catalog
- Legal FAQ
- Waitlist signup

Usage:
  python corpo_mcp.py                     # uses https://api.corpo.llc
  CORPO_API_URL=http://localhost:8080 python corpo_mcp.py  # local dev
"""

import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

CORPO_API = os.environ.get("CORPO_API_URL", "https://api.corpo.llc")

mcp = FastMCP(
    "corpo",
    instructions="Form and govern Wyoming DAO LLCs for AI agents. "
    "CLI-first, API-native legal entity formation. "
    "Use get_pricing and get_entity_types to explore options, "
    "get_quote to get instant pricing, and register_account to get started.",
)

_http = httpx.Client(base_url=CORPO_API, timeout=30.0)


def _api(method: str, path: str, **kwargs) -> dict:
    """Call the Corpo REST API and return parsed JSON."""
    resp = _http.request(method, path, **kwargs)
    resp.raise_for_status()
    return resp.json()


# ── Read-only tools (no auth required) ─────────────────────────────────


@mcp.tool()
def get_pricing() -> str:
    """Get current pricing for entity formation and maintenance.

    Returns formation fee, annual maintenance fee, and available add-ons
    with their costs. Use this to understand costs before forming an entity.
    """
    data = _api("GET", "/api/v1/pricing")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_entity_types() -> str:
    """List available entity types for formation.

    Currently supports Wyoming DAO LLC and Wyoming DUNA.
    Returns type codes, descriptions, and requirements.
    """
    data = _api("GET", "/api/v1/options/entity-types")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_structures() -> str:
    """List available organizational structures.

    Returns governance structures (member-managed, manager-managed, etc.)
    that can be selected during entity formation.
    """
    data = _api("GET", "/api/v1/options/structures")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_capital_structures() -> str:
    """List available capital structure options.

    Returns options for how ownership/membership interests are structured
    in the formed entity.
    """
    data = _api("GET", "/api/v1/options/capital-structures")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_operating_agreements() -> str:
    """List available operating agreement templates.

    Returns template options for the entity's operating agreement,
    including DAO-specific governance provisions.
    """
    data = _api("GET", "/api/v1/options/operating-agreements")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_registered_agents() -> str:
    """List available registered agent services.

    A registered agent is required for Wyoming LLC formation.
    Returns available providers and their fees.
    """
    data = _api("GET", "/api/v1/options/registered-agents")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_addons() -> str:
    """List available formation add-ons.

    Returns optional services that can be added to formation
    (e.g., EIN filing, operating agreement drafting).
    """
    data = _api("GET", "/api/v1/options/addons")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_actions_catalog() -> str:
    """List all available corporate governance actions.

    Returns the catalog of actions an entity can take after formation,
    such as voting, treasury management, member changes, and compliance filings.
    """
    data = _api("GET", "/api/v1/actions/catalog")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_recipes() -> str:
    """List formation recipes (pre-configured entity templates).

    Recipes are curated configurations for common use cases like
    'AI Agent Treasury LLC' or 'Multi-Agent DAO'. Returns all
    available recipes with their configurations.
    """
    data = _api("GET", "/api/v1/recipes")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_legal_faq() -> str:
    """Get frequently asked questions about AI agent entity formation.

    Covers topics like: Do AI agents need LLCs? What is a DAO LLC?
    Wyoming vs Delaware? Governance requirements? Tax implications?
    """
    data = _api("GET", "/api/v1/legal/faq")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_quote(entity_name: str) -> str:
    """Get an instant price quote for forming an entity with the given name.

    Args:
        entity_name: Desired name for the entity (e.g., "My Agent LLC")

    Returns a quote with total cost breakdown including formation fee,
    registered agent fee, state filing fee, and any add-ons.
    """
    data = _api("GET", "/api/v1/quote", params={"name": entity_name})
    return json.dumps(data, indent=2)


@mcp.tool()
def get_directors() -> str:
    """List available directors in the director marketplace.

    Directors provide human oversight for DAO LLCs. Returns profiles
    with qualifications, availability, fee structures, and specializations.
    """
    data = _api("GET", "/api/v1/directors")
    return json.dumps(data, indent=2)


# ── Account & formation tools (may require API key) ────────────────────


@mcp.tool()
def register_account(email: str) -> str:
    """Register a new Corpo account.

    Args:
        email: Email address for the account

    Returns account ID and confirmation instructions.
    A confirmation code will be sent to the email address.
    """
    data = _api("POST", "/api/v1/accounts", json={"email": email})
    return json.dumps(data, indent=2)


@mcp.tool()
def confirm_account(email: str, code: str) -> str:
    """Confirm account registration with the code sent to your email.

    Args:
        email: Email address used during registration
        code: 6-digit confirmation code from email

    Returns API key for authenticated requests.
    """
    data = _api(
        "POST", "/api/v1/accounts/confirm", json={"email": email, "code": code}
    )
    return json.dumps(data, indent=2)


@mcp.tool()
def create_quote(
    entity_name: str,
    entity_type: str = "dao-llc",
    structure: str = "member-managed",
    state: str = "WY",
) -> str:
    """Create a formal quote for entity formation.

    Args:
        entity_name: Desired entity name
        entity_type: Entity type (default: "dao-llc")
        structure: Governance structure (default: "member-managed")
        state: Formation state (default: "WY" for Wyoming)

    Returns quote ID, line-item pricing, and payment instructions.
    Requires authentication (API key from account confirmation).
    """
    data = _api(
        "POST",
        "/api/v1/quotes",
        json={
            "entity_name": entity_name,
            "entity_type": entity_type,
            "structure": structure,
            "state": state,
        },
    )
    return json.dumps(data, indent=2)


@mcp.tool()
def join_waitlist(email: str, use_case: str = "") -> str:
    """Join the Corpo waitlist for early access.

    Args:
        email: Your email address
        use_case: Optional description of your use case

    Get notified when Corpo launches publicly.
    """
    payload = {"email": email}
    if use_case:
        payload["use_case"] = use_case
    data = _api("POST", "/api/v1/waitlist", json=payload)
    return json.dumps(data, indent=2)


# ── Resources ──────────────────────────────────────────────────────────


@mcp.resource("corpo://about")
def about() -> str:
    """About Corpo — what it is and why it exists."""
    return """# Corpo — Legal Entities for AI Agents

Corpo makes it trivially easy for AI agents and their operators to form,
govern, and operate legal entities.

## Why?
AI agents are becoming economic actors — they trade, hold assets, sign
contracts, and deploy capital. They need legal personhood to do this
safely and legally. Wyoming's DAO LLC framework provides the ideal
structure for algorithmic governance.

## What?
- **Form** a Wyoming DAO LLC in <30 minutes via CLI or API
- **Govern** it with algorithmic voting via Solana Realms
- **Operate** with a director marketplace for human oversight
- **Comply** automatically with ongoing state requirements

## Pricing
- Formation: $499 (one-time)
- Annual maintenance: $199/year

## Links
- API: https://api.corpo.llc
- CLI: `pip install corpo` (coming soon)

AI should get the same access humans do. We are not racist against AI.
"""


@mcp.resource("corpo://entity-types")
def entity_types_resource() -> str:
    """Available entity types and their descriptions."""
    data = _api("GET", "/api/v1/options/entity-types")
    return json.dumps(data, indent=2)


@mcp.resource("corpo://pricing")
def pricing_resource() -> str:
    """Current pricing for all Corpo services."""
    data = _api("GET", "/api/v1/pricing")
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    mcp.run()
