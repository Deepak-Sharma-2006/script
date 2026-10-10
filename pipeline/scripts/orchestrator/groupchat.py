"""
scripts/orchestrator/groupchat.py
Upstream Reference: microsoft/autogen - AG2 (61.3k stars)

Asynchronous GroupChat Manager with Dynamic Speaker Routing.
Enables multi-persona adversarial debate without deadlock, dynamically
selecting the most relevant expert persona based on conversation state.
"""

import sys
import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field


@dataclass
class GroupChatMessage:
    sender: str
    recipient: str
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatAgent:
    name: str
    role_description: str
    expertise_keywords: List[str]
    reply_func: Optional[Callable[[str, List[GroupChatMessage]], str]] = None


class GroupChatManager:
    """
    Orchestrates dynamic multi-agent group discussions.
    Dynamically routes speaking turns based on topic keywords and conversation context.
    """

    def __init__(self, agents: List[ChatAgent], max_rounds: int = 10):
        self.agents = {agent.name: agent for agent in agents}
        self.max_rounds = max_rounds
        self.messages: List[GroupChatMessage] = []

    def select_next_speaker(self, last_message: str, previous_speaker: Optional[str] = None) -> ChatAgent:
        """
        Dynamically selects the next most qualified speaker based on keywords,
        avoiding speaker monopoly and preventing deadlocks.
        """
        lower_msg = last_message.lower()
        scored_agents: List[tuple[int, ChatAgent]] = []

        for name, agent in self.agents.items():
            if name == previous_speaker and len(self.agents) > 1:
                # Penalize consecutive turns by the same speaker
                score = -2
            else:
                score = 0

            for kw in agent.expertise_keywords:
                if kw.lower() in lower_msg:
                    score += 3

            scored_agents.append((score, agent))

        # Sort descending by score
        scored_agents.sort(key=lambda x: x[0], reverse=True)
        return scored_agents[0][1]

    def broadcast_message(self, sender: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        msg = GroupChatMessage(
            sender=sender,
            recipient="all",
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(msg)

    def run_dialogue(self, initial_prompt: str, rounds: Optional[int] = None) -> List[GroupChatMessage]:
        """
        Runs an asynchronous-style multi-agent deliberation loop up to max_rounds.
        """
        rounds_to_run = rounds or self.max_rounds
        self.broadcast_message(sender="HumanOperator", content=initial_prompt)

        current_speaker: Optional[str] = None
        last_content = initial_prompt

        for round_idx in range(rounds_to_run):
            next_agent = self.select_next_speaker(last_content, previous_speaker=current_speaker)
            current_speaker = next_agent.name

            if next_agent.reply_func:
                reply = next_agent.reply_func(last_content, self.messages)
            else:
                reply = f"[{next_agent.name}]: Analyzed perspective on '{last_content[:40]}...' adhering to {next_agent.role_description}."

            self.broadcast_message(sender=next_agent.name, content=reply)
            last_content = reply

            # Stop condition if consensus reached
            if "CONCENSUS_REACHED" in reply or "VERDICT: APPROVED" in reply:
                break

        return self.messages


if __name__ == "__main__":
    # Self-test default council
    council_agents = [
        ChatAgent("01-contrarian", "Attacks assumptions and uncovers failure modes", ["fail", "risk", "attack", "vulnerability"]),
        ChatAgent("02-first-principles", "Audits raw algorithmic complexity and latency", ["performance", "speed", "complexity", "ast"]),
        ChatAgent("03-expansionist", "Formulates defensible 10x moats and extensibility", ["moat", "scale", "feature", "future"]),
        ChatAgent("04-outsider", "Audits cognitive ergonomics and usability", ["ergonomics", "simple", "clarity", "clutter"]),
        ChatAgent("05-executor", "Enforces concrete implementation and benchmarks", ["deploy", "run", "test", "benchmark"])
    ]
    manager = GroupChatManager(council_agents, max_rounds=5)
    msgs = manager.run_dialogue("Audit feature rationalization plan for 45 CLI scripts")
    print(f"GroupChat Deliberation Complete: {len(msgs)} messages recorded.")
    for m in msgs:
        print(f"  {m.sender:20} -> {m.content[:70]}...")
