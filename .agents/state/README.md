# Active Runtime State & Distributed Locks

This directory contains dynamic coordination state files governing multi-persona and multi-developer operation.

## Files & Subdirectories
- `active-role.json`: Operating mode indicator (Mode 1: Deep Surge, Mode 2: Portfolio Multiplexing, Mode 3: Collaborative Team).
- `active-model.json`: Currently configured LLM model and context window profile.
- `locks/`: Directory where domain lease locks (`<domain>.lock.json`) are maintained.
- `metrics/`: Token consumption records and session token budget metrics.
