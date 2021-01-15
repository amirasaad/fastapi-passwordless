import smtplib

import pytest


@pytest.fixture(scope="session")
def smtp_conn():
    with smtplib.SMTP(host="127.0.0.1", port="1025") as smtp:
        yield smtp
        smtp.close()
