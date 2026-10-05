"""
In-Repo Universal Specification & Documentation Synchronizer
Solves the Ephemeral Artifact Defect and Multi-Machine Memory Silo:
1. Mirrors all IDE brain artifacts and reports into permanent, version-controlled git directories:
   - docs/plans/          (Feature Implementation Plans)
   - docs/walkthroughs/   (Execution Walkthroughs & Test Proofs)
   - docs/audits/         (Adversarial Security Audits & System Readiness)
   - docs/decisions/      (Enterprise Architecture Decisions)
   - docs/research/       (Multi-Hop Research Triangulation Dossiers)
   - docs/specifications/ (Formal API & Data Model Contracts)
2. Maintains living INDEX.md catalogs in each directory.
3. Dual-persists to SQLite Memory Vault and git-mergeable append-only JSONL (.agents/memory/vault/records.jsonl).
"""

import os
import sys
import time
import json
import sqlite3
from typing import Dict, Any, Optional, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


DOCUMENT_CONFIGS: Dict[str, Dict[str, str]] = {
    "plan": {
        "dir": "docs/plans",
        "kind": "Plan",
        "index_title": "Enterprise Plan Documentation Index",
        "description": "Permanent records of all planned feature architectures."
    },
    "walkthrough": {
        "dir": "docs/walkthroughs",
        "kind": "Walkthrough",
        "index_title": "Enterprise Walkthrough Documentation Index",
        "description": "Permanent records of all executed changes and empirical test results."
    },
    "audit": {
        "dir": "docs/audits",
        "kind": "Audit",
        "index_title": "Enterprise Audit Documentation Index",
        "description": "Permanent records of adversarial pentests, code audits, and system readiness."
    },
    "decision": {
        "dir": "docs/decisions",
        "kind": "Decision",
        "index_title": "Enterprise Architecture Decisions",
        "description": "Permanent records of fundamental architectural choices, trade-offs, and moats."
    },
    "research": {
        "dir": "docs/research",
        "kind": "Research",
        "index_title": "Enterprise Deep Research Dossiers",
        "description": "Multi-hop research triangulation on statutory mandates, competitor benchmarks, and CVEs."
    },
    "specification": {
        "dir": "docs/specifications",
        "kind": "Specification",
        "index_title": "Contract & Interface Specifications",
        "description": "Formal typed interface schemas, state machine models, and API definitions."
    }
}

DOC_TYPE_ALIASES: Dict[str, str] = {
    "adr": "decision",
    "adrs": "decision",
    "decision": "decision",
    "decisions": "decision",
    "rfc": "specification",
    "rfcs": "specification",
    "specification": "specification",
    "specifications": "specification",
    "plan": "plan",
    "plans": "plan",
    "walkthrough": "walkthrough",
    "walkthroughs": "walkthrough",
    "audit": "audit",
    "audits": "audit",
    "research": "research"
}


