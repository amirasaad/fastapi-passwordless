import smtplib
from typing import List

import pytest
from fastapi import FastAPI, Header, HTTPException
from fastapi.security import HTTPBasic
from pydantic import BaseModel, EmailStr
from starlette.testclient import TestClient

app = FastAPI()
client = TestClient(app)

security = HTTPBasic()

fake_secret_token = "coneofsilence"

smtp = smtplib.SMTP(host="127.0.0.1", port=1025)


class EmailSchema(BaseModel):
    email: List[EmailStr]


@app.post("/api/auth/mail/")
def auth_mail(email: EmailSchema):
    try:
        smtp.sendmail(
            from_addr="admin@test.com", to_addrs=email.dict().get("email"),
            msg="hello"
        )
    except smtplib.SMTPException:
        print("error")
    return {}


@app.get("/secret")
def secret(x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"secret": "Here is your secret"}


def test_auth_by_mail(smtp_conn):
    response = client.post("/api/auth/mail/", json={"email": ["john.doe@example.com"]})
    smtp_response, msg = smtp_conn.ehlo()
    assert smtp_response == 250
    print(response.json())
    assert response.status_code == 200


def test_unauthorized_request():
    response = client.get("/secret", headers={"X-Token": "w"})
    assert response.status_code == 401


def test_authorized_request():
    response = client.get("/secret", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
