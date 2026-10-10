"""
Memory Retriever CLI and Engine (INV-06 / Stage 5)

Connects to the dual-tier SQLite Memory Vault (vault.sqlite) with automatic
failover to Markdown synchronization via MemoryVaultSync.
Provides full-text search, snippet ranking, and CLI output.
"""

import os
import sys
import argparse
from typing import List, Dict, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.orchestrator.memory_vault_sync import MemoryVaultSync, DB_PATH

class MemoryRetriever:
    """Retrieves decisions, handoffs, and architectural learnings from the SQLite memory vault."""

    @classmethod
    def search(cls, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Searches the SQLite memory vault using FTS5, auto-syncing if empty or missing."""
        if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
            MemoryVaultSync.sync_all()

        results = MemoryVaultSync.search(query, limit=limit)
        if not results:
            # Try re-syncing once in case files were recently added
            MemoryVaultSync.sync_all()
            results = MemoryVaultSync.search(query, limit=limit)

        return results

    @classmethod
    def format_results_markdown(cls, query: str, results: List[Dict[str, Any]]) -> str:
        """Formats search results as clean markdown."""
        if not results:
            return f"### Memory Search: `{query}`\n\n*No matching memories found in SQLite Memory Vault.*"

        lines = [f"### Memory Search Results for: `{query}` ({len(results)} matches)\n"]
        for i, r in enumerate(results, 1):
            title = r.get("title", "Untitled")
            cat = (r.get("category") or "general").upper()
            snip = (r.get("snippet") or "").replace("\n", " ")
            path = r.get("file_path") or ""
            lines.append(f"{i}. **[{cat}] {title}**")
            if path:
                lines.append(f"   - File: `file:///{path.replace(os.sep, '/')}`")
            lines.append(f"   - Match: {snip}\n")

        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Search SQLite Memory Vault with FTS5")
    parser.add_argument("query", nargs="?", default="", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Maximum results to return")
    parser.add_argument("--sync", action="store_true", help="Force synchronization before searching")
    args = parser.parse_args()

    if args.sync or not args.query:
        sync_res = MemoryVaultSync.sync_all()
        print(f"✅ [Memory Vault] Synchronized {sync_res['total_files_scanned']} files ({sync_res['newly_indexed']} indexed, {sync_res['updated']} updated).")
        if not args.query:
            return

    results = MemoryRetriever.search(args.query, limit=args.limit)
    print(MemoryRetriever.format_results_markdown(args.query, results))

if __name__ == "__main__":
    main()
