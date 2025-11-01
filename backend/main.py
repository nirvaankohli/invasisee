from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

