#!/usr/bin/env bash
set -euo pipefail

# Node 22.23+ ships node:sqlite with FTS5 (required for skill registry search).
# Cloud VMs may expose /exec-daemon/node 22.14 without FTS5; prefer /usr/local/bin.
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [[ ! -s "$NVM_DIR/nvm.sh" ]]; then
  curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
fi
# shellcheck source=/dev/null
source "$NVM_DIR/nvm.sh"
if ! nvm ls 22.23.3 >/dev/null 2>&1; then
  nvm install 22.23.3
fi
nvm alias default 22.23.3 >/dev/null 2>&1 || true
NODE_BIN="$(nvm which 22.23.3)"
sudo ln -sf "$NODE_BIN" /usr/local/bin/node
sudo ln -sf "$(dirname "$NODE_BIN")/npm" /usr/local/bin/npm
sudo ln -sf "$(dirname "$NODE_BIN")/npx" /usr/local/bin/npx

export PATH="/usr/local/bin:${PATH}"

ROOT="${CURSOR_WORKSPACE:-/workspace}"
cd "$ROOT"

npm ci
npx playwright install chromium
if command -v sudo >/dev/null 2>&1; then
  npx playwright install-deps chromium 2>/dev/null || sudo npx playwright install-deps chromium || true
fi
npm run harness:sync
