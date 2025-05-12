from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def greet():
    return {"say": "hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int , q : str | None = None):
    return {"item_id": item_id , "q": q}
