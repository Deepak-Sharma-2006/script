"""
Operational Deadline & Lockdown Engine (INV-07)
Tracks operational deadlines (hackathon end, release freeze, client demo).
Automatically transitions the workspace into Safe Submission Pipeline Mode
at T-minus 4 hours, blocking non-essential R&D rewrites and enforcing safe delivery.
"""

import sys
import os
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class DeadlineLockdown:
    """
    Manages operational deadline lockdown states and validates permitted actions.
    """

    STATE_FILE = os.path.join(".agents", "state", "deadline_lockdown.json")
    DEFAULT_LOCKDOWN_HOURS = 4.0

    PERMITTED_LOCKDOWN_ACTIONS = [
        "generate_submission",
        "verify_submission_format",
        "lint_submission",
        "calculate_checksum",
        "package_artifact",
        "verify_delivery",
        "test_smoke",
        "read_docs",
        "status",
    ]

    PROHIBITED_LOCKDOWN_ACTIONS = [
        "train_new_model",
        "retrain_pipeline",
        "architectural_rewrite",
        "refactor_core_schema",
        "experimental_feature_branch",
    ]

    @classmethod
    def _load_state(cls) -> Dict[str, Any]:
        if os.path.exists(cls.STATE_FILE):
            try:
                with open(cls.STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    @classmethod
    def _save_state(cls, state: Dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(cls.STATE_FILE), exist_ok=True)
        with open(cls.STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    @staticmethod
    def parse_time_string(s: str) -> float:
        """Parses time strings like '4h', '30m', '2d', '1w', '1.5h' into hours."""
        s = s.strip().lower()
        if s.endswith("m"):
            return float(s[:-1]) / 60.0
        elif s.endswith("h"):
            return float(s[:-1])
        elif s.endswith("d"):
            return float(s[:-1]) * 24.0
        elif s.endswith("w"):
            return float(s[:-1]) * 168.0
        elif s.endswith("s"):
            return float(s[:-1]) / 3600.0
        else:
            return float(s)

    @classmethod
    def set_duration(
        cls, duration_str: str, threshold_str: Optional[str] = None
    ) -> Dict[str, Any]:
        """Sets deadline from now plus a duration (e.g. '4h', '72h', '2w') with adaptive threshold."""
        try:
            duration_hours = cls.parse_time_string(duration_str)
        except Exception as e:
            return {"error": f"Invalid duration string '{duration_str}': {str(e)}"}

        if threshold_str:
            try:
                lockdown_hours = cls.parse_time_string(threshold_str)
            except Exception as e:
                return {"error": f"Invalid threshold string '{threshold_str}': {str(e)}"}
        else:
            # Adaptive threshold based on project scale:
            if duration_hours <= 2.0:
                lockdown_hours = 0.25  # 15 minutes for lightning 1-2h burst
            elif duration_hours <= 6.0:
                lockdown_hours = 0.5   # 30 minutes for 4-6h burst
            elif duration_hours <= 24.0:
                lockdown_hours = 2.0   # 2 hours for 12-24h day sprint
            elif duration_hours <= 96.0:
                lockdown_hours = 4.0   # 4 hours for 48-72h standard hackathon
            else:
                lockdown_hours = 24.0  # 24 hours for multi-week enterprise sprint

        now = datetime.now(timezone.utc)
        target_dt = now + timedelta(hours=duration_hours)
        return cls.set_deadline(target_dt.isoformat(), lockdown_hours=lockdown_hours)

    @classmethod
    def clear_deadline(cls) -> Dict[str, Any]:
        """Clears any active deadline and returns to unconfigured normal exploration."""
        if os.path.exists(cls.STATE_FILE):
            try:
                os.remove(cls.STATE_FILE)
            except Exception:
                pass
        return {
            "configured": False,
            "status": "NORMAL_EXPLORATION",
            "message": "Operational deadline cleared. Normal exploration mode active.",
        }

    @classmethod
    def set_deadline(
        cls, deadline_iso: str, lockdown_hours: float = DEFAULT_LOCKDOWN_HOURS
    ) -> Dict[str, Any]:
        """Sets target operational deadline in ISO format."""
        # Validate ISO string
        try:
            dt = datetime.fromisoformat(deadline_iso.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        except Exception as e:
            return {"error": f"Invalid ISO 8601 deadline string: {str(e)}"}

        state = {
            "deadline_iso": dt.isoformat(),
            "deadline_timestamp": dt.timestamp(),
            "lockdown_threshold_hours": lockdown_hours,
            "configured_at": datetime.now(timezone.utc).isoformat(),
        }
        cls._save_state(state)
        return cls.get_status()

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """Calculates current time remaining and lockdown status."""
        state = cls._load_state()
        if not state or "deadline_timestamp" not in state:
            return {
                "configured": False,
                "status": "NORMAL_EXPLORATION",
                "message": "No operational deadline configured.",
            }

        now_utc = datetime.now(timezone.utc)
        deadline_ts = state["deadline_timestamp"]
        now_ts = now_utc.timestamp()
        seconds_remaining = deadline_ts - now_ts
        hours_remaining = seconds_remaining / 3600.0
        lockdown_thresh = state.get("lockdown_threshold_hours", cls.DEFAULT_LOCKDOWN_HOURS)

        if seconds_remaining <= 0:
            status = "DEADLINE_EXPIRED"
            message = "Deadline has passed. No further submissions permitted."
        elif hours_remaining <= lockdown_thresh:
            status = "SAFE_SUBMISSION_LOCKDOWN"
            message = (
                f"T-minus {hours_remaining:.2f} hours remaining (<= {lockdown_thresh}h threshold). "
                "Safe Submission Lockdown ACTIVE: R&D rewrites blocked. Only artifact formatting, "
                "smoke testing, and submission packaging permitted."
            )
        else:
            status = "NORMAL_EXPLORATION"
            message = f"T-minus {hours_remaining:.2f} hours remaining. Normal exploration permitted."

        return {
            "configured": True,
            "status": status,
            "hours_remaining": round(hours_remaining, 2),
            "seconds_remaining": round(seconds_remaining, 1),
            "deadline_iso": state.get("deadline_iso"),
            "lockdown_threshold_hours": lockdown_thresh,
            "message": message,
        }

    @classmethod
    def validate_action(cls, action_name: str) -> Dict[str, Any]:
        """
        Validates if an action is permitted under current deadline status.
        """
        status_info = cls.get_status()
        status = status_info.get("status")

        if status == "NORMAL_EXPLORATION" or not status_info.get("configured"):
            return {
                "permitted": True,
                "action": action_name,
                "status": status,
                "reason": "Normal exploration permitted.",
            }

        if status == "DEADLINE_EXPIRED":
            return {
                "permitted": False,
                "action": action_name,
                "status": status,
                "reason": "DEADLINE EXPIRED: All pipeline actions blocked.",
            }

        # Safe Submission Lockdown mode
        action_clean = action_name.lower().strip()
        is_prohibited = any(p in action_clean for p in cls.PROHIBITED_LOCKDOWN_ACTIONS)
        is_permitted = any(p in action_clean for p in cls.PERMITTED_LOCKDOWN_ACTIONS)

        if is_prohibited or (not is_permitted and "submit" not in action_clean and "pack" not in action_clean):
            return {
                "permitted": False,
                "action": action_name,
                "status": status,
                "reason": (
                    f"ACTION BLOCKED BY T-4H LOCKDOWN: '{action_name}' is forbidden during safe submission freeze. "
                    "Only submission package generation, format linting, and delivery verification are permitted."
                ),
            }

        return {
            "permitted": True,
            "action": action_name,
            "status": status,
            "reason": "Action permitted under safe submission protocol.",
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.orchestrator.deadline_lockdown [--status|--duration <4h|72h> [--threshold <30m|4h>]|--set <ISO> [threshold_h]|--clear|--check <ACTION>]")
        sys.exit(0)

    arg = sys.argv[1]
    if arg == "--status":
        res = DeadlineLockdown.get_status()
        print(json.dumps(res, indent=2))
        sys.exit(0)
    elif arg == "--clear" or arg == "--reset":
        res = DeadlineLockdown.clear_deadline()
        print(json.dumps(res, indent=2))
        sys.exit(0)
    elif arg == "--duration" and len(sys.argv) > 2:
        dur = sys.argv[2]
        thresh = None
        if "--threshold" in sys.argv:
            idx = sys.argv.index("--threshold")
            if idx + 1 < len(sys.argv):
                thresh = sys.argv[idx + 1]
        res = DeadlineLockdown.set_duration(dur, thresh)
        print(json.dumps(res, indent=2))
        sys.exit(0)
    elif arg == "--set" and len(sys.argv) > 2:
        iso_str = sys.argv[2]
        thresh = DeadlineLockdown.DEFAULT_LOCKDOWN_HOURS
        if len(sys.argv) > 3 and not sys.argv[3].startswith("-"):
            try:
                thresh = float(sys.argv[3])
            except ValueError:
                pass
        res = DeadlineLockdown.set_deadline(iso_str, lockdown_hours=thresh)
        print(json.dumps(res, indent=2))
        sys.exit(0)
    elif arg == "--check" and len(sys.argv) > 2:
        res = DeadlineLockdown.validate_action(sys.argv[2])
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["permitted"] else 1)
    else:
        print("Unknown arguments. Run without arguments for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
