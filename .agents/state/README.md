# Active Runtime State & Distributed Locks

This directory contains dynamic coordination state files governing multi-persona and multi-developer operation.

## Files & Subdirectories
- `active-role.json`: Operating mode indicator (Solo, Dual 50/50, or Team Mesh).
- `active-model.json`: Currently configured LLM model and context window profile.
- `locks/`: Directory where domain lease locks (`<domain>.lock.json`) are maintained.
- `metrics/`: Token consumption records and session token budget metrics.
