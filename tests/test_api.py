from fastapi import FastAPI
from starlette.testclient import TestClient

app = FastAPI()
client = TestClient(app)


@app.post('/api/auth/mail/')
def auth_mail():
    return {}


def test_auth_by_mail():
    response = client.post('/api/auth/mail/')
    assert response.status_code == 200
