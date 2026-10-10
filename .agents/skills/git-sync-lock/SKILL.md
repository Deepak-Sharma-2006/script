---
name: git-sync-lock
description: >-
  Coordinates distributed lease locking and role handoffs across collaborating team workstations in Mode 3 (Collaborative Team Mode).
  Use this skill to inspect active locks, acquire exclusive domain leases, or transfer phase ownership
  to prevent concurrent write collisions.
---

# Distributed Lease Locking & Role Coordination

This skill provides conflict-free distributed collaboration across collaborating team workstations in Mode 3 (Collaborative Team Mode).

## Commands

- **Check Active Locks**:
  ```bash
  npx ts-node scripts/lock-manager.ts status
  ```
- **Acquire Domain Lease**:
  ```bash
  npx ts-node scripts/lock-manager.ts acquire --domain <domain> --operator <name> --ttl 3600
  ```
- **Transfer Domain Lease (Phase Handoff)**:
  ```bash
  npx ts-node scripts/lock-manager.ts transfer --domain <domain> --to <operator>
  ```
- **Release Lease**:
  ```bash
  npx ts-node scripts/lock-manager.ts release --domain <domain> --operator <name>
  ```

## Safety Rule
An agent must NEVER edit files in a domain that is currently leased to another operator without an explicit handoff transfer.
