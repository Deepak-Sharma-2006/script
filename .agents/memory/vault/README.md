# Vault Journal Directory

This directory stores the git-synchronized append-only journal (`records.jsonl`) used for multi-machine memory replication without SQLite binary merge conflicts.

## Mechanism
When a new memory is recorded via `scripts/memory-vault.ts` or `spec_sync.py`, it is indexed in `vault.sqlite` locally and appended as a single JSON line to `records.jsonl`.