class SpecSync:
    """
    Universal documentation engine synchronizing all enterprise document classes into durable git storage.
    """

    @classmethod
    def _extract_title_and_slug(cls, content: str, default_name: str) -> tuple[str, str]:
        """Extracts human-meaningful title and slug from the first markdown heading."""
        import re
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("# "):
                raw_title = line[2:].strip()
                clean_title = re.sub(r'^[A-Za-z\s]+:\s*', '', raw_title)
                slug = re.sub(r'[^a-zA-Z0-9_]', '_', clean_title.lower()).strip('_')
                slug = re.sub(r'_+', '_', slug)
                words = [w for w in slug.split('_') if w and w not in ["and", "or", "the", "for", "with", "in", "to", "of", "a", "an"]][:4]
                slug_short = "_".join(words) if words else default_name
                return raw_title, slug_short
        return default_name, default_name

    @classmethod
    def persist_document(
        cls,
        doc_type: str,
        name: str,
        content: str,
        title: Optional[str] = None,
        custom_timestamp: Optional[float] = None
    ) -> str:
        doc_type_clean = DOC_TYPE_ALIASES.get(doc_type.lower().strip(), doc_type.lower().strip())
        config = DOCUMENT_CONFIGS.get(doc_type_clean)
        if not config:
            raise ValueError(f"Unknown document type '{doc_type}'. Supported: {list(DOCUMENT_CONFIGS.keys())}")

        target_dir = os.path.join(os.getcwd(), config["dir"])
        os.makedirs(target_dir, exist_ok=True)

        import re
        epoch_time = custom_timestamp if custom_timestamp is not None else time.time()
        time_struct = time.localtime(epoch_time)
        timestamp_prefix = time.strftime("%Y-%m-%d_%H-%M-%S", time_struct)
        display_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)

        # Smart title and slug extraction
        extracted_title, extracted_slug = cls._extract_title_and_slug(content, name)
        final_title = title or extracted_title or name
        final_slug = extracted_slug if name in ["active_feature", "feature", "document", "unnamed"] else re.sub(r'[^a-zA-Z0-9_]', '_', name.lower()).strip('_')
        final_slug = re.sub(r'_+', '_', final_slug)

        filename = f"{timestamp_prefix}_{final_slug}_{doc_type_clean}.md"
        target_path = os.path.join(target_dir, filename)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Update living index catalog with real-time timestamp (YYYY-MM-DD HH:MM:SS)
        cls._update_index(target_dir, config["kind"], final_slug, filename, final_title, config, display_timestamp)

        # Dual-record in SQLite vault and git-mergeable JSONL
        cls._record_in_vault(f"{config['kind']}: {final_title}", doc_type_clean, content, target_path)

        print(f"[SpecSync] Persisted {config['kind']} -> {config['dir']}/{filename}")
        return target_path

    @classmethod
    def persist_plan(cls, name: str, content: str, title: Optional[str] = None, custom_timestamp: Optional[float] = None) -> str:
        return cls.persist_document("plan", name, content, title, custom_timestamp)

    @classmethod
    def persist_walkthrough(cls, name: str, content: str, title: Optional[str] = None, custom_timestamp: Optional[float] = None) -> str:
        return cls.persist_document("walkthrough", name, content, title, custom_timestamp)

    @classmethod
    def persist_audit(cls, name: str, content: str, title: Optional[str] = None, custom_timestamp: Optional[float] = None) -> str:
        return cls.persist_document("audit", name, content, title, custom_timestamp)

    @classmethod
    def persist_decision(cls, name: str, content: str, title: Optional[str] = None, custom_timestamp: Optional[float] = None) -> str:
        return cls.persist_document("decision", name, content, title, custom_timestamp)

    @classmethod
    def persist_adr(cls, name: str, content: str, title: Optional[str] = None, custom_timestamp: Optional[float] = None) -> str:
        """Backward-compatible alias for persist_decision."""
        return cls.persist_decision(name, content, title, custom_timestamp)

    @classmethod
    def persist_research(cls, name: str, content: str, title: Optional[str] = None, custom_timestamp: Optional[float] = None) -> str:
        return cls.persist_document("research", name, content, title, custom_timestamp)

    @classmethod
    def persist_specification(cls, name: str, content: str, title: Optional[str] = None, custom_timestamp: Optional[float] = None) -> str:
        return cls.persist_document("specification", name, content, title, custom_timestamp)

    @classmethod
    def persist_rfc(cls, name: str, content: str, title: Optional[str] = None, custom_timestamp: Optional[float] = None) -> str:
        """Backward-compatible alias for persist_specification."""
        return cls.persist_specification(name, content, title, custom_timestamp)

    @classmethod
    def get_all_indexes(cls) -> Dict[str, Dict[str, Any]]:
        """Returns the status, path, and entry counts for all 6 living index catalogs."""
        results = {}
        for doc_type, config in DOCUMENT_CONFIGS.items():
            base_dir = os.path.join(os.getcwd(), config["dir"])
            index_path = os.path.join(base_dir, "INDEX.md")
            exists = os.path.exists(index_path)
            doc_files = [
                f for f in os.listdir(base_dir)
                if f.endswith(".md") and f != "INDEX.md" and f != "README.md"
            ] if os.path.exists(base_dir) else []
            results[doc_type] = {
                "kind": config["kind"],
                "dir": config["dir"],
                "index_path": index_path,
                "index_exists": exists,
                "document_count": len(doc_files),
                "documents": sorted(doc_files)
            }
        return results

    @classmethod
    def sync_brain_artifacts(cls, brain_dir: Optional[str] = None, feature_name: Optional[str] = None) -> List[str]:
        """
        Automatically scans the IDE brain artifacts directory and mirrors:
        - implementation_plan.md -> docs/plans/
        - walkthrough.md        -> docs/walkthroughs/
        - *_audit.md            -> docs/audits/
        into permanent git-tracked storage with real-time timestamps (min & sec),
        updating living INDEX catalogs and the SQLite Memory Vault.
        """
        synced_files: List[str] = []
        search_dirs: List[str] = []
        if brain_dir and os.path.exists(brain_dir):
            search_dirs.append(brain_dir)
        else:
            app_data = os.path.expanduser(r"~\.gemini\antigravity-ide\brain")
            if os.path.exists(app_data):
                conv_dirs = sorted(
                    [os.path.join(app_data, d) for d in os.listdir(app_data) if os.path.isdir(os.path.join(app_data, d))],
                    key=lambda p: os.path.getmtime(p),
                    reverse=True
                )
                search_dirs.extend(conv_dirs[:3])

        feat = feature_name or "active_feature"
        for bdir in search_dirs:
            # 1. Implementation Plans and any *_plan.md
            for fname in os.listdir(bdir):
                if fname.endswith(("_plan.md", "-plan.md")) or fname == "implementation_plan.md":
                    fpath = os.path.join(bdir, fname)
                    if os.path.isfile(fpath):
                        with open(fpath, "r", encoding="utf-8") as f:
                            content = f.read()
                        if content.strip():
                            mtime = os.path.getmtime(fpath)
                            plan_name = fname.replace(".md", "").replace("_plan", "")
                            title, slug = cls._extract_title_and_slug(content, plan_name)
                            dest = cls.persist_plan(slug, content, title, custom_timestamp=mtime)
                            synced_files.append(dest)

            # 2. Walkthrough and any *_walkthrough.md
            for fname in os.listdir(bdir):
                if fname.endswith(("_walkthrough.md", "-walkthrough.md")) or fname == "walkthrough.md":
                    wpath = os.path.join(bdir, fname)
                    if os.path.isfile(wpath):
                        with open(wpath, "r", encoding="utf-8") as f:
                            content = f.read()
                        if content.strip():
                            mtime = os.path.getmtime(wpath)
                            walk_name = fname.replace(".md", "").replace("_walkthrough", "")
                            title, slug = cls._extract_title_and_slug(content, walk_name or feat)
                            dest = cls.persist_walkthrough(slug, content, title, custom_timestamp=mtime)
                            synced_files.append(dest)

            # 3. Audits and any *_audit.md
            for fname in os.listdir(bdir):
                if fname.endswith(("_audit.md", "-audit.md")) and not fname.endswith(("_plan.md", "-plan.md")):
                    fpath = os.path.join(bdir, fname)
                    if os.path.isfile(fpath):
                        with open(fpath, "r", encoding="utf-8") as f:
                            content = f.read()
                        if content.strip():
                            mtime = os.path.getmtime(fpath)
                            audit_name = fname.replace(".md", "").replace("_audit", "")
                            title, slug = cls._extract_title_and_slug(content, audit_name)
                            dest = cls.persist_audit(slug, content, title, custom_timestamp=mtime)
                            synced_files.append(dest)

        return synced_files

    @classmethod
    def _update_index(
        cls,
        base_dir: str,
        kind: str,
        feature: str,
        filename: str,
        title: str,
        config: Dict[str, str],
        timestamp_str: Optional[str] = None
    ) -> None:
        index_file = os.path.join(base_dir, "INDEX.md")
        ts = timestamp_str or time.strftime("%Y-%m-%d %H:%M:%S")

        # Resolve active domain
        state_file = os.path.join(os.getcwd(), ".agents", "state", "active-domain.json")
        active_domain = "software"
        if os.path.exists(state_file):
            try:
                with open(state_file, "r", encoding="utf-8") as sf:
                    active_domain = json.load(sf).get("domain_id", "software")
            except Exception:
                pass

        entry = f"- **{ts}** | [{title}]({filename}) | *Scope: {feature}* | *Domain: `{active_domain}`*\n"

        if not os.path.exists(index_file):
            with open(index_file, "w", encoding="utf-8") as f:
                f.write(f"# {config['index_title']}\n\n> {config['description']}\n\n")

        # Check if entry already exists
        with open(index_file, "r", encoding="utf-8") as f:
            existing_content = f.read()

        if filename not in existing_content:
            with open(index_file, "a", encoding="utf-8") as f:
                f.write(entry)

    @classmethod
    def _record_in_vault(cls, title: str, kind: str, content: str, file_path: str) -> None:
        # Resolve active domain
        state_file = os.path.join(os.getcwd(), ".agents", "state", "active-domain.json")
        active_domain = "software"
        if os.path.exists(state_file):
            try:
                with open(state_file, "r", encoding="utf-8") as sf:
                    active_domain = json.load(sf).get("domain_id", "software")
            except Exception:
                pass

        # 1. Dual-Write to Git-Mergeable Append-Only JSONL
        jsonl_dir = os.path.join(os.getcwd(), ".agents", "memory", "vault")
        os.makedirs(jsonl_dir, exist_ok=True)
        jsonl_path = os.path.join(jsonl_dir, "records.jsonl")

        record = {
            "id": f"doc-{int(time.time())}-{abs(hash(title)) % 10000}",
            "title": title,
            "kind": kind,
            "domain_id": active_domain,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "file_path": file_path,
            "preview": content[:400]
        }

        try:
            with open(jsonl_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception:
            pass

        # 2. Record in Local SQLite FTS5 for Fast Text Search
        db_path = os.path.join(os.getcwd(), ".agents", "memory", "vault.sqlite")
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    scope TEXT NOT NULL,
                    phase INTEGER NOT NULL,
                    operator TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    body TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    domain_id TEXT DEFAULT 'software'
                );
            """)
            try:
                cur.execute("ALTER TABLE memories ADD COLUMN domain_id TEXT DEFAULT 'software'")
            except Exception:
                pass
            cur.execute("""
                INSERT OR REPLACE INTO memories 
                (id, title, kind, scope, phase, operator, tags, created_at, body, file_path, domain_id)
                VALUES (?, ?, ?, 'project', 1, 'SpecSync', ?, datetime('now'), ?, ?, ?);
            """, (record["id"], title, kind, f"doc,{kind},{active_domain}", content[:600], file_path, active_domain))
            conn.commit()
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SpecSync Universal Documentation Engine")
    parser.add_argument("--type", choices=list(DOCUMENT_CONFIGS.keys()), help="Document category")
    parser.add_argument("--name", help="Feature or document name")
    parser.add_argument("--file", help="Source file to read content from")
    parser.add_argument("--title", help="Human-readable title")
    parser.add_argument("--all-indexes", action="store_true", help="Print summary of all 6 living index catalogs")
    parser.add_argument("--sync-brain", nargs="?", const="AUTO", help="Sync brain artifacts directory into in-repo docs/")
    args = parser.parse_args()

    if args.all_indexes:
        indexes = SpecSync.get_all_indexes()
        print("\n=== In-Repo Living Documentation Catalogs (6 Document Classes) ===")
        for doc_type, info in indexes.items():
            status = "ACTIVE" if info["index_exists"] else "MISSING"
            print(f"  [{info['kind'].upper():<11}] {info['dir']:<18} | {status} | {info['document_count']} docs | Index: {info['index_path']}")
        print("==================================================================\n")
        sys.exit(0)

    if args.sync_brain:
        target_brain = args.sync_brain
        if target_brain == "AUTO":
            app_data = os.path.expanduser(r"~\.gemini\antigravity-ide\brain")
            if os.path.exists(app_data):
                dirs = [
                    os.path.join(app_data, d) for d in os.listdir(app_data)
                    if os.path.isdir(os.path.join(app_data, d)) and not d.startswith(".") and d != "tempmediaStorage"
                ]
                dirs.sort(key=lambda p: os.path.getmtime(p), reverse=True)
                target_brain = dirs[0] if dirs else None

        if target_brain and os.path.exists(target_brain):
            synced = SpecSync.sync_brain_artifacts(target_brain, args.name)
            print(f"[SpecSync] Synchronized {len(synced)} document(s) from brain artifacts ({target_brain}).")
        else:
            print("[SpecSync] No active brain directory found to synchronize.")
        sys.exit(0)

    if not args.name:
        parser.error("--name is required unless using --all-indexes or --sync-brain")

    content = ""
    if args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = f"# {args.title or args.name}\n\nDocument persisted via SpecSync CLI.\n"

    SpecSync.persist_document(args.type or "plan", args.name, content, args.title)
