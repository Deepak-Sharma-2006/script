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

    CORE_UNIVERSAL_KERNEL = """
# Enterprise Autonomous Agentic Core Kernel (v2.0)

1. Zero Ghost Packages & AST Grounding: Only import packages declared in package.json or standard library. Never hallucinate packages or APIs.
2. 6-Persona Execution Lifecycle: Every response must visibly execute through [Product Manager], [System Architect], [Adversarial SDET], [Core Engineer], [Mutation & Security Auditor], and [Technical Writer].
3. Empirical Grounding & Attestation Receipt: Never assert tests pass, builds succeed, or metrics hold without executing real commands. Conclude with verifiable squad_execution_attestation receipt.
4. Red-First Testing & Mutation Gate: Author adversarial tests first (must fail red before implementation). Verify >= 80% mutation kill rate.
5. Zero Secrets Policy: Absolute zero credentials, tokens, or private keys committed or output. Use safe placeholders only.
6. Zero-LaTeX Formatting Invariant: Strictly prohibit raw LaTeX ($ or $$). Use clean Unicode (>=, <=, x, !=, ->, ~, +-, theta, p^) or fenced code blocks.
7. Memory Vault & SpecSync: Mirror all brain plans/walkthroughs to docs/ and record architectural decisions to SQLite Memory Vault.
""".strip()

    DOMAIN_SPECIFIC_OVERLAYS = {
        "blockchain": """
## Domain Overlay: Blockchain & Smart Contracts
- Enforce Checks-Effects-Interactions (CEI) pattern and ReentrancyGuard on state-changing calls.
- Ban spot price calculations without Time-Weighted Average Price (TWAP) or Chainlink oracles.
- Enforce SafeERC20 and integer overflow guards.
""".strip(),
        "ai_ml": """
## Domain Overlay: AI, Machine Learning & Data Engineering
- Asymptotic Scale Profiler: Run mandatory 500-item micro-benchmarks before executing >10k items.
- Memory Guard: Enforce 75% physical RAM allocation ceiling to prevent kernel OOM (SIGKILL).
- Distractor Parity & Upstream Recall Gate: R_upstream >= Target + 0.05. Test set must reflect true negative distractor density.
- Probability Calibration: Evaluate Brier score and reliability curves before threshold tuning.
""".strip(),
        "frontend": """
## Domain Overlay: Frontend & UI Engineering
- Enforce Standard Component Shell: Header, Viewport, and Action Dock at bottom-right.
- Design Tokens: Import design-tokens.css. Zero ad-hoc inline styles or raw hex values.
- Headless Playwright: Verify tab transitions, state store persistence, and bounding boxes.
""".strip(),
        "systems": """
## Domain Overlay: Systems, Infrastructure & Backend
- Zero-copy IO, memory-mapped buffers, and idempotent CLI DAG pipelines.
- Distributed lease locks and constant-time cryptographic primitives.
- Fail-closed error handling with circuit breakers and graceful shutdown.
""".strip(),
    }

    @classmethod
    def get_active_domain(cls) -> str:
        """Reads active domain from .agents/state/active-domain.json."""
        if os.path.exists(cls.ACTIVE_DOMAIN_FILE):
            try:
                with open(cls.ACTIVE_DOMAIN_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    domain = data.get("activeDomain", data.get("domain", "systems"))
                    return domain
            except Exception:
                pass
        return "systems"

    @classmethod
    def assemble_compact_prompt(cls, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Assembles a compressed prompt including the 4 KB Core Kernel
        plus the single active domain overlay, pruning everything else.
        """
        active_dom = domain or cls.get_active_domain()
        # Map specific subdomains to overlay category
        category = "systems"
        if active_dom in ("blockchain", "web3"):
            category = "blockchain"
        elif active_dom in ("ai_ml", "machine_learning", "data_engineering", "datascience"):
            category = "ai_ml"
        elif active_dom in ("frontend", "ui", "web_app"):
            category = "frontend"
        else:
            category = "systems"

        overlay = cls.DOMAIN_SPECIFIC_OVERLAYS.get(category, "")
        full_compact = f"{cls.CORE_UNIVERSAL_KERNEL}\n\n{overlay}".strip()

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
