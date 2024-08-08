from fastapi.testclient import TestClient
from starlette.datastructures import Headers

from main import app, get_request_id


client = TestClient(app)


def test_get_request_id() -> None:
    headers = Headers(
        {
            "x-amzn-lambda-context": '{"request_id":"85203a83-e02c-4284-b6dd-3f0def1ae128"}',
        }
    )
    request_id = get_request_id(headers=headers)
    assert request_id == "85203a83-e02c-4284-b6dd-3f0def1ae128"


def test_read_main() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
