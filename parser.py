from models import WebLog, AuthLog
from datetime import datetime


def parse_web(line: str) -> WebLog | None:
    try:
        parts = line.split()
        ip = parts[0]

        ts_raw = line.split("[", 1)[1].split("]", 1)[0]
        timestamp = datetime.strptime(ts_raw, "%d/%b/%Y:%H:%M:%S %z")

        request = line.split('"')[1]
        method = request.split(" ", 1)[0]
        path = request[len(method) + 1 : request.rfind(" HTTP")]

        status = int(parts[-2])

        return WebLog(
            source="web",
            ip=ip,
            timestamp=timestamp,
            method=method,
            path=path,
            status=status,
        )

    except (IndexError, ValueError):
        return None


def parse_auth(line: str) -> AuthLog | None:
    if " server " not in line:
        return None

    ts = " ".join(line.split()[:3])

    ip = None
    if " from " in line:
        ip = line.split(" from ")[1].split()[0]

    return AuthLog(
        source="auth",
        timestamp=ts,
        message=line,
        ip=ip,
    )
