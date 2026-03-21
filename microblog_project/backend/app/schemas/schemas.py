from pydantic import BaseModel
from typing import List, Optional


class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = []