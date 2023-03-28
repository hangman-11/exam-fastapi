from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import utils, schemas, model

routers = APIRouter(
    prefix="/users",
    tags=['user']
)


@routers.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def user_create(data: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pass = utils.hashing(data.password)
    data.password = hashed_pass
    new_user = model.User(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@routers.get("/{id}", response_model=schemas.SingleUserResponse)
def find_user(id: int, db: Session = Depends(get_db)):
    user_data = db.query(model.User).filter(model.User.id == id).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id:{id} not found")
    return user_data
