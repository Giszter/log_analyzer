from pathlib import Path


def read_logs(paths: list[str]) -> list[str]:
    lines = []

    for p in paths:
        path = Path(p)

        if not path.exists():
            print(f"[WARN] File not found: {path}")
            continue

        if not path.is_file():
            print(f"[WARN] Not a file: {path}")
            continue

        try:
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        lines.append(line)
        except OSError as e:
            print(f"[ERROR] Cannot read {path}: {e}")

    return lines
