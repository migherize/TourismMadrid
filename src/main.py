from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home_page():
    return {"page": "home"}



@app.get("/spider-crawl")
def crawler():
    return {}