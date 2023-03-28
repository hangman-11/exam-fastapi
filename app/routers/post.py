from fastapi import Depends, status, HTTPException, APIRouter
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, model
from .. import oauth2

routers = APIRouter(
    prefix="/posts",
    tags=['post']
)


# current_user: int = Depends(oauth2.get_current_user),
# @routers.get("/", response_model=List[schemas.PostResponse])
@routers.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db),
             limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM app""")
    # post = cursor.fetchall()
    posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(model.Post,
                       func.count(model.Post.id).label("votes")).join(model.vote,
                                                                      model.vote.post_id == model.Post.id,
                                                                      isouter=True).group_by(model.Post.id).all()

    return results


@routers.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(info: schemas.CreatePost, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO app (title,content,is_published) VALUES (%s,%s,%s) RETURNING *""",
    #                (info.title, info.content, info.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    new_post = model.Post(owner_id=current_user.id, **info.dict())
    db.add(new_post)
    db.commit()
    return new_post


@routers.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM app WHERE "id "= %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"the post with {id} not found""}
        # another way is http exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id:{id} not found")
    return post


@routers.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_id=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM app WHERE "id " = %s returning *""", (str(id),))
    # del_post = cursor.fetchone()
    # conn.commit()
    del_post = db.query(model.Post).filter(model.Post.id == id)
    delete_pst = del_post.first()
    if delete_pst is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post wit id :{id} does not exist  ")

    if delete_pst.id != get_id.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you are not authorized")
    del_post.delete(synchronize_session=False)
    db.commit()

    return {"message": "post successfully deleted"}


@routers.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db),
                get_id=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE FROM app SET title = %s, content = %s , is_published =%s WHERE "id " =%s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # upd_post = cursor.fetchone()
    # conn.commit()
    upd_post = db.query(model.Post).filter(model.Post.id == id)
    post_1 = upd_post.first()
    if post_1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post wit id :{id} does not exist  ")
    upd_post.update(post.dict(), synchronize_session=False)

    if post_1.id != get_id.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you are not authorized")

    db.commit()
    return {"message": "post successfully updated "}
