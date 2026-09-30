"""
Universal Task Dispatcher & Master Agentic Entry Point
Enables individual, autonomous execution of the workspace's core tasks:
  1. Solution Formulation (--task solution)
  2. Code Implementation & TDD Self-Healing (--task code)
  3. Presentation Pitch Deck Synthesis (--task presentation)
  4. Enterprise Security & Readiness Audit (--task audit)
  5. SQLite Memory Vault Search (--task memory)
"""

import os
import sys
import json
import argparse
import sqlite3
from typing import Dict, Any, Optional

from scripts.orchestrator.solution_council import SolutionCouncil
from scripts.orchestrator.coding_engine import CodingEngine
from scripts.orchestrator.project_auditor import ProjectAuditor
from scripts.orchestrator.research_triangulator import ResearchTriangulator
from scripts.orchestrator.domain_persona_engine import DomainPersonaEngine
from scripts.engine.planner import OmniDeckPlanner
from scripts.engine.deck_orchestrator import DeckOrchestrator


class TaskDispatcher:
    """
    Unified entry point routing tasks to the appropriate multi-agent subsystem,
    ensuring every prompt is executed through the full agentic system.
    """

    @classmethod
    def dispatch(cls, task: str, **kwargs) -> Dict[str, Any]:
        """Dispatches a task dynamically based on task type."""
        task_clean = task.lower().strip()

        if task_clean in ("solution", "solve", "1"):
            return cls._handle_solution(**kwargs)
        elif task_clean in ("code", "build", "tdd", "2"):
            return cls._handle_coding(**kwargs)
        elif task_clean in ("presentation", "pitch", "deck", "ppt", "3"):
            return cls._handle_presentation(**kwargs)
        elif task_clean in ("audit", "security", "pentest", "case_b"):
            return cls._handle_audit(**kwargs)
        elif task_clean in ("continue", "onboard", "case_c"):
            return cls._handle_continue(**kwargs)
        elif task_clean in ("memory", "vault", "search"):
            return cls._handle_memory(**kwargs)
        elif task_clean in ("squad", "agile", "enterprise", "team", "lifecycle"):
            return cls._handle_squad(**kwargs)
        elif task_clean in ("research", "deep_research", "investigate"):
            return cls._handle_research(**kwargs)
        elif task_clean in ("impact", "post_production", "product_analysis"):
            return cls._handle_impact(**kwargs)
        else:
            raise ValueError(f"Unknown task type '{task}'. Supported: solution, code, presentation, audit, continue, memory, squad, research, impact")

    @classmethod
    def _handle_solution(cls, **kwargs) -> Dict[str, Any]:
        """Task 1: Dispatches to SolutionCouncil."""
        title = kwargs.get("title") or kwargs.get("prompt") or "INNOVATION ARCHITECTURE"
        text = kwargs.get("text") or kwargs.get("prompt") or title
        active_state = DomainPersonaEngine.get_active_state()
        domain = kwargs.get("domain") or active_state.get("domain_name", "General Engineering")
        out_dir = kwargs.get("output_dir", "docs/dossiers")

        print(f"\n[TaskDispatcher] Routing to Task 1: SolutionCouncil ({domain})...")
        res = SolutionCouncil.formulate_solution(
            problem_title=title,
            problem_text=text,
            domain=domain,
            output_dir=out_dir
        )
        return res

    @classmethod
    def _handle_coding(cls, **kwargs) -> Dict[str, Any]:
        """Task 2: Dispatches to CodingEngine."""
        module_name = kwargs.get("module", "core_service")
        test_path = kwargs.get("test_path", f"tests/test_{module_name}.py")
        impl_path = kwargs.get("impl_path", f"src/{module_name}.py")
        test_code = kwargs.get("test_code")
        impl_generator = kwargs.get("impl_generator")

        if not test_code or not impl_generator:
            raise ValueError("Task 2 (code) requires 'test_code' and 'impl_generator' callable.")

        print(f"\n[TaskDispatcher] Routing to Task 2: CodingEngine TDD Loop ({module_name})...")
        res = CodingEngine.execute_tdd_loop(
            module_name=module_name,
            test_file_path=test_path,
            test_code=test_code,
            impl_file_path=impl_path,
            impl_code_generator=impl_generator,
            max_healing_passes=kwargs.get("max_passes", 5)
        )
        return res

    @classmethod
    def _handle_presentation(cls, **kwargs) -> Dict[str, Any]:
        """Task 3: Dispatches to OmniDeck Presentation Engine (PPTX First)."""
        prompt = kwargs.get("prompt") or kwargs.get("text") or "Enterprise Presentation"
        active_theme = DomainPersonaEngine.get_presentation_theme()
        theme = kwargs.get("theme") or active_theme or "cyber_dark_terminal"
        num_slides = kwargs.get("slides", 6)
        out_pptx = kwargs.get("output_pptx", "specs/presentations/deck_dispatcher_output.pptx")
        export_pdf = kwargs.get("export_pdf", False)
        out_pdf = kwargs.get("output_pdf", out_pptx.replace(".pptx", ".pdf"))

        print(f"\n[TaskDispatcher] Routing to Task 3: OmniDeck Presentation Engine (Theme: {theme})...")
        custom_specs = kwargs.get("custom_slides") or kwargs.get("custom_slide_specs")
        plan = OmniDeckPlanner.plan_from_prompt(
            prompt=prompt,
            theme_name=theme,
            num_slides=num_slides,
            custom_slide_specs=custom_specs
        )
        
        # Stage 1: Compile PPTX only (fast <0.2s)
        pptx_path = DeckOrchestrator.compile_pptx(plan, out_pptx)

        pdf_path = None
        if export_pdf:
            # Stage 2: Gated PDF Export
            pdf_path = DeckOrchestrator.export_approved_pdf(pptx_path, out_pdf, render_pngs=kwargs.get("render_pngs", False))

        return {
            "project_title": plan.project_title,
            "slides_count": len(plan.slides),
            "pptx_path": pptx_path,
            "pdf_path": pdf_path,
            "theme": theme
        }

    @classmethod
    def _handle_audit(cls, **kwargs) -> Dict[str, Any]:
        """Runs security and system audits or audits/remediates existing projects (Case B)."""
        target = kwargs.get("target")
        auto_heal = kwargs.get("auto_heal", False) or kwargs.get("remediate", False)
        output_report = kwargs.get("output_report", "docs/audits/remediation_audit.md")

        if target:
            print(f"\n[TaskDispatcher] Routing to ProjectAuditor for Target: {target}...")
            if auto_heal:
                return ProjectAuditor.remediate_project(
                    target_dir=target,
                    max_healing_passes=kwargs.get("max_passes", 5)
                )
            else:
                return ProjectAuditor.audit_project(
                    target_dir=target,
                    output_report_path=output_report
                )

        import subprocess
        print("\n[TaskDispatcher] Running Enterprise Security & Secret Audits...")
        sec_res = subprocess.run(["node", "--experimental-strip-types", "scripts/secret-scanner.ts"], capture_output=True, text=True)
        print(sec_res.stdout)
        return {"secret_scanner_exit_code": sec_res.returncode}

    @classmethod
    def _handle_continue(cls, **kwargs) -> Dict[str, Any]:
        """Task: Case C Hybrid Onboarding & Implementation."""
        target = kwargs.get("target")
        if not target:
            raise ValueError("Task 'continue' requires a '--target' directory or project path.")

        new_specs = kwargs.get("new_specs") or kwargs.get("specs") or None

        print(f"\n[TaskDispatcher] Routing to ProjectAuditor.onboard_and_continue for Target: {target}...")
        return ProjectAuditor.onboard_and_continue(
            target_dir=target,
            new_features_spec=new_specs
        )

    @classmethod
    def _handle_memory(cls, **kwargs) -> Dict[str, Any]:
        """Searches SQLite Memory Vault."""
        query = kwargs.get("query", "").lower()
        db_path = os.path.join(os.getcwd(), ".agents", "memory", "vault.sqlite")
        results = []

        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT id, title, kind, created_at, body, file_path FROM memories WHERE lower(title) LIKE ? OR lower(body) LIKE ?", (f"%{query}%", f"%{query}%"))
            rows = cur.fetchall()
            for r in rows:
                results.append({
                    "id": r[0], "title": r[1], "kind": r[2], "created_at": r[3],
                    "snippet": r[4][:120], "file_path": r[5]
                })
            conn.close()

        print(f"\n[TaskDispatcher] Memory Vault Search for '{query}': Found {len(results)} records.")
        return {"query": query, "matches": results}

    @classmethod
    def _handle_squad(cls, **kwargs) -> Dict[str, Any]:
        """Task: Enterprise Agile Product Squad Orchestrator."""
        from scripts.orchestrator.squad_orchestrator import SquadOrchestrator
        feature = kwargs.get("feature") or kwargs.get("module") or "enterprise_feature"
        prompt = kwargs.get("prompt") or f"Implement production-grade {feature} with reactive state persistence and strict gating."
        test_path = kwargs.get("test_path", f"specs/scratch_tests/test_{feature}.py")
        impl_path = kwargs.get("impl_path", f"specs/scratch_tests/{feature}.py")
        test_code = kwargs.get("test_code")
        impl_generator = kwargs.get("impl_generator")
        mode = kwargs.get("mode", "solo")

        # Ensure clean baseline for red-phase verification
        if os.path.exists(impl_path):
            try:
                os.remove(impl_path)
            except Exception:
                pass

        if not test_code:
            class_name = "".join([part.capitalize() for part in feature.split("_")]) + "Service"
            test_code = f'''
import unittest
from specs.scratch_tests.{feature} import {class_name}

class Test{class_name}(unittest.TestCase):
    def test_service_initialization(self):
        srv = {class_name}()
        self.assertEqual(srv.status, "IDLE")

    def test_operation_gating(self):
        srv = {class_name}()
        with self.assertRaises(PermissionError):
            srv.execute_statutory_action()

    def test_complete_verified_flow(self):
        srv = {class_name}()
        srv.start()
        self.assertEqual(srv.status, "RUNNING")
        srv.complete(score=0.98)
        self.assertEqual(srv.status, "COMPLETED")
        receipt = srv.execute_statutory_action()
        self.assertTrue(receipt["success"])
        self.assertEqual(srv.status, "CERTIFIED")

    def test_fail_state(self):
        srv = {class_name}()
        srv.fail()
        self.assertEqual(srv.status, "FAILED")
'''

        if not impl_generator:
            class_name = "".join([part.capitalize() for part in feature.split("_")]) + "Service"
            impl_generator = lambda it, err: f'''
class {class_name}:
    def __init__(self):
        self.status = "IDLE"
        self.score = 0.0

    def start(self):
        self.status = "RUNNING"

    def complete(self, score: float):
        self.status = "COMPLETED"
        self.score = score

    def fail(self):
        self.status = "FAILED"

    def execute_statutory_action(self):
        if self.status not in ["COMPLETED", "CERTIFIED"]:
            raise PermissionError("Prerequisite engine must complete before statutory action.")
        self.status = "CERTIFIED"
        return {{"success": True, "score": self.score}}
'''

        print(f"\n[TaskDispatcher] Routing to Enterprise Agile Product Squad ({feature}, mode: {mode})...")
        res = SquadOrchestrator.execute_squad_feature(
            feature_name=feature,
            user_prompt=prompt,
            test_file_path=test_path,
            test_code=test_code,
            impl_file_path=impl_path,
            impl_code_generator=impl_generator,
            mode=mode
        )
        import dataclasses
        return dataclasses.asdict(res)

    @classmethod
    def _handle_research(cls, **kwargs) -> Dict[str, Any]:
        """Dispatches to DeepResearchSpecialist / ResearchTriangulator."""
        title = kwargs.get("title") or kwargs.get("prompt") or "Autonomous System Research"
        text = kwargs.get("text") or kwargs.get("prompt") or title
        active_state = DomainPersonaEngine.get_active_state()
        domain = kwargs.get("domain") or active_state.get("domain_name", "General Engineering")
        mode = kwargs.get("research_mode") or kwargs.get("mode") or "EXPLORATION"
        min_time = kwargs.get("min_time", 0.0)

        print(f"\n[TaskDispatcher] Routing to Deep Research Specialist ({domain}, mode: {mode})...")
        res = ResearchTriangulator.triangulate(
            problem_title=title,
            problem_text=text,
            domain=domain,
            mode=mode,
            min_deliberation_seconds=float(min_time)
        )
        import dataclasses
        return dataclasses.asdict(res)

    @classmethod
    def _handle_impact(cls, **kwargs) -> Dict[str, Any]:
        """Dispatches to ResearchTriangulator for Post-Production Impact Analysis."""
        title = kwargs.get("title") or kwargs.get("feature") or kwargs.get("target") or "Production Platform"
        active_state = DomainPersonaEngine.get_active_state()
        domain = kwargs.get("domain") or active_state.get("domain_name", "Enterprise Software")
        metrics = kwargs.get("empirical_metrics") or {}

        print(f"\n[TaskDispatcher] Routing to Post-Production Impact Analysis ({title})...")
        res = ResearchTriangulator.triangulate(
            problem_title=title,
            domain=domain,
            mode="IMPACT",
            empirical_metrics=metrics
        )
        import dataclasses
        return dataclasses.asdict(res)


