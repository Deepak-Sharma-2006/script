"""
Automatic Skill Resolution & Injection Engine
Solves the operator visibility blindspot and passive skill retrieval defect:
1. Automatically detects active domain & subdomains from .agents/state/active-domain.json
2. Retrieves verified curated skills mapped to those subdomains
3. Scans prompt keywords across all 300 in-tree skills in .agents/skills/
4. Surfaces exactly which skills are activated, ensuring zero ghost skills and 100% receipt transparency
"""

import sys
import os
import re
import json
from typing import Dict, Any, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class SkillResolver:
    """
    Programmatic resolver for dynamic skill discovery, binding, and attestation.
    """

    SKILLS_DIR = os.path.join(".agents", "skills")
    STATE_FILE = os.path.join(".agents", "state", "active-domain.json")
    TEMPLATES_DIR = os.path.join("templates", "domains")

    CORE_GOVERNANCE_SKILLS = [
        "agentic-engineering",
        "claude-council",
        "token-budget-guard",
        "skill-finder",
    ]

    @classmethod
    def get_active_domain_context(cls) -> Tuple[str, List[str]]:
        """Reads active domain and subdomains from state."""
        domain_id = "software"
        subdomains: List[str] = []

        if os.path.exists(cls.STATE_FILE):
            try:
                with open(cls.STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    domain_id = data.get("domain_id", data.get("domain", "software"))
                    subdomains = data.get("subdomains", [])
            except Exception:
                pass

        return domain_id, subdomains

    @classmethod
    def _get_subdomain_curated_skills(cls, domain_id: str, subdomains: List[str]) -> List[Dict[str, str]]:
        """Retrieves curated skills from rubric.json for active subdomains."""
        rubric_path = os.path.join(cls.TEMPLATES_DIR, domain_id, "rubric.json")
        curated: List[Dict[str, str]] = []

        if not os.path.exists(rubric_path):
            return curated

        try:
            with open(rubric_path, "r", encoding="utf-8") as f:
                rubric = json.load(f)

            subs_data = rubric.get("subdomains", {})
            for sub_name in subdomains:
                if sub_name in subs_data:
                    skills = subs_data[sub_name].get("curated_skills", [])
                    for s in skills:
                        skill_path = os.path.join(cls.SKILLS_DIR, s, "SKILL.md")
                        if os.path.exists(skill_path):
                            curated.append({
                                "name": s,
                                "path": skill_path.replace("\\", "/"),
                                "match_reason": f"subdomain:{sub_name}",
                            })
        except Exception:
            pass

        return curated

    @classmethod
    def _scan_prompt_keyword_skills(cls, prompt: str, max_matches: int = 3) -> List[Dict[str, str]]:
        """Matches prompt keywords against installed skills in .agents/skills/."""
        if not os.path.exists(cls.SKILLS_DIR):
            return []

        prompt_lower = prompt.lower()
        # Extract alphanumeric words > 3 chars
        tokens = set(re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", prompt_lower))

        matched = []
        try:
            installed = [
                d for d in os.listdir(cls.SKILLS_DIR)
                if os.path.isdir(os.path.join(cls.SKILLS_DIR, d)) and not d.startswith(".")
            ]
        except Exception:
            return []

        for skill_name in installed:
            skill_path = os.path.join(cls.SKILLS_DIR, skill_name, "SKILL.md")
            if not os.path.exists(skill_path):
                continue

            score = 0
            # Direct skill name match
            if skill_name in prompt_lower:
                score += 10
            else:
                # Skill parts match
                parts = skill_name.split("-")
                for p in parts:
                    if len(p) >= 3 and p in tokens:
                        score += 3

            if score > 0:
                matched.append((score, skill_name, skill_path))

        matched.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "name": item[1],
                "path": item[2].replace("\\", "/"),
                "match_reason": "prompt_keyword_affinity",
            }
            for item in matched[:max_matches]
        ]

    @classmethod
    def resolve_skills(
        cls,
        prompt: str,
        domain_id: Optional[str] = None,
        subdomains: Optional[List[str]] = None,
        max_total: int = 5,
    ) -> Dict[str, Any]:
        """
        Main entry point: resolves active domain curated skills + prompt keyword skills,
        guaranteeing zero ghost skills and providing full attestation metadata.
        """
        active_domain, active_subs = cls.get_active_domain_context()
        dom = domain_id or active_domain
        subs = subdomains if subdomains is not None else active_subs

        # 1. Curated subdomain skills
        curated = cls._get_subdomain_curated_skills(dom, subs)

        # 2. Keyword matched skills
        keyword_skills = cls._scan_prompt_keyword_skills(prompt)

        # 3. Combine with deduplication
        seen = set()
        resolved: List[Dict[str, str]] = []

        # Prioritize keyword skills that directly match operator intent
        for s in keyword_skills:
            if s["name"] not in seen:
                seen.add(s["name"])
                resolved.append(s)

        # Add subdomain curated skills
        for s in curated:
            if s["name"] not in seen and len(resolved) < max_total:
                seen.add(s["name"])
                resolved.append(s)

        # Ensure at least 1 core governance skill if resolved is empty
        if not resolved:
            for g in cls.CORE_GOVERNANCE_SKILLS:
                gp = os.path.join(cls.SKILLS_DIR, g, "SKILL.md")
                if os.path.exists(gp) and g not in seen:
                    seen.add(g)
                    resolved.append({
                        "name": g,
                        "path": gp.replace("\\", "/"),
                        "match_reason": "core_governance_fallback",
                    })
                    break

        return {
            "domain": dom,
            "subdomains": subs,
            "resolved_count": len(resolved),
            "activated_skills": resolved[:max_total],
        }


def main():
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Build a rate limited API service with postgres"
    result = SkillResolver.resolve_skills(prompt)
    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
