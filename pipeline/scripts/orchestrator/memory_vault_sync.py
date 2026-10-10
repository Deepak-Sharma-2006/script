"""
Dual-Tier Distributed Memory Vault Synchronization Engine (INV-06 / Stage 5)

Synchronizes Git-tracked Markdown decision records (.agents/memory/decisions/)
and handoff manifests (.agents/memory/handoffs/) into the local SQLite FTS5 virtual table
(.agents/memory/vault.sqlite) for fast, millisecond full-text and semantic search.
"""

import os
import sys
import glob
import sqlite3
import hashlib
from typing import List, Dict, Any, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_ROOT = os.getcwd()
DB_PATH = os.path.join(WORKSPACE_ROOT, ".agents", "memory", "vault.sqlite")
DECISIONS_DIR = os.path.join(WORKSPACE_ROOT, ".agents", "memory", "decisions")
HANDOFFS_DIR = os.path.join(WORKSPACE_ROOT, ".agents", "handoffs")

class MemoryVaultSync:
    """Manages SQLite FTS5 full-text indexing of Git-tracked memory files."""

    @classmethod
    def init_database(cls) -> sqlite3.Connection:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                category TEXT,
                title TEXT,
                content TEXT,
                file_path TEXT,
                sha256 TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Migrate existing schema if missing columns
        cursor.execute("PRAGMA table_info(memories)")
        cols = {row[1] for row in cursor.fetchall()}
        if "sha256" not in cols:
            cursor.execute("ALTER TABLE memories ADD COLUMN sha256 TEXT")
        if "file_path" not in cols:
            cursor.execute("ALTER TABLE memories ADD COLUMN file_path TEXT")
        if "category" not in cols:
            cursor.execute("ALTER TABLE memories ADD COLUMN category TEXT")
        if "content" not in cols:
            cursor.execute("ALTER TABLE memories ADD COLUMN content TEXT")

        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                title,
                content,
                category,
                content='memories',
                content_rowid='rowid'
            )
        """)
        conn.commit()
        return conn

    @classmethod
    def sync_all(cls) -> Dict[str, Any]:
        conn = cls.init_database()
        cursor = conn.cursor()

        os.makedirs(DECISIONS_DIR, exist_ok=True)
        os.makedirs(HANDOFFS_DIR, exist_ok=True)

        decision_files = glob.glob(os.path.join(DECISIONS_DIR, "*.md"))
        handoff_files = glob.glob(os.path.join(HANDOFFS_DIR, "*.json"))
        all_files = decision_files + handoff_files

        indexed_count = 0
        updated_count = 0

        for fpath in all_files:
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue

            file_sha = hashlib.sha256(content.encode()).hexdigest()
            file_name = os.path.basename(fpath)
            category = "decision" if fpath.endswith(".md") else "handoff"

            cursor.execute("SELECT sha256 FROM memories WHERE file_path = ?", (fpath,))
            row = cursor.fetchone()

            if row and row[0] == file_sha:
                continue  # Clean cache hit

            cursor.execute("""
                INSERT OR REPLACE INTO memories (id, title, kind, scope, phase, operator, tags, created_at, body, file_path, domain_id, sha256, category, content)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?)
            """, (file_name, file_name, category, "project", 1, "system", "git-sync,architecture", content, fpath, "system", file_sha, category, content))

            if row:
                updated_count += 1
            else:
                indexed_count += 1

        # Rebuild FTS5 index if changes occurred
        if indexed_count > 0 or updated_count > 0:
            cursor.execute("INSERT INTO memories_fts(memories_fts) VALUES('rebuild')")
            conn.commit()

        conn.close()
        return {
            "total_files_scanned": len(all_files),
            "newly_indexed": indexed_count,
            "updated": updated_count,
            "db_path": DB_PATH
        }

    @classmethod
    def search(cls, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not os.path.exists(DB_PATH):
            cls.sync_all()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT m.title, m.category, snippet(memories_fts, 1, '<b>', '</b>', '...', 25), m.file_path
                FROM memories_fts f
                JOIN memories m ON f.rowid = m.rowid
                WHERE memories_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit))
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "title": r[0],
                    "category": r[1],
                    "snippet": r[2],
                    "file_path": r[3]
                })
            conn.close()
            return results
        except Exception:
            conn.close()
            return []


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--search":
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "phase"
        res = MemoryVaultSync.search(q)
        print(f"🔍 Memory Vault Search Results for: '{q}':")
        for item in res:
            print(f"   • [{item['category']}] {item['title']} -> {item['snippet']}")
    else:
        res = MemoryVaultSync.sync_all()
        print(f"✅ [Memory Vault Sync] Scanned: {res['total_files_scanned']} files | Indexed: {res['newly_indexed']} | Updated: {res['updated']}")

if __name__ == "__main__":
    main()
