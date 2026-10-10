"""
scripts/orchestrator/state_graph.py
Upstream Reference: langchain-ai/langgraph (42.7k stars)

Cyclic State Graph with Persistent Checkpointing and Time-Travel Rollback.
Maintains state machine execution across cycles, saves full execution state
snapshots to SQLite, and supports deterministic rollback to previous checkpoints.
"""

import os
import sys
import json
import sqlite3
import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field


@dataclass
class StateGraphNode:
    name: str
    action: Callable[[Dict[str, Any]], Dict[str, Any]]


class StateGraph:
    """
    Cyclic execution graph with persistent SQLite checkpoints and time-travel rollback.
    """

    DB_PATH = os.path.join(".agents", "state", "state_graph.sqlite")

    def __init__(self, name: str = "default_graph"):
        self.name = name
        self.nodes: Dict[str, StateGraphNode] = {}
        self.edges: Dict[str, str] = {}  # node -> next_node
        self.conditional_edges: Dict[str, Callable[[Dict[str, Any]], str]] = {}
        self.entry_point: Optional[str] = None
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.DB_PATH), exist_ok=True)
        with sqlite3.connect(self.DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    graph_name TEXT NOT NULL,
                    node_name TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    iteration INTEGER NOT NULL,
                    timestamp REAL NOT NULL
                )
            """)
            conn.commit()

    def add_node(self, name: str, action: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.nodes[name] = StateGraphNode(name, action)

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node

    def add_conditional_edge(self, from_node: str, router_func: Callable[[Dict[str, Any]], str]):
        self.conditional_edges[from_node] = router_func

    def save_checkpoint(self, node_name: str, state: Dict[str, Any], iteration: int) -> int:
        with sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO checkpoints (graph_name, node_name, state_json, iteration, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (self.name, node_name, json.dumps(state), iteration, time.time()))
            conn.commit()
            return cursor.lastrowid

    def rollback_to(self, checkpoint_id: int) -> Optional[Dict[str, Any]]:
        """
        Time-travel rollback: restores state from a previously saved checkpoint.
        """
        with sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT state_json FROM checkpoints
                WHERE checkpoint_id = ? AND graph_name = ?
            """, (checkpoint_id, self.name))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None

    def execute(self, initial_state: Dict[str, Any], max_iterations: int = 15) -> Dict[str, Any]:
        """
        Executes graph until an 'END' state is reached or max_iterations exceeded.
        """
        if not self.entry_point or self.entry_point not in self.nodes:
            raise ValueError(f"Invalid entry point '{self.entry_point}'")

        current_node_name = self.entry_point
        state = dict(initial_state)

        for iteration in range(1, max_iterations + 1):
            node = self.nodes[current_node_name]
            # Execute node logic
            state = node.action(state)
            self.save_checkpoint(current_node_name, state, iteration)

            # Determine next node
            if current_node_name in self.conditional_edges:
                next_node_name = self.conditional_edges[current_node_name](state)
            else:
                next_node_name = self.edges.get(current_node_name, "END")

            if next_node_name == "END":
                state["__status__"] = "COMPLETED"
                break

            if next_node_name not in self.nodes:
                raise ValueError(f"Next node '{next_node_name}' not defined in graph")

            current_node_name = next_node_name
        else:
            state["__status__"] = "MAX_ITERATIONS_REACHED"

        return state


if __name__ == "__main__":
    g = StateGraph("test_self_heal")
    g.add_node("implement", lambda s: {**s, "code": "def solve(): return True", "attempts": s.get("attempts", 0) + 1})
    g.add_node("test", lambda s: {**s, "passed": s["attempts"] >= 2})

    g.set_entry_point("implement")
    g.add_edge("implement", "test")
    g.add_conditional_edge("test", lambda s: "END" if s.get("passed") else "implement")

    final = g.execute({"attempts": 0})
    print("StateGraph (LangGraph Cyclic State & Time-Travel Rollback) - Finished:", final)
