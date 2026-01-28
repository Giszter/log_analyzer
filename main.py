import click
from reader import read_logs
from models import detect_log_type
from parser import parse_web, parse_auth
from rules_loader import load_rules
from rules_engine import RuleEngine

import click

from reader import read_logs
from models import detect_log_type
from parser import parse_web, parse_auth
from rules_loader import load_rules
from rules_engine import RuleEngine


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=False))
@click.option(
    "--rules",
    "rules_path",
    default=None,
    help="Optional path to rules YAML file (defaults to ./rules.yml)",
)
def cli(paths, rules_path):
    if not paths:
        raise click.UsageError(
            "No log files provided.\nUsage: python main.py <logfile1> [logfile2 ...]"
        )

    rules = load_rules(rules_path)
    engine = RuleEngine(rules)

    alerts = []

    # 🔥 PRZETWARZAJ LOGI LINIA PO LINII (ZACHOWUJ KOLEJNOŚĆ)
    for line in read_logs(paths):
        log_type = detect_log_type(line)

        if log_type == "web":
            log = parse_web(line)
        elif log_type == "auth":
            log = parse_auth(line)
        else:
            continue

        if not log:
            continue

        # RuleEngine dostaje event NATYCHMIAST
        for alert in engine.process(log):
            alerts.append(alert)

    if not alerts:
        click.echo("No alerts detected.")
        return

    click.echo("\n=== Alerts ===")
    for alert in alerts:
        alert_type = alert.get("type", "threshold")

        click.echo(
            f"[{alert['severity'].upper()}] "
            f"{alert['rule_id']} ({alert_type}) → {alert['key']}"
        )


if __name__ == "__main__":
    cli()
