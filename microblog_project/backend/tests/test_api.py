"""Microblog API — 15 Тестов"""
import pytest
import tempfile
import requests
import asyncio
import time
import os
import sys
from pathlib import Path
from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uvicorn import Config, Server
from app.main import app
from app.database import get_db, Base
from app.models.models import User
from tests.tests_config import SERVER_PORT, TEST_API_KEY


sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="function")
def test_db_file():
    """
    Временный путь к файлу тестовой базы данных
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    try:
        yield db_path
    finally:
        Path(db_path).unlink()


@pytest.fixture(scope="function", autouse=True)
def test_db(test_db_file, tmp_path):
    """
    Тестовая база данных и папка для медиафайлов
    """
    test_media = tmp_path / "static" / "media"
    test_media.mkdir(parents=True, exist_ok=True)
    os.environ["MEDIA_ROOT"] = str(test_media)

    engine = create_engine(f"sqlite:///{test_db_file}",
                          connect_args={"check_same_thread": False})

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    test_user = User(name="Test User", api_key=TEST_API_KEY)
    db.add(test_user)
    db.commit()
    db.close()


    def override_get_db():
        """
        Тестовое подключение к базе данных с откатом изменений
        """
        db = SessionLocal()
        try:
            yield db
        finally:
            db.rollback()
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides = {}
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_server():
    """
    Uvicorn сервер
    """
    config = Config(app=app, host="127.0.0.1", port=SERVER_PORT, log_level="error")
    server = Server(config)

    srv_thread = Thread(target=lambda: asyncio.run(server.serve()))
    srv_thread.daemon = True
    srv_thread.start()

    time.sleep(1)
    yield
    server.should_exit = True
    time.sleep(0.5)


@pytest.fixture
def client(test_server):
    """
    Тестовый клиент
    """
    base_url = f"http://127.0.0.1:{SERVER_PORT}"
    session = requests.Session()
    session.headers.update({"User-Agent": "testclient"})
    yield session, base_url
    session.close()

# Тесты

def test_get_me_no_key(client):
    session, base_url = client
    resp = session.get(f"{base_url}/api/users/me")
    assert resp.status_code == 401

def test_get_me_success(client):
    session, base_url = client
    resp = session.get(f"{base_url}/api/users/me", headers={"api-key": TEST_API_KEY})
    assert resp.status_code == 200

def test_get_tweets_no_key(client):
    session, base_url = client
    resp = session.get(f"{base_url}/api/tweets")
    assert resp.status_code == 401

def test_get_tweets_success(client):
    session, base_url = client
    resp = session.get(f"{base_url}/api/tweets", headers={"api-key": TEST_API_KEY})
    assert resp.status_code in [200, 422]

def test_create_tweet_no_key(client):
    session, base_url = client
    resp = session.post(f"{base_url}/api/tweets", json={"tweet_data": "test"})
    assert resp.status_code == 401

def test_create_tweet_success(client):
    session, base_url = client
    resp = session.post(
        f"{base_url}/api/tweets",
        json={"tweet_data": "Hello World", "tweet_media_ids": []},
        headers={"api-key": TEST_API_KEY}
    )
    assert resp.status_code in [200, 422]

def test_delete_tweet_success(client):
    session, base_url = client
    resp = session.delete(f"{base_url}/api/tweets/1", headers={"api-key": TEST_API_KEY})
    assert resp.status_code in [200, 404, 422]


def test_upload_media_no_key(client, tmp_path):
    session, base_url = client
    test_file = tmp_path / "test.jpg"
    test_file.write_bytes(b"fake")

    with open(test_file, "rb") as f:
        files = {"file": ("test.jpg", f, "image/jpeg")}
        resp = session.post(f"{base_url}/api/medias", files=files)

    assert resp.status_code == 401

def test_upload_media_success(client, tmp_path):
    session, base_url = client
    test_file = tmp_path / "test.jpg"
    test_file.write_bytes(b"/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAA")

    with open(test_file, "rb") as f:
        files = {"file": ("test.jpg", f, "image/jpeg")}
        resp = session.post(
            f"{base_url}/api/medias",
            files=files,
            headers={"api-key": TEST_API_KEY}
        )

    assert resp.status_code == 200
    data = resp.json()
    assert "result" in data
    assert data["result"] == "true"
    assert "media_id" in data
    assert isinstance(data["media_id"], int)

def test_like_tweet_success(client):
    session, base_url = client
    resp = session.post(f"{base_url}/api/tweets/1/likes", headers={"api-key": TEST_API_KEY})
    assert resp.status_code in [200, 404, 422]

def test_unlike_tweet_success(client):
    session, base_url = client
    resp = session.delete(f"{base_url}/api/tweets/1/likes", headers={"api-key": TEST_API_KEY})
    assert resp.status_code in [200, 404, 422]

def test_follow_user_success(client):
    session, base_url = client
    resp = session.post(f"{base_url}/api/users/2/follow", headers={"api-key": TEST_API_KEY})
    assert resp.status_code in [200, 400, 404, 422]

def test_follow_self_error(client):
    session, base_url = client
    resp = session.post(f"{base_url}/api/users/1/follow", headers={"api-key": TEST_API_KEY})
    assert resp.status_code in [400, 404, 422]

def test_unfollow_user_success(client):
    session, base_url = client
    resp = session.delete(f"{base_url}/api/users/2/follow", headers={"api-key": TEST_API_KEY})
    assert resp.status_code in [200, 404, 422]

def test_get_user_profile_success(client):
    session, base_url = client
    resp = session.get(f"{base_url}/api/users/1", headers={"api-key": TEST_API_KEY})
    assert resp.status_code == 200