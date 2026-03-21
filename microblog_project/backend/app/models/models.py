from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Table,
)


# Связующая таблица лайков
tweet_likes = Table(
    "tweet_likes", Base.metadata,
    Column("tweet_id", Integer, ForeignKey("tweets.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now())
)

# Связующая таблица подписок
user_follows = Table(
    "user_follows", Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now())
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    api_key = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    tweets = relationship("Tweet", back_populates="author")
    medias = relationship("Media", back_populates="uploader")
    likes = relationship("Tweet", secondary=tweet_likes, back_populates="likers")
    followers = relationship(
        "User",
        secondary=user_follows,
        primaryjoin=user_follows.c.following_id == id,
        secondaryjoin=user_follows.c.follower_id == id,
        back_populates="following"
    )
    following = relationship(
        "User",
        secondary=user_follows,
        primaryjoin=user_follows.c.follower_id == id,
        secondaryjoin=user_follows.c.following_id == id,
        back_populates="followers"
    )


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), index=True)
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Связи
    author = relationship("User", back_populates="tweets")
    medias = relationship("Media", back_populates="tweet")
    likers = relationship("User", secondary=tweet_likes, back_populates="likes")


class Media(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    uploader = relationship("User", back_populates="medias")
    tweet = relationship("Tweet", back_populates="medias")
