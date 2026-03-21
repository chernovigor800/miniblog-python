from fastapi import FastAPI
from app.api import users, tweets, media


app = FastAPI(
    title="Microblog API",
    version="1.0",
    docs_url="/docs",
)

# Подключение роутеров
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(media.router)