import os
import yaml
from crew.core.crewai_shim import Task
from utils.yaml_loader import TASK_CFG


def _render_template(template: str, context: dict) -> str:
    """Safely format a YAML template with context."""
    try:
        return template.format(**context)
    except Exception:
        out = template
        for k, v in context.items():
            out = out.replace("{" + k + "}", str(v))
        return out


def make_news_task(agent, context):
    cfg = TASK_CFG.get("news", {})
    desc = _render_template(cfg.get("description", ""), context)
    return Task(description=desc, agent=agent)


def make_indicators_task(agent, context):
    cfg = TASK_CFG.get("indicators", {})
    desc = _render_template(cfg.get("description", ""), context)
    return Task(description=desc, agent=agent)


def make_strategy_task(agent, context):
    cfg = TASK_CFG.get("strategy", {})
    desc = _render_template(cfg.get("description", ""), context)
    return Task(description=desc, agent=agent)


def make_report_task(agent, context):
    cfg = TASK_CFG.get("report", {})
    desc = _render_template(cfg.get("description", ""), context)
    return Task(description=desc, agent=agent)
