"""
Updates templates/domains/*/rubric.json with verified curated_skills mapped to .agents/skills/
Across all 8 Master Domains and all 46 Subdomains.
"""
import os
import json

SKILLS_DIR = os.path.join(".agents", "skills")

MAPPINGS = {
    "software": {
        "web_frontend": ["frontend-patterns", "motion-ui", "frontend-a11y", "design-system", "make-interfaces-feel-better", "vite-patterns", "liquid-glass-design", "browser-qa"],
        "backend_systems": ["backend-patterns", "postgres-patterns", "mysql-patterns", "clickhouse-io", "redis-patterns", "fastapi-patterns", "django-patterns", "nestjs-patterns"],
        "mobile_apps": ["react-native-patterns", "dart-flutter-patterns", "swiftui-patterns", "android-clean-architecture", "ios-icon-gen"],
        "desktop_native": ["windows-desktop-e2e", "bun-runtime", "dotnet-patterns", "cpp-coding-standards"],
        "game_engineering": ["blender-motion-state-inspection", "cpp-testing", "latency-critical-systems"],
        "embedded_rtos": ["cisco-ios-patterns", "netmiko-ssh-automation", "cpp-coding-standards"],
        "enterprise_bpm": ["tinystruct-patterns", "contract-first", "jira-integration"]
    },
    "ai_ml": {
        "classical_ml": ["benchmark", "python-patterns", "python-testing"],
        "deep_learning": ["pytorch-patterns", "mle-workflow", "benchmark-optimization-loop"],
        "generative_foundation": ["prompt-optimizer", "fal-ai-media", "foundation-models-on-device"],
        "agentic_ai": ["agentic-engineering", "eval-harness", "continuous-agent-loop", "team-agent-orchestration", "claude-council", "cost-tracking", "openclaw-persona-forge"],
        "nlp_rag": ["iterative-retrieval", "regex-vs-llm-structured-text", "deep-research", "exa-search"],
        "computer_vision": ["blender-motion-state-inspection", "fal-ai-media", "videodb"],
        "rl_alignment": ["benchmark-optimization-loop", "autonomous-loops", "eval-harness"],
        "mlops_inference": ["mle-workflow", "latency-critical-systems", "data-throughput-accelerator", "ito-inference", "ito-compute"],
        "physical_ai": ["blender-motion-state-inspection", "cpp-coding-standards", "latency-critical-systems"]
    },
    "blockchain": {
        "smart_contracts": ["defi-amm-security", "evm-token-decimals", "contract-first", "nodejs-keccak256"],
        "defi_protocols": ["defi-amm-security", "evm-token-decimals", "contract-first", "finance-billing-ops", "agent-payment-x402"],
        "zero_knowledge": ["rust-patterns", "cpp-coding-standards", "security-review"],
        "layer2_scaling": ["latency-critical-systems", "data-throughput-accelerator", "contract-first"],
        "depin_identity": ["contract-first", "agent-payment-x402", "security-review"]
    },
    "deep_tech": {
        "quantum_computing": ["latency-critical-systems", "benchmark", "cpp-coding-standards"],
        "computational_biology": ["deep-research", "research-ops", "scientific-pkg-gget", "scientific-db-pubmed-database"],
        "computational_materials": ["scientific-db-uspto-database", "research-ops", "benchmark"],
        "hpc_supercomputing": ["latency-critical-systems", "benchmark", "data-throughput-accelerator", "cpp-testing"],
        "aerospace_avionics": ["safety-guard", "verification-loop", "delivery-gate"]
    },
    "cybersecurity": {
        "appsec_devsecops": ["security-review", "styx-pentest", "safety-guard", "gateguard", "security-scan"],
        "zero_trust_network": ["homelab-network-readiness", "homelab-wireguard-vpn", "security-review"],
        "cryptography_pqc": ["nodejs-keccak256", "security-review", "contract-first"],
        "red_team_offensive": ["styx-pentest", "security-bounty-hunter", "safety-guard"],
        "soc_dfir": ["logistics-exception-management", "unified-notifications-ops", "messages-ops"]
    },
    "cloud_infra": {
        "kubernetes_cloud_native": ["kubernetes-patterns", "docker-patterns", "deployment-patterns"],
        "sre_observability": ["dashboard-builder", "verification-loop", "canary-watch", "production-audit"],
        "platform_iac": ["docker-patterns", "flox-environments", "uncloud"],
        "edge_computing": ["latency-critical-systems", "fastapi-patterns", "nextjs-turbopack"],
        "green_computing": ["cost-tracking", "ecc-tools-cost-audit", "connections-optimizer"]
    },
    "data_engineering": {
        "stream_processing": ["data-throughput-accelerator", "latency-critical-systems", "clickhouse-io"],
        "lakehouse_warehousing": ["postgres-patterns", "clickhouse-io", "contract-first"],
        "data_orchestration": ["django-celery", "contract-first", "team-agent-orchestration"],
        "specialized_databases": ["clickhouse-io", "postgres-patterns", "mysql-patterns", "redis-patterns"],
        "data_mesh_governance": ["contract-first", "living-docs-governance", "database-migrations"]
    },
    "vertical_applied": {
        "fintech_banking": ["finance-billing-ops", "customer-billing-ops", "contract-first", "agent-payment-x402"],
        "healthtech_informatics": ["hipaa-compliance", "healthcare-cdss-patterns", "healthcare-phi-compliance", "healthcare-eval-harness", "healthcare-emr-patterns"],
        "govtech_sovereign": ["accessibility", "frontend-a11y", "safety-guard", "delivery-gate"],
        "legaltech_regulatory": ["customs-trade-compliance", "living-docs-governance", "pdf-document-intelligence", "contract-first"],
        "industrial_iot": ["cisco-ios-patterns", "netmiko-ssh-automation", "cpp-coding-standards"]
    }
}

def verify_and_apply():
    missing_skills = []
    total_skills_mapped = 0
    subdomains_updated = 0

    for domain_id, subdomains in MAPPINGS.items():
        rubric_path = os.path.join("templates", "domains", domain_id, "rubric.json")
        if not os.path.exists(rubric_path):
            print(f"Error: Rubric path {rubric_path} does not exist!")
            continue

        with open(rubric_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for sub_id, skill_list in subdomains.items():
            valid_skills = []
            for skill in skill_list:
                skill_file = os.path.join(SKILLS_DIR, skill, "SKILL.md")
                if os.path.exists(skill_file):
                    valid_skills.append(skill)
                    total_skills_mapped += 1
                else:
                    missing_skills.append((domain_id, sub_id, skill))

            if sub_id in data.get("subdomains", {}):
                data["subdomains"][sub_id]["curated_skills"] = valid_skills
                subdomains_updated += 1
            else:
                print(f"Warning: Subdomain '{sub_id}' not found in {domain_id} rubric!")

        with open(rubric_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")

        print(f"Updated {domain_id}/rubric.json with verified curated skills.")

    print("\n-------------------------------------------------------------")
    print(f"Subdomains Updated: {subdomains_updated} / 46")
    print(f"Total Skill References Mapped & Verified: {total_skills_mapped}")
    if missing_skills:
        print(f"CRITICAL: Found {len(missing_skills)} missing skills:")
        for m in missing_skills:
            print(f"  - {m[0]} -> {m[1]} -> {m[2]}")
    else:
        print("SUCCESS: 100% of mapped skills exist on disk with SKILL.md!")

if __name__ == "__main__":
    verify_and_apply()
