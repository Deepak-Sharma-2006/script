"""
Unit tests for newly delivered Python touchpoints:
- GroupChatManager (AutoGen AG2)
- TaskDAGRunner (CrewAI)
- StateGraph (LangGraph)
"""

import unittest
import os
import json
import sqlite3
from scripts.orchestrator.groupchat import GroupChatManager, ChatAgent
from scripts.orchestrator.task_dag_runner import TaskDAGRunner, DAGTask
from scripts.orchestrator.state_graph import StateGraph


class TestSota18Ingestion(unittest.TestCase):

    def test_touchpoint_autogen_groupchat(self):
        """Touchpoint 4: AutoGen GroupChat Manager with dynamic speaker routing."""
        agent1 = ChatAgent("security_auditor", "Audits security vulnerabilities", ["security", "vulnerability", "leak"])
        agent2 = ChatAgent("perf_engineer", "Optimizes latency and throughput", ["latency", "speed", "memory", "perf"])

        manager = GroupChatManager([agent1, agent2], max_rounds=4)

        # Test dynamic speaker selection
        speaker_sec = manager.select_next_speaker("Found a potential memory leak and security vulnerability")
        self.assertEqual(speaker_sec.name, "security_auditor")

        speaker_perf = manager.select_next_speaker("Need to improve query latency and execution speed")
        self.assertEqual(speaker_perf.name, "perf_engineer")

        # Test dialogue loop
        msgs = manager.run_dialogue("Optimize system throughput and resolve memory leak", rounds=2)
        self.assertGreaterEqual(len(msgs), 3)  # HumanOperator + 2 turns

    def test_touchpoint_crewai_task_dag_runner(self):
        """Touchpoint 5: CrewAI Task DAG Delegation with Output Validation."""
        runner = TaskDAGRunner()
        runner.add_task(DAGTask("fetch", "Fetch data", required_output_keys=["raw_data"]))
        runner.add_task(DAGTask("process", "Process data", dependencies=["fetch"], required_output_keys=["cleaned"]))

        runner.tasks["fetch"].executor = lambda inp: {"raw_data": [1, 2, 3]}
        runner.tasks["process"].executor = lambda inp: {"cleaned": [x * 2 for x in inp["fetch"]["raw_data"]]}

        res = runner.execute()
        self.assertIn("fetch", res)
        self.assertIn("process", res)
        self.assertEqual(res["process"]["cleaned"], [2, 4, 6])

        # Test failure on missing schema key
        broken_runner = TaskDAGRunner()
        broken_runner.add_task(DAGTask("broken", "Missing key", required_output_keys=["missing_key"]))
        broken_runner.tasks["broken"].executor = lambda inp: {"wrong_key": 1}
        with self.assertRaises(ValueError):
            broken_runner.execute()

    def test_touchpoint_langgraph_state_graph_and_rollback(self):
        """Touchpoint 9: LangGraph Cyclic State Graph with SQLite Checkpoints and Rollback."""
        graph = StateGraph("test_rollback_graph")

        def step1(s):
            return {**s, "counter": s.get("counter", 0) + 1}

        def step2(s):
            return {**s, "completed": s["counter"] >= 2}

        graph.add_node("step1", step1)
        graph.add_node("step2", step2)
        graph.set_entry_point("step1")
        graph.add_edge("step1", "step2")
        graph.add_conditional_edge("step2", lambda s: "END" if s.get("completed") else "step1")

        final = graph.execute({"counter": 0}, max_iterations=6)
        self.assertEqual(final["completed"], True)
        self.assertEqual(final["__status__"], "COMPLETED")

        # Verify checkpoints saved in SQLite
        db_path = StateGraph.DB_PATH
        self.assertTrue(os.path.exists(db_path))
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT checkpoint_id, state_json FROM checkpoints WHERE graph_name = 'test_rollback_graph'")
            rows = cursor.fetchall()
            self.assertGreater(len(rows), 0)
            chk_id, state_str = rows[0]

            # Verify rollback
            restored = graph.rollback_to(chk_id)
            self.assertIsNotNone(restored)
            self.assertIn("counter", restored)


if __name__ == "__main__":
    unittest.main()
