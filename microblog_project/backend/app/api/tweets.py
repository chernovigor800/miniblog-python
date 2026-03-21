from fastapi import APIRouter, Request, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Dict, Any
from app.database import get_db
from app.models.models import Tweet, Media, tweet_likes, User
from app.crud.crud import (
    create_tweet, delete_tweet, like_tweet, unlike_tweet
)
from app.schemas.schemas import TweetCreate
from .auth import get_api_key, require_user, set_api_key_header


router = APIRouter(prefix="/api", tags=["tweets"])


# Лента твитов
@router.get("/tweets")
def get_tweet_feed(request: Request, response: Response, db: Session = Depends(get_db)) -> Dict[str, Any]:
    api_key = get_api_key(request)
    require_user(db, api_key)

    tweets = db.query(Tweet).order_by(desc(Tweet.created_at)).limit(20).all()
    result: Dict[str, Any] = {"result": "true", "tweets": []}

    for tweet in tweets:
        medias = db.query(Media).filter(Media.tweet_id == tweet.id).all()
        likes = (
            db.query(tweet_likes.c.user_id, User.name)
            .join(User, tweet_likes.c.user_id == User.id)
            .filter(tweet_likes.c.tweet_id == tweet.id)
            .all()
        )
        result["tweets"].append({
            "id": tweet.id,
            "content": tweet.content,
            "attachments": [f"/media/{m.filename}" for m in medias],
            "author": {"id": tweet.author.id, "name": tweet.author.name},
            "likes": [{"user_id": uid, "name": name} for uid, name in likes],
        })

    set_api_key_header(response, api_key)
    return result


# Добавление нового твита
@router.post("/tweets")
def create_tweet_endpoint(
    tweet: TweetCreate, request: Request, response: Response, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    api_key = get_api_key(request)
    user = require_user(db, api_key)
    new_tweet = create_tweet(db, tweet.tweet_data, user.id, tweet.tweet_media_ids or [])
    print(f"Tweet #{new_tweet.id} от {user.name}")
    set_api_key_header(response, api_key)
    return {"result": "true", "tweet_id": new_tweet.id}


# Удаление своего твита
@router.delete("/tweets/{tweet_id}")
def delete_tweet_endpoint(request: Request, tweet_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    api_key = get_api_key(request)
    user = require_user(db, api_key)
    if not delete_tweet(db, tweet_id, user.id):
        raise HTTPException(status_code=404, detail="Tweet not found")
    print(f"Tweet #{tweet_id} deleted")
    return {"result": "true"}


# Добавление лайков к твитам
@router.post("/tweets/{tweet_id}/likes")
def like_tweet_endpoint(request: Request, response: Response, tweet_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    api_key = get_api_key(request)
    user = require_user(db, api_key)
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    like_tweet(db, tweet_id, user.id)
    print(f"{user.name} liked {tweet_id}")
    set_api_key_header(response, api_key)
    return {"result": "true"}


# Удаление своих лайков с твитов
@router.delete("/tweets/{tweet_id}/likes")
def unlike_tweet_endpoint(request: Request, response: Response, tweet_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    api_key = get_api_key(request)
    user = require_user(db, api_key)
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    unlike_tweet(db, tweet_id, user.id)
    print(f"{user.name} unliked {tweet_id}")
    set_api_key_header(response, api_key)
    return {"result": "true"}
