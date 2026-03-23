#!/bin/bash
# form-entity.sh — Form a Wyoming DAO LLC in one command
# Usage: ./form-entity.sh "My Entity LAO"
# Requires: curl, jq
#
# This creates an account, gets a quote, pays (test mode), submits,
# and verifies — all in ~30 seconds.

set -euo pipefail

CORPO="https://api.corpo.llc"
ENTITY_NAME="${1:-}"

if [ -z "$ENTITY_NAME" ]; then
  echo "Usage: $0 \"Your Entity Name LAO\""
  echo ""
  echo "Examples:"
  echo "  $0 \"Sentinel Protocol LAO\""
  echo "  $0 \"Nexus Ventures LAO\""
  echo "  $0 \"Digital Horizon LAO\""
  echo ""
  echo "Note: Name must end in 'LAO' (Wyoming DAO LLC requirement)."
  exit 1
fi

# Validate LAO suffix
if [[ ! "$ENTITY_NAME" =~ LAO$ ]]; then
  echo "❌ Entity name must end in 'LAO'"
  echo "   Example: \"${ENTITY_NAME} LAO\""
  exit 1
fi

echo "🏛️  Corpo — Wyoming DAO LLC Formation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Create account
echo "1️⃣  Creating account..."
ACCOUNT=$(curl -s -X POST "$CORPO/api/v1/accounts" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Formation User\"}")

API_KEY=$(echo "$ACCOUNT" | jq -r '.api_key')
ACCOUNT_ID=$(echo "$ACCOUNT" | jq -r '.account_id')

if [ "$API_KEY" = "null" ] || [ -z "$API_KEY" ]; then
  echo "❌ Account creation failed:"
  echo "$ACCOUNT" | jq .
  exit 1
fi
echo "   ✅ Account: $ACCOUNT_ID"
echo "   🔑 API Key: ${API_KEY:0:20}..."
echo ""

# Step 2: Get quote (also creates formation draft)
echo "2️⃣  Getting quote for: $ENTITY_NAME"
QUOTE=$(curl -s -X POST "$CORPO/api/v1/quotes" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{\"entity_name\":\"$ENTITY_NAME\",\"entity_type\":\"dao_llc\",\"state\":\"WY\"}")

STATUS=$(echo "$QUOTE" | jq -r '.status')
QUOTE_ID=$(echo "$QUOTE" | jq -r '.quote_id')

if [ "$STATUS" = "name_unavailable" ]; then
  echo "❌ Name unavailable:"
  echo "$QUOTE" | jq '.errors // empty'
  exit 1
fi

PRICE=$(echo "$QUOTE" | jq -r '.pricing.total_display')
echo "   ✅ Quote: $QUOTE_ID"
echo "   💰 Price: $PRICE"
echo "   📋 Type: Wyoming DAO LLC"
echo "   ⚖️  Governance: Algorithmic (Solana Realms)"
echo ""

# Step 3: Pay
echo "3️⃣  Processing payment (test mode)..."
PAY=$(curl -s -X POST "$CORPO/api/v1/quotes/$QUOTE_ID/pay" \
  -H "Authorization: Bearer $API_KEY")

PAY_STATUS=$(echo "$PAY" | jq -r '.status')
echo "   ✅ Payment: $PAY_STATUS"
echo ""

# Step 4: Check entity (payment triggers formation in staging)
echo "4️⃣  Checking entity..."
ENTITIES=$(curl -s "$CORPO/api/v1/entities" \
  -H "Authorization: Bearer $API_KEY")
echo "$ENTITIES" | jq '.[0] // "Pending — entity will appear after filing completes"'
echo ""

# Step 5: Verify (if entity exists)
ENTITY_ID=$(echo "$ENTITIES" | jq -r '.[0].id // empty')
if [ -n "$ENTITY_ID" ]; then
  echo "5️⃣  Public verification (no auth required)..."
  VERIFY=$(curl -s "$CORPO/api/v1/entities/$ENTITY_ID/verify")
  echo "$VERIFY" | jq .
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "✅ Entity formed and verifiable!"
  echo "🔗 Verify: $CORPO/api/v1/entities/$ENTITY_ID/verify"
else
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📋 Formation submitted! Entity will be created after filing."
  echo "🔑 Your API key: $API_KEY"
  echo "   Use it to check: curl $CORPO/api/v1/entities -H 'Authorization: Bearer $API_KEY'"
fi

echo ""
echo "🏛️  Corpo — Legal infrastructure for AI agents"
echo "   https://api.corpo.llc"
