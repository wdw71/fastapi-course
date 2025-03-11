from typing import Optional
from fastapi import FastAPI, Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(app.root_path, "static", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of the post 1", "id": 1},{
    "title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return{"data": my_posts}

@app.post("/posts/")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return{"data": post_dict}

@app.get("/posts/latest")
def get_latest_post()):
    post = my_posts(len(my_posts)-1)
    return{"detail latest": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    print(post)
    return{"post_detail": post}
