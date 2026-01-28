import pytest
from parser import parse_web


@pytest.mark.parametrize(
    "line, expected_ip, expected_fragment, expected_status",
    [
        (
            "10.0.0.88 - - [03/Jul/2025:10:00:16 +0000] "
            '"GET /search?q=1; DROP TABLE users-- HTTP/1.1" 200 54',
            "10.0.0.88",
            "DROP TABLE",
            200,
        ),
        (
            "192.168.1.10 - - [03/Jul/2025:10:00:01 +0000] "
            '"GET /index.html HTTP/1.1" 200 1234',
            "192.168.1.10",
            "/index.html",
            200,
        ),
    ],
)
def test_parse_web(line, expected_ip, expected_fragment, expected_status):
    log = parse_web(line)

    assert log is not None
    assert log.ip == expected_ip
    assert expected_fragment in log.path
    assert log.status == expected_status
