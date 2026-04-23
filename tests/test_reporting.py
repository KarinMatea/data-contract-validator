from data_contract_validator.reporting import generate_html_report, write_html_report
from data_contract_validator.validator import load_json_file, validate_users


def test_generate_html_report_contains_summary_and_error_details():
    data = load_json_file("sample_data/users.json")
    valid_users, errors = validate_users(data)

    html = generate_html_report(valid_users, errors)

    assert "<h1>Validation Report</h1>" in html
    assert "Valid records: <strong>2</strong>" in html
    assert "Invalid records: <strong>1</strong>" in html
    assert "Record 3" in html
    assert "invalid-email" in html


def test_write_html_report_creates_file(tmp_path):
    report_file = tmp_path / "report.html"
    html_content = "<html><body><h1>Hello</h1></body></html>"

    write_html_report(str(report_file), html_content)

    assert report_file.exists()
    assert "<h1>Hello</h1>" in report_file.read_text(encoding="utf-8")