import logging

from fastapi import FastAPI


logger = logging.getLogger("uvicorn")
logger.setLevel("INFO")

app = FastAPI()


@app.get("/")
def read_root():
    logger.info("test")
    return {"Hello": "World"}
