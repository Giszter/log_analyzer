from collections import defaultdict


class RuleEngine:
    def __init__(self, rules: list[dict]):
        self.rules = rules
        self.counters = defaultdict(lambda: defaultdict(int))
        self.triggered = defaultdict(set)

    def process(self, log):
        alerts = []

        for rule in self.rules:
            if rule["source"] != log.source:
                continue

            rule_id = rule["id"]
            group_by = rule["group_by"]
            key = getattr(log, group_by, None)

            if key is None:
                continue

            if "escalate_on" in rule and key in self.triggered[rule_id]:
                esc = rule["escalate_on"]

                if self._match_where(esc, log):
                    alerts.append(
                        {
                            "rule_id": rule_id,
                            "key": key,
                            "severity": esc.get("severity", rule["severity"]),
                            "type": "escalation",
                        }
                    )

            if not self._match_where(rule.get("where", {}), log):
                continue

            self.counters[rule_id][key] += 1

            if self.counters[rule_id][key] == rule["threshold"]:
                self.triggered[rule_id].add(key)

                alerts.append(
                    {
                        "rule_id": rule_id,
                        "key": key,
                        "severity": rule["severity"],
                        "type": "threshold",
                    }
                )

        return alerts

    def _match_where(self, where: dict, log) -> bool:
        for field, value in where.items():
            if field == "severity":
                continue

            if field.endswith("_contains"):
                attr = field.replace("_contains", "")
                text = str(getattr(log, attr, "")).lower()
                if value.lower() not in text:
                    return False
            else:
                if getattr(log, field, None) != value:
                    return False

        return True
