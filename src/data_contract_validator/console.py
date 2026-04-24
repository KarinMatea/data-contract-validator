from collections.abc import Sequence
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_summary(
    valid_records: Sequence[Any],
    errors: Sequence[dict[str, Any]],
) -> None:
    total = len(valid_records) + len(errors)
    summary = Table(show_header=False, box=None, padding=(0, 2))
    summary.add_row("Total records", str(total))
    summary.add_row("Valid records", f"[green]{len(valid_records)}[/green]")
    summary.add_row("Invalid records", f"[red]{len(errors)}[/red]")
    console.print(Panel(summary, title="Validation Summary", expand=False))


def print_odds_events_table(valid_records: Sequence[Any]) -> None:
    if not valid_records:
        console.print("[yellow]No valid odds events found.[/yellow]")
        return

    table = Table(title="Tennis Odds Events", header_style="bold cyan")
    table.add_column("Sport", style="magenta")
    table.add_column("Match", style="white")
    table.add_column("Commence Time", style="green")
    table.add_column("Bookmakers", justify="right")
    table.add_column("Markets", justify="right")

    for event in valid_records:
        match_name = f"{event.home_team} vs {event.away_team}"
        table.add_row(
            event.sport_title,
            match_name,
            event.commence_time,
            str(event.bookmaker_count),
            str(event.market_count),
        )

    console.print(table)


def print_errors_table(errors: Sequence[dict[str, Any]]) -> None:
    if not errors:
        return

    table = Table(title="Validation Errors", header_style="bold red")
    table.add_column("Record", justify="right")
    table.add_column("Field")
    table.add_column("Error Type")
    table.add_column("Message")

    for error in errors:
        record_number = str(error.get("record_number", "-"))
        for item in error.get("errors", []):
            table.add_row(
                record_number,
                str(item.get("field", "")),
                str(item.get("error_type", "")),
                str(item.get("message", "")),
            )

    console.print(table)


def print_generic_success_table(valid_records: Sequence[Any]) -> None:
    if not valid_records:
        console.print("[yellow]No valid records found.[/yellow]")
        return

    table = Table(title="Valid Records", header_style="bold green")
    table.add_column("Record", justify="right")
    table.add_column("Data", style="white")

    for index, record in enumerate(valid_records, start=1):
        if hasattr(record, "model_dump"):
            payload = record.model_dump()
        else:
            payload = str(record)

        table.add_row(str(index), str(payload))

    console.print(table)
