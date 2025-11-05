from dataclasses import dataclass
from typing import Any, List

@dataclass
class Task:
    description: str
    agent: Any = None

class Agent:
    def __init__(self, role: str = "", goal: str = "", backstory: str = "", llm=None, max_iter: int = 1, allow_delegation: bool = False, **kwargs):
        """
        Minimal Agent shim. `llm` should be a callable that accepts a prompt and returns text.
        """
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = llm
        self.max_iter = max_iter
        self.allow_delegation = allow_delegation
        self._kwargs = kwargs

    def run(self, task: Task) -> str:
        prompt = f"Role: {self.role}\nGoal: {self.goal}\nBackstory: {self.backstory}\nTask:\n{task.description}"
        if callable(self.llm):
            try:
                return self.llm(prompt)
            except Exception as e:
                return f"LLM_ERROR: {e}"
        return "NO_LLM_AVAILABLE: " + (prompt[:800] + ("..." if len(prompt) > 800 else ""))

class Process:
    sequential = "sequential"
    parallel = "parallel"

class Crew:
    def __init__(self, agents: List[Agent] = None, tasks: List[Task] = None, process=Process.sequential, verbose: bool = False, **kwargs):
        self.agents = agents or []
        self.tasks = tasks or []
        self.process = process
        self.verbose = verbose
        self._kwargs = kwargs

    def kickoff(self):
        results = []
        for t in self.tasks:
            agent = getattr(t, "agent", None) or (self.agents[0] if self.agents else None)
            if agent is None:
                results.append("NO_AGENT_ASSIGNED")
                continue
            out = agent.run(t)
            results.append(out)
        class Out:
            def __init__(self, raw):
                self.raw = raw
            def __str__(self):
                return str(self.raw)
        # When multiple tasks, return joined text. Keep format compatible with original code which checks .raw
        return Out(raw="\n\n".join(results))
