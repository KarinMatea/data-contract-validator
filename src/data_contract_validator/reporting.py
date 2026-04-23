from html import escape
from pathlib import Path

from data_contract_validator.models import UserContract


def generate_html_report(valid_users: list[UserContract], errors: list[dict]) -> str:
    error_items = []

    for error in errors:
        detail_items = []

        for detail in error["errors"]:
            detail_items.append(
                "<li>"
                f"<strong>{escape(detail['field'])}</strong>: "
                f"{escape(detail['message'])} "
                f"<code>{escape(repr(detail['input_value']))}</code>"
                "</li>"
            )

        error_items.append(
            "<section class='error-record'>"
            f"<h3>Record {error['record_number']}</h3>"
            "<ul>"
            f"{''.join(detail_items)}"
            "</ul>"
            "</section>"
        )

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Validation Report</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 2rem auto;
      max-width: 900px;
      padding: 0 1rem;
      background: #f7f7f7;
      color: #222;
    }}
    h1, h2, h3 {{
      color: #111;
    }}
    .summary {{
      background: white;
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 1.5rem;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
    }}
    .error-record {{
      background: #fff4f4;
      border: 1px solid #f0caca;
      border-radius: 8px;
      padding: 1rem;
      margin-bottom: 1rem;
    }}
    code {{
      background: #eee;
      padding: 0.1rem 0.3rem;
      border-radius: 4px;
    }}
  </style>
</head>
<body>
  <h1>Validation Report</h1>

  <section class="summary">
    <h2>Summary</h2>
    <p>Valid records: <strong>{len(valid_users)}</strong></p>
    <p>Invalid records: <strong>{len(errors)}</strong></p>
  </section>

  <section>
    <h2>Error details</h2>
    {"".join(error_items) if error_items else "<p>No validation errors found.</p>"}
  </section>
</body>
</html>
"""
    return html.strip()


def write_html_report(file_path: str, html_content: str) -> None:
    path = Path(file_path)
    path.write_text(html_content, encoding="utf-8")
