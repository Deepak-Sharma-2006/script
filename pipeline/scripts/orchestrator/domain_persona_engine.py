"""
Domain Persona Engine — Universal Dynamic SDLC Persona Hydration
Dynamically equips the 6 enterprise personas ([PM], [Architect], [SDET], [Engineer], [Auditor], [Writer])
with deep domain expertise, statutory constraints, specialized rubrics, and verification gates
based on the active Master Domain and selected subdomains.
"""

import os
import json
from typing import Dict, Any, List, Optional


class DomainPersonaEngine:
    """
    Manages just-in-time (JIT) dynamic hydration of the 6 enterprise personas
    with domain-specific rubrics, coding idioms, statutory gates, and threat models.
    """

    STATE_PATH = os.path.join(".agents", "state", "active-domain.json")
    TEMPLATES_DIR = os.path.join("pipeline", "templates", "domains") if os.path.exists(os.path.join("pipeline", "templates", "domains")) else os.path.join("templates", "domains")

    @classmethod
    def get_active_state(cls) -> Dict[str, Any]:
        """Reads active domain state or returns default software profile."""
        if os.path.exists(cls.STATE_PATH):
            try:
                with open(cls.STATE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        # Fallback default
        return {
            "domain_id": "software",
            "domain_name": "Software Engineering & Application Development",
            "subdomains": ["web_frontend", "backend_systems"],
            "configured_at": "2026-09-30T00:00:00.000Z",
            "configured_by": "SystemDefault",
            "active_stack": {
                "languages_and_tools": ["TypeScript", "Python", "React", "Node.js"],
                "statutory_standards": ["OpenAPI 3.1", "12-Factor App"],
                "verification_gates": ["unit_tdd", "mutation_testing", "zero_secrets"]
            }
        }

    @classmethod
    def load_domain_rubric(cls, domain_id: Optional[str] = None) -> Dict[str, Any]:
        """Loads the full domain rubric JSON from templates/domains/<domain_id>/rubric.json."""
        if not domain_id:
            state = cls.get_active_state()
            domain_id = state.get("domain_id", "software")

        rubric_file = os.path.join(cls.TEMPLATES_DIR, domain_id, "rubric.json")
        if not os.path.exists(rubric_file):
            # Fallback to software rubric
            rubric_file = os.path.join(cls.TEMPLATES_DIR, "software", "rubric.json")
            if not os.path.exists(rubric_file):
                raise FileNotFoundError(f"Neither {domain_id} nor default software rubric found.")

        with open(rubric_file, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def hydrate_persona(cls, persona_key: str, domain_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns specialized domain instructions, role title, and rubrics
        for a specific persona key (product_manager, system_architect, adversarial_sdet,
        core_engineer, mutation_auditor, technical_writer).
        """
        state = cls.get_active_state()
        rubric = cls.load_domain_rubric(domain_id or state.get("domain_id"))
        specializations = rubric.get("persona_specializations", {})

        persona_data = specializations.get(persona_key, {})
        subdomains = state.get("subdomains", [])

        # Extract subdomain details
        subdomain_details = []
        d_id = domain_id or state.get("domain_id", "software")
        for s in subdomains:
            pack_path = os.path.join(cls.TEMPLATES_DIR, d_id, f"{s}.json")
            if os.path.exists(pack_path):
                try:
                    with open(pack_path, "r", encoding="utf-8") as pf:
                        pdata = json.load(pf)
                    subdomain_details.append({
                        "subdomain_id": s,
                        "name": pdata.get("name", s),
                        "description": pdata.get("description", ""),
                        "technologies": pdata.get("key_technologies", []),
                        "standards": pdata.get("statutory_standards", []),
                        "physical_compute_boundaries": pdata.get("physical_compute_boundaries", {}),
                        "forbidden_antipatterns": pdata.get("forbidden_antipatterns", [])
                    })
                    continue
                except Exception:
                    pass
            meta = rubric.get("subdomains", {}).get(s, {})
            if meta:
                subdomain_details.append({
                    "subdomain_id": s,
                    "name": meta.get("name", s),
                    "description": meta.get("description", ""),
                    "technologies": meta.get("key_technologies", []),
                    "standards": meta.get("statutory_standards", [])
                })

        return {
            "domain_id": rubric.get("domain_id"),
            "domain_name": rubric.get("domain_name"),
            "active_subdomains": subdomain_details,
            "role_title": persona_data.get("role_title", f"Senior {persona_key.replace('_', ' ').title()}"),
            "specialization": persona_data,
            "verification_gates": rubric.get("verification_gates", []),
            "composite_stack": state.get("active_stack", {})
        }

    @classmethod
    def get_active_skills(cls, domain_id: Optional[str] = None, subdomains: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        Resolves verified skills from .agents/skills/ for the active domain and subdomains.
        Enforces Contrarian hardening invariant: Every returned skill must physically exist on disk.
        """
        state = cls.get_active_state()
        d_id = domain_id or state.get("domain_id", "software")
        subs = subdomains or state.get("subdomains", [])

        rubric = cls.load_domain_rubric(d_id)
        resolved_skills: Dict[str, Dict[str, str]] = {}
        workspace_root = os.getcwd().replace("\\", "/")

        for s in subs:
            meta = rubric.get("subdomains", {}).get(s, {})
            curated = meta.get("curated_skills", [])
            for skill_id in curated:
                if skill_id not in resolved_skills:
                    skill_md_rel = os.path.join(".agents", "skills", skill_id, "SKILL.md")
                    if os.path.exists(skill_md_rel):
                        resolved_skills[skill_id] = {
                            "id": skill_id,
                            "path": skill_md_rel.replace("\\", "/"),
                            "markdown_link": f"[{skill_id}](file:///{workspace_root}/.agents/skills/{skill_id}/SKILL.md)"
                        }

        # Fallback to skill-scout if zero skills mapped
        if not resolved_skills and os.path.exists(os.path.join(".agents", "skills", "skill-scout", "SKILL.md")):
            resolved_skills["skill-scout"] = {
                "id": "skill-scout",
                "path": ".agents/skills/skill-scout/SKILL.md",
                "markdown_link": f"[skill-scout](file:///{workspace_root}/.agents/skills/skill-scout/SKILL.md)"
            }

        return list(resolved_skills.values())

    @classmethod
    def generate_persona_system_prompt_overlay(cls, persona_key: str, domain_id: Optional[str] = None) -> str:
        """
        Generates a concise, highly-dense domain prompt overlay (<500 tokens)
        to be prepended or injected into the persona reasoning loop.
        """
        hydrated = cls.hydrate_persona(persona_key, domain_id=domain_id)
        domain_name = hydrated["domain_name"]
        role_title = hydrated["role_title"]
        spec = hydrated["specialization"]
        subdomains_str = ", ".join([s["name"] for s in hydrated["active_subdomains"]])
        standards_str = " | ".join(hydrated["composite_stack"].get("statutory_standards", []))
        tools_str = ", ".join(hydrated["composite_stack"].get("languages_and_tools", [])[:8])

        active_skills = cls.get_active_skills(
            domain_id=domain_id,
            subdomains=[s["subdomain_id"] for s in hydrated["active_subdomains"]]
        )
        skill_links = [s["markdown_link"] for s in active_skills[:6]]
        skills_str = ", ".join(skill_links) if skill_links else "None"

        overlay = [
            f"=== [DOMAIN SPECIALIZATION: {domain_name.upper()}] ===",
            f"Active Persona Role  : {role_title}",
            f"Target Subdomains    : {subdomains_str}",
            f"Key Technology Stack : {tools_str}",
            f"Statutory Standards  : {standards_str}",
            f"Curated Skills       : {skills_str}",
            "--------------------------------------------------------------------------------"
        ]

        if persona_key == "product_manager":
            overlay.append(f"Domain Objectives   : {spec.get('domain_objectives', '')}")
            overlay.append(f"Requirements Rubric : {spec.get('requirements_rubric', '')}")
            overlay.append(f"Forbidden Pitfalls  : {', '.join(spec.get('forbidden_pitfalls', []))}")

        elif persona_key == "system_architect":
            overlay.append(f"Mandatory Patterns  : {', '.join(spec.get('mandatory_patterns', []))}")
            overlay.append(f"Perf Invariants     : {', '.join(spec.get('performance_invariants', []))}")

        elif persona_key == "adversarial_sdet":
            overlay.append(f"Threat Model        : {spec.get('threat_model', '')}")
            overlay.append(f"Chaos Vectors       : {', '.join(spec.get('chaos_vectors', []))}")
            overlay.append(f"Boundary Fuzzing    : {spec.get('boundary_fuzzing', '')}")

        elif persona_key == "core_engineer":
            overlay.append(f"Coding Idioms       : {spec.get('coding_idioms', '')}")
            overlay.append(f"Concurrency Rules   : {spec.get('concurrency_rules', '')}")
            overlay.append(f"Resource Rules      : {spec.get('memory_and_resource_rules', '')}")

        elif persona_key == "mutation_auditor":
            overlay.append(f"Security Standards  : {', '.join(spec.get('security_standards', []))}")
            overlay.append(f"Compliance Gates    : {', '.join(spec.get('statutory_compliance_gates', []))}")
            overlay.append(f"Audit Checklist     : {', '.join(spec.get('audit_checklist', []))}")

        elif persona_key == "technical_writer":
            overlay.append(f"Documentation Lexicon: {spec.get('documentation_lexicon', '')}")
            overlay.append(f"Diagram Style       : {spec.get('architectural_diagram_style', '')}")
            overlay.append(f"Recommended Theme   : {spec.get('presentation_theme', 'modern_tech')}")

        overlay.append("================================================================================")
        return "\n".join(overlay)

    @classmethod
    def get_presentation_theme(cls, domain_id: Optional[str] = None) -> str:
        """Returns the recommended presentation theme for OmniDeck based on active domain."""
        hydrated = cls.hydrate_persona("technical_writer", domain_id=domain_id)
        return hydrated["specialization"].get("presentation_theme", "modern_tech")

    @classmethod
    def hydrate_all_personas(cls, domain_id: Optional[str] = None) -> Dict[str, Any]:
        """Returns hydrated configurations for all personas for the active domain."""
        roles = [
            "deep_research_specialist",
            "product_manager",
            "system_architect",
            "adversarial_sdet",
            "core_engineer",
            "mutation_auditor",
            "technical_writer"
        ]
        return {r: cls.hydrate_persona(r, domain_id=domain_id) for r in roles}


def main():
    import sys
    from datetime import datetime, timezone

    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if len(sys.argv) < 2 or "--status" in sys.argv:
        state = DomainPersonaEngine.get_active_state()
        print(json.dumps(state, indent=2))
        return

    arg = sys.argv[1]
    if arg == "--hydrate" and len(sys.argv) > 2:
        persona = sys.argv[2]
        overlay = DomainPersonaEngine.generate_persona_system_prompt_overlay(persona)
        print(overlay)
    elif arg == "--write-overlay":
        overlay = DomainPersonaEngine.generate_persona_system_prompt_overlay("core_engineer")
        out_path = os.path.join(".agents", "state", "active-domain-context.md")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(overlay)
        print(f"✅ Hydrated active domain context written to {out_path}")
    elif arg == "--set-domain" and len(sys.argv) > 2:
        dom = sys.argv[2]
        subs = sys.argv[3].split(",") if len(sys.argv) > 3 else []
        state_path = os.path.join(".agents", "state", "active-domain.json")
        os.makedirs(os.path.dirname(state_path), exist_ok=True)
        payload = {
            "domain_id": dom,
            "subdomains": subs,
            "configured_at": datetime.now(timezone.utc).isoformat(),
            "configured_by": "CLI"
        }
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"✅ Configured active domain: {dom} with subdomains: {subs}")
    else:
        print("Usage: python -m scripts.orchestrator.domain_persona_engine [--status | --hydrate <persona> | --write-overlay | --set-domain <id> <sub1,sub2>]")


if __name__ == "__main__":
    main()