def main():
    parser = argparse.ArgumentParser(description="Universal Task Dispatcher for Enterprise Agentic System")
    parser.add_argument("--task", required=True, choices=["solution", "code", "presentation", "audit", "continue", "memory", "squad", "research", "impact"], help="Task to execute")
    parser.add_argument("--target", help="Target project directory or blueprint file for audit/remediation or continuation")
    parser.add_argument("--feature", default="case_service", help="Feature name for squad lifecycle")
    parser.add_argument("--mode", default="solo", choices=["solo", "dual"], help="Operator mode (solo or dual)")
    parser.add_argument("--auto-heal", action="store_true", help="Automatically trigger red-to-green remediation on detected flaws")
    parser.add_argument("--output-report", default="docs/audits/remediation_audit.md", help="Path to write audit/remediation report")
    parser.add_argument("--prompt", help="Natural language prompt or problem statement")
    parser.add_argument("--title", help="Problem statement title")
    parser.add_argument("--domain", default=None, help="Domain area (defaults to active domain)")
    parser.add_argument("--theme", default=None, help="Presentation theme (defaults to active domain theme)")
    parser.add_argument("--slides", type=int, default=6, help="Number of presentation slides")
    parser.add_argument("--export-pdf", action="store_true", help="Explicit order to export approved PPTX to PDF")
    parser.add_argument("--query", default="", help="Memory search query")
    parser.add_argument("--research-mode", default="EXPLORATION", choices=["EXPLORATION", "FEASIBILITY", "DIAGNOSTIC", "IMPACT"], help="Research mode")
    parser.add_argument("--min-time", type=float, default=0.0, help="Minimum deliberation seconds (0 for rapid, 120 for deep)")

    args = parser.parse_args()

    res = TaskDispatcher.dispatch(
        task=args.task,
        target=args.target,
        feature=args.feature,
        mode=args.mode,
        auto_heal=args.auto_heal,
        output_report=args.output_report,
        prompt=args.prompt,
        title=args.title,
        domain=args.domain,
        theme=args.theme,
        slides=args.slides,
        export_pdf=args.export_pdf,
        query=args.query,
        research_mode=args.research_mode,
        min_time=args.min_time
    )
    print("\n[TaskDispatcher] Task Result:")
    import dataclasses
    if dataclasses.is_dataclass(res):
        out_dict = dataclasses.asdict(res)
    elif isinstance(res, dict):
        out_dict = {k: v for k, v in res.items() if not k.startswith('_')}
    else:
        out_dict = str(res)
    print(json.dumps(out_dict, indent=2, default=str))


if __name__ == "__main__":
    main()
