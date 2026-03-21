from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header
from sqlalchemy.orm import Session

import shutil
import uuid
from pathlib import Path

from app.database import get_db
from app.crud.crud import create_media
from .auth import require_user
from app.core.config import MAX_FILE_SIZE


router = APIRouter(prefix="/api", tags=["media"])


# Добавление медиафайлов
@router.post("/medias")
async def upload_media_file(
        api_key: str = Header(None, alias="api-key"),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):

    user = require_user(db, api_key or "")

    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    media_root = Path("/app/static/media")
    media_root.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename or "").suffix[:5].lower() or ".jpg"
    filename = f"{uuid.uuid4().hex[:12]}{ext}"
    file_path = media_root / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    media = create_media(db, filename, user.id)
    print(f"Media ID: {media.id}")

    return {"result": "true", "media_id": media.id}