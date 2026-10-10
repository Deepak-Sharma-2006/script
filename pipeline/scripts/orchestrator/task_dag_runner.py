"""
scripts/orchestrator/task_dag_runner.py
Upstream Reference: crewAIInc/crewAI (59.4k stars)

Deterministic Task DAG Delegation with Output Validation.
Replaces probabilistic agent chains with mathematically ordered Directed Acyclic Graphs (DAGs)
where task outputs are strictly validated against typed schemas.
"""

import sys
import os
import json
import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from scripts.orchestrator.dag_runner import DAGRunner


@dataclass
class DAGTask:
    task_id: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    required_output_keys: List[str] = field(default_factory=list)
    executor: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None


class TaskDAGRunner:
    """
    Executes tasks in topological order, verifying that all output dictionaries
    strictly satisfy declared schema keys before passing downstream.
    """

    def __init__(self):
        self.tasks: Dict[str, DAGTask] = {}
        self.results: Dict[str, Dict[str, Any]] = {}

    def add_task(self, task: DAGTask):
        self.tasks[task.task_id] = task

    def get_execution_order(self) -> List[str]:
        """Topological sort using Kahn's algorithm."""
        in_degree = {t_id: 0 for t_id in self.tasks}
        for task in self.tasks.values():
            for dep in task.dependencies:
                if dep not in self.tasks:
                    raise ValueError(f"Task '{task.task_id}' depends on undefined task '{dep}'")
            in_degree[task.task_id] = len(task.dependencies)

        queue = [t_id for t_id, deg in in_degree.items() if deg == 0]
        order = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)

            for task in self.tasks.values():
                if curr in task.dependencies:
                    in_degree[task.task_id] -= 1
                    if in_degree[task.task_id] == 0:
                        queue.append(task.task_id)

        if len(order) != len(self.tasks):
            raise ValueError("Cycle detected in Task DAG dependencies! Execution aborted.")

        return order

    def execute(self) -> Dict[str, Any]:
        """Executes all DAG tasks and validates schema integrity."""
        order = self.get_execution_order()

        for t_id in order:
            task = self.tasks[t_id]
            # Aggregate inputs from upstream dependencies
            inputs = {dep: self.results.get(dep, {}) for dep in task.dependencies}

            if task.executor:
                out = task.executor(inputs)
            else:
                out = {"status": "completed", "task_id": t_id, "timestamp": time.time()}

            # Strict Output Schema Validation
            missing_keys = [k for k in task.required_output_keys if k not in out]
            if missing_keys:
                raise ValueError(f"Task '{t_id}' output failed schema validation! Missing required keys: {missing_keys}")

            self.results[t_id] = out

        return self.results


if __name__ == "__main__":
    runner = TaskDAGRunner()
    runner.add_task(DAGTask("scrape", "Scrape source data", required_output_keys=["data"]))
    runner.add_task(DAGTask("rank", "Rank items", dependencies=["scrape"], required_output_keys=["ranked"]))
    runner.add_task(DAGTask("visualize", "Generate UI", dependencies=["rank"], required_output_keys=["rendered"]))

    # Test run
    runner.tasks["scrape"].executor = lambda inp: {"data": [1, 2, 3]}
    runner.tasks["rank"].executor = lambda inp: {"ranked": sorted(inp["scrape"]["data"], reverse=True)}
    runner.tasks["visualize"].executor = lambda inp: {"rendered": "<html>ok</html>"}

    res = runner.execute()
    print("TaskDAGRunner (CrewAI Deterministic Task DAG Delegation) - Execution Success:", list(res.keys()))
