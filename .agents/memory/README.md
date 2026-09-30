# Durable Memory Vault (`.agents/memory/`)

This directory houses the persistent, cross-phase architectural knowledge store ensuring continuous learnings across tasks, sessions, and machines.

## Architecture
- `vault.sqlite`: Local SQLite database providing indexed full-text search across decisions, lessons, and handoffs.
- `vault/records.jsonl`: Git-mergeable append-only journal replicating memory records across git remotes.
- `project/`: Project-specific architectural memories (decisions, facts, handoffs, lessons, runbooks).
- `team/`: Shared team memories synchronized across all workstation operators.

## Commands
- `npm run memory:save`: Save a new architectural learning or decision.
- `npm run memory:search`: Search historical decisions by keyword.
- `npm run memory:doctor`: Verify SQLite database and file-system consistency.
