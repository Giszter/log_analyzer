import pytest
from rules_engine import RuleEngine
from models import AuthLog


@pytest.mark.parametrize(
    "messages, expected_severities",
    [
        (
            [
                "Failed password",
                "Failed password",
                "Failed password",
                "Accepted password",
            ],
            {"high", "critical"},
        ),
        (
            [
                "Failed password",
                "Failed password",
                "Failed password",
            ],
            {"high"},
        ),
    ],
)
def test_ssh_bruteforce_detection(messages, expected_severities):
    rules = [
        {
            "id": "ssh_failed_logins",
            "source": "auth",
            "where": {"message_contains": "Failed password"},
            "group_by": "ip",
            "threshold": 3,
            "severity": "high",
            "escalate_on": {
                "message_contains": "Accepted password",
                "severity": "critical",
            },
        }
    ]

    engine = RuleEngine(rules)

    alerts = []
    for msg in messages:
        log = AuthLog(source="auth", timestamp=None, message=msg, ip="1.2.3.4")
        alerts.extend(engine.process(log))

    severities = {a["severity"] for a in alerts}

    assert severities == expected_severities
