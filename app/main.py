import time
from sqlalchemy.orm import Session
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import model, schemas, utils
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from .routers import userpy, post, auth, votes

# model.Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(host='localhost', dbname='fastapi',
                                user='postgres', password='12345678', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("connection to database successful")
        break
    except Exception as error:
        print("connecting to the database failed ")
        print(f"error :{error}")
        time.sleep(3)

# my_post = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#            {"title": "my fav place", "content": "my home is my favourite place", "id": 2}]


# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p
#
#
# def find_index(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i
origins = ['*']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.routers)
app.include_router(userpy.routers)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "you are a genius stay disciplined"}
