from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, model, utils, database, oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login")
def login_auth(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email_address == user_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    if not utils.verify(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    access_token = oauth2.create_token(data={"user_id": user.id})

    return {"token ": access_token, "type": "bearer"}
