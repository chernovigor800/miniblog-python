from fastapi import Request, Response, HTTPException
from sqlalchemy.orm import Session

from app.models.models import User
from app.crud.crud import get_user_by_api_key
from app.core.config import API_KEY_HEADER


def get_api_key(request: Request) -> str:
    """
    Извлечь API ключ из заголовков
    """
    return request.headers.get(API_KEY_HEADER) or ""


def set_api_key_header(response: Response, api_key: str) -> None:
    """
    Установить API ключ в заголовки ответа
    """
    response.headers[API_KEY_HEADER] = api_key


def require_user(db: Session, api_key: str) -> User:
    """
    Получить аутентифицированного пользователя
    """
    user = get_user_by_api_key(db, api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid api-key")
    return user