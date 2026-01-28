import yaml
from pathlib import Path

DEFAULT_RULES_FILE = "rules.yml"


def load_rules(path: str | None) -> list[dict]:
    if path:
        rules_path = Path(path)
    else:
        rules_path = Path(DEFAULT_RULES_FILE)

    if not rules_path.exists():
        if path:
            print(f"[WARN] Rules file not found: {rules_path} (rules disabled)")
        return []

    try:
        with rules_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except OSError as e:
        print(f"[WARN] Cannot read rules file: {e} (rules disabled)")
        return []

    return data.get("rules", [])
