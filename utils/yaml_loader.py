import os
import yaml
from typing import Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

def load_yaml_file(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as fh:
        return yaml.safe_load(fh)

AGENTS_CFG = load_yaml_file(os.path.join(CONFIG_DIR, "agents.yaml"))
TASK_CFG = load_yaml_file(os.path.join(CONFIG_DIR, "task.yaml"))
