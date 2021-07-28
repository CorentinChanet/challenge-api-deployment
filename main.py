from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from schemas.pydantic_models import Property
from preprocessing.cleaning_data import preprocess
from predict.prediction import predict

app = FastAPI()

app.mount( "/static",
    StaticFiles(directory="/app/static"),
    name="static")

port = int(os.environ.get("PORT", 8000))

templates = Jinja2Templates(directory="/app/templates")


@app.get("/")
def read_root():
    return """This API expects a JSON containing real-estate information. Go to https://corentin-api-test.herokuapp.com/predict/ for more information."""


@app.get("/predict/")
def read_predict(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict/")
def price_prediction(item: Property):
    property = dict(item)
    return {'price' : predict(preprocess(property))}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)

# docker run -it -v $PWD/app:/app -p 127.0.0.1:8000:8000 -t fastapi:latest bash