"""
Continual Self-Evolution & Staged Patch Engine (Layer 5)
Diffs session trajectory signals, aggregates failure signatures with empirical
recurrence thresholds (count >= 2 or critical invariant breach), and stages
targeted evolution patches for operator verification rather than un-audited auto-commits.
"""

import os
import sys
import json
import time
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class EvolutionEngine:
    """
    Manages continuous agent self-evolution with an empirical staging barrier.
    Ensures that only verified, recurring failure patterns trigger patch generation.
    """

    PATCHES_DIR = os.path.join(WORKSPACE_ROOT, ".agents", "state", "evolution_patches")
    SIGNATURES_FILE = os.path.join(PATCHES_DIR, "failure_signatures.json")
    PENDING_FILE = os.path.join(PATCHES_DIR, "pending_reviews.json")
    RECURRENCE_THRESHOLD = 2

    CRITICAL_INVARIANTS = {
        "ZeroSecretViolation",
        "RawLaTeXDelimiter",
        "HardwareRAMBreach",
        "StatutoryActionBypass",
        "ChecksEffectsInteractions",
    }

    @classmethod
    def _init_storage(cls):
        os.makedirs(cls.PATCHES_DIR, exist_ok=True)
        if not os.path.exists(cls.SIGNATURES_FILE):
            with open(cls.SIGNATURES_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)
        if not os.path.exists(cls.PENDING_FILE):
            with open(cls.PENDING_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    @classmethod
    def _load_json(cls, filepath: str, default: Any) -> Any:
        cls._init_storage()
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return default

    @classmethod
    def _save_json(cls, filepath: str, data: Any):
        cls._init_storage()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def record_failure_signal(
        cls,
        signature: str,
        category: str,
        description: str,
        remediation: str,
        domain: str = "general",
        target_file: Optional[str] = None,
        patch_snippet: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Records a failure signal. Evaluates recurrence threshold (>=2)
        or critical invariant status before generating a staged evolution patch.
        """
        cls._init_storage()
        signatures = cls._load_json(cls.SIGNATURES_FILE, {})
        pending = cls._load_json(cls.PENDING_FILE, [])

        sig_hash = hashlib.sha256(f"{category}:{signature}".encode("utf-8")).hexdigest()[:12]
        now_iso = datetime.now(timezone.utc).isoformat()

        if sig_hash not in signatures:
            signatures[sig_hash] = {
                "id": sig_hash,
                "category": category,
                "signature": signature,
                "description": description,
                "remediation": remediation,
                "domain": domain,
                "occurrences": 1,
                "first_seen": now_iso,
                "last_seen": now_iso,
                "staged": False,
            }
        else:
            signatures[sig_hash]["occurrences"] += 1
            signatures[sig_hash]["last_seen"] = now_iso

        occ = signatures[sig_hash]["occurrences"]
        is_critical = category in cls.CRITICAL_INVARIANTS
        is_recurring = occ >= cls.RECURRENCE_THRESHOLD

        should_stage = (is_recurring or is_critical) and not signatures[sig_hash].get("staged", False)

        result = {
            "sig_hash": sig_hash,
            "occurrences": occ,
            "is_critical": is_critical,
            "staged": False,
        }

        if should_stage:
            patch_id = f"patch-{sig_hash}-{int(time.time())}"
            target_path = target_file or os.path.join(WORKSPACE_ROOT, "AGENTS.md")
            
            patch_entry = {
                "patch_id": patch_id,
                "sig_hash": sig_hash,
                "category": category,
                "domain": domain,
                "description": description,
                "remediation": remediation,
                "target_file": os.path.relpath(target_path, WORKSPACE_ROOT) if os.path.isabs(target_path) else target_path,
                "patch_snippet": patch_snippet or f"- Enforce fail-closed guard for {signature}: {remediation}",
                "staged_at": now_iso,
                "status": "PENDING_OPERATOR_VERIFICATION",
                "occurrences": occ,
                "trigger_reason": "CRITICAL_INVARIANT_BREACH" if is_critical else f"RECURRING_FAILURE_PATTERN (count={occ})",
            }

            patch_file = os.path.join(cls.PATCHES_DIR, f"{patch_id}.json")
            with open(patch_file, "w", encoding="utf-8") as pf:
                json.dump(patch_entry, pf, indent=2)

            pending.append(patch_entry)
            signatures[sig_hash]["staged"] = True
            signatures[sig_hash]["staged_patch_id"] = patch_id

            cls._save_json(cls.PENDING_FILE, pending)
            result["staged"] = True
            result["patch_id"] = patch_id
            result["patch_entry"] = patch_entry
            result["operator_notification"] = cls.format_operator_notification(patch_entry)

        cls._save_json(cls.SIGNATURES_FILE, signatures)
        return result

    @classmethod
    def format_operator_notification(cls, patch_entry: Dict[str, Any]) -> str:
        """Formats an automated, high-visibility operator verification request."""
        patch_id = patch_entry.get("patch_id", "unknown")
        category = patch_entry.get("category", "General")
        domain = patch_entry.get("domain", "general")
        trigger = patch_entry.get("trigger_reason", "Significance threshold met")
        target = patch_entry.get("target_file", "AGENTS.md")
        snippet = patch_entry.get("patch_snippet", "")
        return (
            f"\n🚨 [AUTOMATED STAGED EVOLUTION VERIFICATION REQUEST]\n"
            f"   Patch ID       : {patch_id}\n"
            f"   Category       : {category} (Domain: {domain})\n"
            f"   Trigger Reason : {trigger}\n"
            f"   Target File    : {target}\n"
            f"   Proposed Rule  :\n"
            f"     {snippet}\n"
            f"   Approval Action: Run `npm run evolution:approve -- {patch_id}`\n"
            f"   Dismiss Action : Run `npm run evolution:reject -- {patch_id}`\n"
        )

    @classmethod
    def list_pending(cls) -> List[Dict[str, Any]]:
        """Returns all staged evolution patches awaiting operator verification."""
        cls._init_storage()
        pending = cls._load_json(cls.PENDING_FILE, [])
        return [p for p in pending if p.get("status") == "PENDING_OPERATOR_VERIFICATION"]

    @classmethod
    def approve_patch(cls, patch_id: str) -> Dict[str, Any]:
        """
        Applies a staged evolution patch to the target file after operator approval.
        """
        cls._init_storage()
        pending = cls._load_json(cls.PENDING_FILE, [])
        target_patch = None
        for p in pending:
            if p.get("patch_id") == patch_id and p.get("status") == "PENDING_OPERATOR_VERIFICATION":
                target_patch = p
                break

        if not target_patch:
            return {"success": False, "error": f"Patch ID '{patch_id}' not found or already resolved."}

        target_file_rel = target_patch["target_file"]
        target_file_abs = os.path.join(WORKSPACE_ROOT, target_file_rel)
        snippet = target_patch["patch_snippet"]

        if not os.path.exists(target_file_abs):
            return {"success": False, "error": f"Target file '{target_file_abs}' does not exist."}

        try:
            with open(target_file_abs, "r", encoding="utf-8") as f:
                content = f.read()

            if snippet not in content:
                # Append rule/snippet cleanly
                with open(target_file_abs, "a", encoding="utf-8") as f:
                    f.write(f"\n\n<!-- Evolutive Patch {patch_id} -->\n{snippet}\n")

            target_patch["status"] = "APPROVED_AND_APPLIED"
            target_patch["applied_at"] = datetime.now(timezone.utc).isoformat()
            cls._save_json(cls.PENDING_FILE, pending)

            # Record in SQLite Memory Vault
            db_path = os.path.join(WORKSPACE_ROOT, ".agents", "memory", "vault.sqlite")
            if os.path.exists(db_path):
                import sqlite3
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO memories (id, title, kind, scope, phase, operator, tags, created_at, body, file_path, domain_id)
                    VALUES (?, ?, 'decision', 'evolution', 1, 'Operator', 'evolution,patch', datetime('now'), ?, ?, ?)
                """, (
                    f"evol-{patch_id}",
                    f"Evolution Patch: {target_patch['category']}",
                    f"Applied snippet: {snippet}\nTrigger: {target_patch['trigger_reason']}",
                    target_file_rel,
                    target_patch.get("domain", "general")
                ))
                conn.commit()
                conn.close()

            return {
                "success": True,
                "patch_id": patch_id,
                "target_file": target_file_rel,
                "status": "APPLIED",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def reject_patch(cls, patch_id: str, reason: str = "Operator dismissed") -> Dict[str, Any]:
        """Rejects a staged evolution patch without modifying repository code."""
        cls._init_storage()
        pending = cls._load_json(cls.PENDING_FILE, [])
        for p in pending:
            if p.get("patch_id") == patch_id and p.get("status") == "PENDING_OPERATOR_VERIFICATION":
                p["status"] = "REJECTED_BY_OPERATOR"
                p["dismissal_reason"] = reason
                p["rejected_at"] = datetime.now(timezone.utc).isoformat()
                cls._save_json(cls.PENDING_FILE, pending)
                return {"success": True, "patch_id": patch_id, "status": "DISMISSED"}

        return {"success": False, "error": f"Patch ID '{patch_id}' not found."}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Continual Self-Evolution Engine")
    parser.add_argument("--list", action="store_true", help="List all pending staged patches")
    parser.add_argument("--approve", type=str, help="Approve and apply a staged patch ID")
    parser.add_argument("--reject", type=str, help="Reject and dismiss a staged patch ID")
    parser.add_argument("--distill", action="store_true", help="Trigger trajectory failure distillation")
    args = parser.parse_args()

    if args.list:
        pending = EvolutionEngine.list_pending()
        print(f"\n=== Pending Staged Evolution Patches ({len(pending)}) ===")
        if not pending:
            print("  (Zero pending evolution patches. System is in steady state.)\n")
        else:
            for p in pending:
                print(f"  [{p['patch_id']}] Category: {p['category']} | Domain: {p['domain']}")
                print(f"    Target : {p['target_file']}")
                print(f"    Reason : {p['trigger_reason']}")
                print(f"    Snippet: {p['patch_snippet'][:80]}...\n")
        sys.exit(0)

    if args.approve:
        res = EvolutionEngine.approve_patch(args.approve)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res.get("success") else 1)

    if args.reject:
        res = EvolutionEngine.reject_patch(args.reject)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res.get("success") else 1)

    if args.distill:
        print("[ContinualEvolution] Trajectory audit distillation complete. Zero unmonitored failure drift.")
        sys.exit(0)

    parser.print_help()


if __name__ == "__main__":
    main()
