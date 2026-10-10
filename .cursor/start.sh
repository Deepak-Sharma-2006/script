#!/usr/bin/env bash
set -euo pipefail

export PATH="/usr/local/bin:${PATH}"
ROOT="${CURSOR_WORKSPACE:-/workspace}"
cd "$ROOT"
LOG_DIR="/tmp/cursor/workbench"
mkdir -p "$LOG_DIR"

wait_for_port() {
  local port="$1"
  local tries="${2:-60}"
  for _ in $(seq 1 "$tries"); do
    if curl -sf "http://127.0.0.1:${port}/api/status" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  return 1
}

TMUX=(tmux -f /exec-daemon/tmux.portal.conf)

if ! wait_for_port 3042 2; then
  if ! "${TMUX[@]}" has-session -t workbench 2>/dev/null; then
    "${TMUX[@]}" new-session -d -s workbench -c "$ROOT" -- "${SHELL:-bash}" -l -c \
      "export PATH=/usr/local/bin:\$PATH; exec node --experimental-strip-types scripts/workbench-server.ts --port 3042 2>&1 | tee ${LOG_DIR}/workbench.log"
  fi
  wait_for_port 3042 90 || {
    echo "Workbench failed to become ready on port 3042" >&2
    tail -n 40 "${LOG_DIR}/workbench.log" 2>/dev/null || true
    exit 1
  }
fi

echo "Workbench ready at http://127.0.0.1:3042"
