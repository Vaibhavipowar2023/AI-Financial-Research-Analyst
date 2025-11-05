from typing import Dict
from crew.core.crewai_shim import Agent
from services.llm import llm, llm_concise
from utils.yaml_loader import AGENTS_CFG

_LLM_MAP = {
    'default': llm,
    'concise': llm_concise,
}

def build_agents() -> Dict[str, Agent]:
    out: Dict[str, Agent] = {}
    for key, spec in AGENTS_CFG['agents'].items():
        agent = Agent(
            role=spec.get('role', ''),
            goal=spec.get('goal', ''),
            backstory=spec.get('backstory', ''),
            llm=_LLM_MAP.get(spec.get('llm', 'default'), llm),
            max_iter=spec.get('max_iter', 1),
            allow_delegation=spec.get('allow_delegation', False),
        )
        out[key] = agent
    return out
