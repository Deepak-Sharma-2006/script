"""
Domain Prompt Hygiene & System Prompt Compression Engine (INV-10)
Compresses monolithic 25 KB system prompt instructions into a focused 4 KB
Core Universal Kernel, and dynamically prunes domain-irrelevant rules
to eliminate attention dilution and preserve token budget.
"""

import sys
import os
import json
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class PromptHygieneEngine:
    """
    Manages prompt hygiene by generating a compact Core Universal Kernel
    and injecting only the active domain's specialized persona overlays.
    """

    ACTIVE_DOMAIN_FILE = os.path.join(".agents", "state", "active-domain.json")
    TEMPLATES_DIR = os.path.join("pipeline", "templates", "domains") if os.path.exists(os.path.join("pipeline", "templates", "domains")) else os.path.join("templates", "domains")

    CORE_UNIVERSAL_KERNEL = """
# Enterprise Autonomous Agentic Core Kernel (v2.0)

1. Zero Ghost Packages & AST Grounding: Only import packages declared in package.json or standard library. Never hallucinate packages or APIs.
2. Direct High-Signal Engineering: Execute with zero theatrical persona monologues (Rule 15). Persona specialization is decoupled into dedicated headless CLI worker lanes (Lead 1 Alpha, Lead 2 Beta, Mutation Auditor, OmniDeck) and modular tasks via TaskDispatcher.
3. Empirical Grounding & Attestation Receipt: Never assert tests pass, builds succeed, or metrics hold without executing real commands. Conclude with verifiable squad_execution_attestation receipt.
4. Red-First Testing & Mutation Gate: Author adversarial tests first (must fail red before implementation). Verify >= 80% mutation kill rate.
5. Zero Secrets Policy: Absolute zero credentials, tokens, or private keys committed or output. Use safe placeholders only.
6. Zero-LaTeX Formatting Invariant: Strictly prohibit raw LaTeX ($ or $$). Use clean Unicode (>=, <=, x, !=, ->, ~, +-, theta, p^) or fenced code blocks.
7. Memory Vault & SpecSync: Mirror all brain plans/walkthroughs to docs/ and record architectural decisions to SQLite Memory Vault.
""".strip()

    DOMAIN_SPECIFIC_OVERLAYS = {
        "software": """
## Domain Overlay: Software Engineering & Application Development
- Enforce strict TypeScript (strict: true, zero 'any') and RFC 7807 Problem Details error handling.
- Mandatory universal frontend layout: app-header, app-viewport, and bottom-right app-action-dock.
- Headless Playwright: Verify tab transitions, geometry, zero console errors, and reactive store bindings.
""".strip(),
        "ai_ml": """
## Domain Overlay: AI, Machine Learning & Cognitive Systems
- Asymptotic Scale Profiler: Run mandatory micro-benchmarks before executing unindexed O(N²) operations >10k items.
- Memory Guard: Enforce 75% physical RAM allocation ceiling to prevent kernel OOM (SIGKILL).
- Distractor Parity & Upstream Recall Gate: R_upstream >= Target + 0.05. Test set must reflect true negative distractor density.
- Probability Calibration: Evaluate Brier score and reliability curves before threshold tuning.
""".strip(),
        "blockchain": """
## Domain Overlay: Blockchain & Smart Contracts
- Enforce Checks-Effects-Interactions (CEI) pattern and ReentrancyGuard on state-changing calls.
- Ban spot price calculations without Time-Weighted Average Price (TWAP) or Chainlink oracles.
- Enforce SafeERC20, integer overflow guards, and deterministic gas bounds.
""".strip(),
        "deep_tech": """
## Domain Overlay: Scientific Research, Deep Tech & Frontier Computing
- Floating-Point Precision: Ban raw float equality (a == b); enforce epsilon bounds or symplectic integrators.
- Physical Invariants: Enforce conservation of energy/momentum, dimensional analysis, and convergence tolerance.
- Zero-Raw-LaTeX Invariant: Use universally rendering Unicode math typography across all documentation.
""".strip(),
        "cybersecurity": """
## Domain Overlay: Cybersecurity, AppSec & Cryptographic Defense
- Timing Attacks: Enforce constant-time comparison (crypto.timingSafeEqual / hmac.compare_digest).
- SQL & Command Injection: Mandatory parameterized queries and safe command array execution.
- Zero-Trust: Enforce mTLS, Least Privilege RBAC, and memory-safe deserialization.
""".strip(),
        "cloud_infra": """
## Domain Overlay: Cloud, Distributed Systems & Infrastructure Operations
- Idempotency & Retries: Enforce distributed idempotency keys and exponential backoff with jitter.
- FinOps Egress Guard: Mandate cross-region bandwidth cost modeling before large-scale replication.
- Resilience: Enforce phased canary rollouts, Prometheus error budget checks, and automated rollback.
""".strip(),
        "data_engineering": """
## Domain Overlay: Data Engineering, Big Data & Knowledge Intelligence
- Stream Ingestion: Enforce Data Contract schema validation, non-null assertions, and dead-letter queues.
- State Retention: Centralized reactive state store mandatory; tab transitions must never clear computed state.
- Exactly-Once Semantics: Watermark backpressure and transactional outbox patterns.
""".strip(),
        "vertical_applied": """
## Domain Overlay: Vertical Applied IT & Industry Solutions
- Statutory Action Gating: Downstream export and certificate actions remain fail-closed until engine reaches COMPLETED.
- Statutory Compliance: Enforce HIPAA/DISHA Row-Level Security on PHI, PCI-DSS tokenization, and ISO 20022 messaging.
""".strip(),
        "systems": """
## Domain Overlay: Systems, Infrastructure & Backend
- Zero-copy IO, memory-mapped buffers, and idempotent CLI DAG pipelines.
- Distributed lease locks and constant-time cryptographic primitives.
- Fail-closed error handling with circuit breakers and graceful shutdown.
""".strip(),
    }

    @classmethod
    def get_active_domain_context(cls) -> Dict[str, Any]:
        """Reads active domain, subdomains, and active stack from .agents/state/active-domain.json."""
        if os.path.exists(cls.ACTIVE_DOMAIN_FILE):
            try:
                with open(cls.ACTIVE_DOMAIN_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    domain_id = data.get("domain_id", data.get("activeDomain", data.get("domain", "ai_ml")))
                    subdomains = data.get("subdomains", [])
                    return {
                        "domain_id": domain_id,
                        "domain_name": data.get("domain_name", domain_id),
                        "subdomains": subdomains,
                        "active_stack": data.get("active_stack", {})
                    }
            except Exception:
                pass
        return {
            "domain_id": "ai_ml",
            "domain_name": "Artificial Intelligence, Machine Learning & Cognitive Systems",
            "subdomains": ["classical_ml", "deep_learning"],
            "active_stack": {}
        }

    @classmethod
    def get_active_domain(cls) -> str:
        """Reads active domain ID from state."""
        return cls.get_active_domain_context()["domain_id"]

    @classmethod
    def assemble_compact_prompt(cls, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Assembles a compressed prompt including the 4 KB Core Kernel
        plus the single active domain and subdomain overlay, pruning everything else.
        """
        context = cls.get_active_domain_context()
        active_dom = domain or context["domain_id"]

        # Map to valid domain overlay key
        category = active_dom
        if category not in cls.DOMAIN_SPECIFIC_OVERLAYS:
            if category in ("web3", "defi"):
                category = "blockchain"
            elif category in ("machine_learning", "datascience"):
                category = "ai_ml"
            elif category in ("frontend", "ui", "web_app"):
                category = "software"
            else:
                category = "systems"

        base_overlay = cls.DOMAIN_SPECIFIC_OVERLAYS.get(category, cls.DOMAIN_SPECIFIC_OVERLAYS["systems"])

        # Inject active subdomains if available
        subdomain_lines = []
        subs = context.get("subdomains", [])
        if subs:
            sub_names = ", ".join(subs[:4])
            subdomain_lines.append(f"Active Subdomains: {sub_names}")

        stack = context.get("active_stack", {})
        standards = stack.get("statutory_standards", [])
        if standards:
            subdomain_lines.append(f"Statutory Standards: {' | '.join(standards[:3])}")

        tools = stack.get("languages_and_tools", [])
        if tools:
            subdomain_lines.append(f"Specialized Stack: {', '.join(tools[:6])}")

        if subdomain_lines:
            subdomain_block = "\n" + "\n".join(f"- {line}" for line in subdomain_lines)
            active_overlay = f"{base_overlay}{subdomain_block}"
        else:
            active_overlay = base_overlay

        full_compact = f"{cls.CORE_UNIVERSAL_KERNEL}\n\n{active_overlay}".strip()

        byte_size = len(full_compact.encode("utf-8"))
        char_count = len(full_compact)

        return {
            "active_domain": active_dom,
            "category": category,
            "prompt_text": full_compact,
            "byte_size": byte_size,
            "char_count": char_count,
            "compression_ratio_vs_25kb": round(25000 / max(char_count, 1), 2),
            "status": "COMPACT_KERNEL_READY",
        }


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--active-domain":
        print(PromptHygieneEngine.get_active_domain())
        sys.exit(0)

    res = PromptHygieneEngine.assemble_compact_prompt()
    if len(sys.argv) > 1 and sys.argv[1] == "--text":
        print(res["prompt_text"])
    else:
        info = {k: v for k, v in res.items() if k != "prompt_text"}
        print(json.dumps(info, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()

