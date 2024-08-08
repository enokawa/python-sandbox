import json
import logging

from fastapi import FastAPI, Request
from starlette.datastructures import Headers


logger = logging.getLogger("uvicorn")
logger.setLevel("INFO")

app = FastAPI()


def get_request_id(headers: Headers) -> str | None:
    lambda_context = headers.get("x-amzn-lambda-context")
    if not lambda_context:
        return None

    request_id = json.loads(lambda_context).get("request_id")
    return request_id


@app.get("/")
def read_root(req: Request):
    request_id = get_request_id(req.headers)
    logger.info(f"request_id: {request_id}")

    return {"Hello": "World"}
