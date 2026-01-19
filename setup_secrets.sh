#!/bin/bash

# Script to set up GitHub secrets for kids-routines repository

echo "🔐 Setting up GitHub Secrets for kids-routines"
echo "=============================================="
echo ""

REPO="anna-xheads/kids-routines"

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    exit 1
fi

echo "📝 Setting SERVICE_ACCOUNT_JSON..."
if [ -f "secrets/service_account.json" ]; then
    gh secret set SERVICE_ACCOUNT_JSON --repo "$REPO" < secrets/service_account.json
    echo "   ✅ SERVICE_ACCOUNT_JSON set"
else
    echo "   ❌ secrets/service_account.json not found"
fi

echo ""
echo "📝 Setting GREEN_API_INSTANCE_ID..."
gh secret set GREEN_API_INSTANCE_ID --repo "$REPO" --body "7105233428"
echo "   ✅ GREEN_API_INSTANCE_ID set"

echo ""
echo "📝 Setting GREEN_API_TOKEN..."
gh secret set GREEN_API_TOKEN --repo "$REPO" --body "01be127289a24d33871059257b7c6ac6fac9a551f1e5425db7"
echo "   ✅ GREEN_API_TOKEN set"

echo ""
echo "=============================================="
echo "✅ All secrets configured!"
echo "=============================================="
echo ""
echo "You can verify the secrets at:"
echo "https://github.com/$REPO/settings/secrets/actions"
