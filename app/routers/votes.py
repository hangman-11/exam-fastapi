from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, model
from .. import oauth2

router = APIRouter(
    prefix="/vote",
    tags=['vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    vote_query = db.query(model.vote).filter(model.vote.post_id == vote.post_id,
                                             model.vote.user_id == current_user.id)
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    found_vote = vote_query.first()

    if vote.dir == 1:
        if not post :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the post you want to like doesn't exist")
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"the user {current_user.id}"
                                       f" has already voted on this post with id {vote.post_id}")

        new_vote = model.vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the vote does not exist")

        vote_query.delete(synchronize_session=False)
