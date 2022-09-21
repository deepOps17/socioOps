from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['VOTE']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Check if the post exists or not
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    # If the user want to provide a vote
    if vote.dir == 1:
        # Check if the user has already voted on this post
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User has already voted on this post")
        # Vote on that particular post
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added!!"}
    # If the user wants to cancel the vote
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        # Delete the vote
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "vote removed!!"}
