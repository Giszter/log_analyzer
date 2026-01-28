import pytest
from parser import parse_auth


@pytest.mark.parametrize(
    "line, expected_ip, expected_phrase",
    [
        (
            "Jul  3 10:00:03 server sshd[1234]: "
            "Failed password for admin from 10.0.0.50 port 52341 ssh2",
            "10.0.0.50",
            "Failed password",
        ),
        (
            "Jul  3 10:00:07 server sshd[1234]: "
            "Accepted password for admin from 10.0.0.50 port 52345 ssh2",
            "10.0.0.50",
            "Accepted password",
        ),
    ],
)
def test_parse_auth(line, expected_ip, expected_phrase):
    log = parse_auth(line)

    assert log is not None
    assert log.ip == expected_ip
    assert expected_phrase in log.message
