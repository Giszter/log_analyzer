from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class WebLog:
    source: str
    ip: str
    timestamp: datetime
    method: str
    path: str
    status: int


@dataclass
class AuthLog:
    source: str
    timestamp: datetime
    message: str
    ip: str | None = None


IP_PREFIX = re.compile(r"^\d{1,3}(\.\d{1,3}){3}\s")
AUTH_RE = re.compile(r"\bserver\b.*\b(sshd|sudo)\b")


def detect_log_type(line: str) -> str:
    if IP_PREFIX.match(line):
        return "web"

    if AUTH_RE.search(line):
        return "auth"

    return "unknown"
