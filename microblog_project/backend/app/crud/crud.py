from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.models import User, Tweet, Media, tweet_likes, user_follows


def get_user_by_api_key(db: Session, api_key: str | None = None):
    """
    Получить пользователя по API-KEY
    """
    if not api_key or api_key.strip() == '':

        return None

    return db.query(User).filter(User.api_key == api_key.strip()).first()


def get_user_by_id(db: Session, user_id: int):
    """
    Получить пользователя по ID
    """

    return db.query(User).filter(User.id == user_id).first()


def create_tweet(db: Session, tweet_data: str, user_id: int, media_ids: list = []):
    """
    Создать твит с медиафайлами
    """
    tweet = Tweet(content=tweet_data.strip()[:280], author_id=user_id)
    db.add(tweet)
    db.commit()
    db.refresh(tweet)

    for media_id in media_ids:
        media = db.query(Media).filter(Media.id == media_id).first()
        if media:
            media.tweet_id = tweet.id
            db.commit()

    return tweet


def delete_tweet(db: Session, tweet_id: int, user_id: int):
    """
    Удалить свой твит
    """
    tweet = db.query(Tweet).filter(and_(Tweet.id == tweet_id, Tweet.author_id == user_id)).first()
    if tweet:
        # Каскадное удаление медиа и лайков
        db.query(Media).filter(Media.tweet_id == tweet_id).delete()
        db.query(tweet_likes).filter(tweet_likes.c.tweet_id == tweet_id).delete()
        db.delete(tweet)
        db.commit()

        return True

    return False


def like_tweet(db: Session, tweet_id: int, user_id: int):
    """
    Поставить лайк на твит
    """
    if not db.query(tweet_likes).filter(
            tweet_likes.c.tweet_id == tweet_id,
            tweet_likes.c.user_id == user_id
    ).first():
        db.execute(tweet_likes.insert().values(tweet_id=tweet_id, user_id=user_id))
        db.commit()

    return True


def unlike_tweet(db: Session, tweet_id: int, user_id: int):
    """
    Убрать лайк с твита
    """
    likes_deleted = db.execute(tweet_likes.delete().where(
        and_(tweet_likes.c.tweet_id == tweet_id, tweet_likes.c.user_id == user_id)
    ))
    db.commit()

    return likes_deleted.rowcount > 0


def follow_user(db: Session, follower_id: int, following_id: int):
    """
    Подписаться на пользователя
    """
    if (follower_id != following_id and
            not db.query(user_follows).filter(
                user_follows.c.follower_id == follower_id,
                user_follows.c.following_id == following_id
            ).first()):
        db.execute(user_follows.insert().values(
            follower_id=follower_id,
            following_id=following_id
        ))
        db.commit()

        return True

    return False


def unfollow_user(db: Session, follower_id: int, following_id: int):
    """
    Отписаться от пользователя
    """
    result = db.execute(user_follows.delete().where(
        and_(
            user_follows.c.follower_id == follower_id,
            user_follows.c.following_id == following_id
        )
    ))
    db.commit()

    return result.rowcount > 0


def get_user_profile(db: Session, user_id: int):
    """
    Профиль пользователя
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    followers = db.query(User.id, User.name).join(
        user_follows,
        user_follows.c.follower_id == User.id
    ).filter(
        user_follows.c.following_id == user_id
    ).all()

    following = db.query(User.id, User.name).join(
        user_follows,
        user_follows.c.following_id == User.id
    ).filter(
        user_follows.c.follower_id == user_id
    ).all()

    return {
        "id": user.id,
        "name": user.name,
        "followers": [{"id": f.id, "name": f.name} for f in followers],
        "following": [{"id": f.id, "name": f.name} for f in following]
    }


def create_media(db: Session, filename: str, user_id: int):
    """
    Создать медиа запись
    """
    media = Media(filename=filename, user_id=user_id, tweet_id=None)
    db.add(media)
    db.commit()
    db.refresh(media)

    return media