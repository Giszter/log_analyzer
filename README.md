# Security Log Analyzer (Python)

A simple, extensible command-line tool for analyzing security logs and detecting suspicious activity using configurable rules.

The project focuses on **clarity, determinism, and testability** rather than complex heuristics or machine learning.

---

## Features

- CLI built with `click`
- Supports multiple log files as input
- Parses different log formats:
  - Web server access logs
  - Authentication (`auth.log`) logs
- Declarative detection rules defined in YAML
- Stateful detections (e.g. brute-force followed by success)
- Safe handling of malformed log entries
- Minimal dependencies, deterministic behavior
- Linted and formatted with **Ruff**
- Covered by focused unit tests (pytest)

---

## Supported Detections (Examples)

- Web login brute-force attempts
- SSH failed login attempts
- SSH brute-force **followed by successful login** (escalation)
- SQL injection attempts (`UNION SELECT`, `DROP TABLE`, etc.)
- Malformed log entries are ignored safely

---

## Usage
example
bash
`python main.py webserver.log auth.log`

Optional custom rules file:
python main.py webserver.log auth.log --rules custom_rules.yml
If --rules is not provided, the tool automatically falls back to ./rules.yml if present.

---

## Rules Configuration
Rules are defined declaratively in YAML:
rules:
```
  - id: ssh_failed_logins
    source: auth
    where:
      message_contains: "Failed password"
    group_by: ip
    threshold: 3
    severity: high
    escalate_on:
      message_contains: "Accepted password"
      severity: critical
```
### Rule Concepts
```
source — log source (web or auth)
where — matching conditions
group_by — aggregation key (e.g. IP)
threshold — number of occurrences required
escalate_on — optional escalation condition
```