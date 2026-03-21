from fastapi import APIRouter, Request, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database import get_db
from app.models.models import User, user_follows
from app.crud.crud import get_user_profile, follow_user, unfollow_user
from .auth import get_api_key, require_user, set_api_key_header


router = APIRouter(prefix="/api", tags=["users"])


# Мой профиль
@router.get("/users/me")
def get_current_user_profile(
    request: Request, response: Response, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    api_key = get_api_key(request)
    user = require_user(db, api_key)

    followers = (
        db.query(User.id, User.name)
        .join(user_follows, user_follows.c.follower_id == User.id)
        .filter(user_follows.c.following_id == user.id)
        .all()
    )

    following = (
        db.query(User.id, User.name)
        .join(user_follows, user_follows.c.following_id == User.id)
        .filter(user_follows.c.follower_id == user.id)
        .all()
    )

    set_api_key_header(response, api_key)
    print(f"{user.name} | Followers: {len(followers)} | Following: {len(following)}")

    return {
        "result": "true",
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [{"id": f[0], "name": f[1]} for f in followers],
            "following": [{"id": f[0], "name": f[1]} for f in following],
        },
    }


# Профиль по ID
@router.get("/users/{user_id}")
def get_user_profile_handler(
    request: Request, response: Response, user_id: int, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    require_user(db, get_api_key(request))
    profile = get_user_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    set_api_key_header(response, get_api_key(request))
    return {"result": "true", "user": profile}


# Подписаться на пользователя
@router.post("/users/{user_id}/follow")
def follow_user_endpoint(
    request: Request, response: Response, user_id: int, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    api_key = get_api_key(request)
    current_user = require_user(db, api_key)

    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You can't follow yourself")

    if not follow_user(db, current_user.id, user_id):
        raise HTTPException(status_code=400, detail="Following already exists")

    print(f"{current_user.name} → {user_id}")
    set_api_key_header(response, api_key)
    return {"result": "true"}


# Отписаться от пользователя
@router.delete("/users/{user_id}/follow")
def unfollow_user_endpoint(
    request: Request, response: Response, user_id: int, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    api_key = get_api_key(request)
    current_user = require_user(db, api_key)

    unfollow_user(db, current_user.id, user_id)
    print(f"{current_user.name} unfollow {user_id}")

    set_api_key_header(response, api_key)
    return {"result": "true"}
