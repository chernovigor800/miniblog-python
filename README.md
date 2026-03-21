**Miniblog (X-clone)** 

Описание:
---------  
   Аналог известного приложения X на Python с базой данных
   PostgreSQL. Многопользовательская платформа для коротких постов 
   с медиа, лайками и подписками. API-first архитектура с SQLAlchemy
   ORM и тестовой базой данных. Раздача статики и фронтенда 
   реализована при помощи nginx-сервера. Приложение протестировано 
   при помощи pytest. Код проверен линтерами ruff, mypy.

Основной функционал:
--------------------
    - Регистрация пользователей с уникальным api_key
    - Публикация твитов с текстом и несколькими изображениями
    - Система лайков (счётчик + точный список)
    - Подписки (follow/unfollow)
    - Лента по подпискам + свои посты
    - Хранение медиафайлов

База данных PostgreSQL со следующими таблицами:
-----------------------------------------------
    - users — пользователи (name, api_key, created_at)
    - tweets — посты (content, author_id, likes_count, created_at)
    - medias — изображения (filename, user_id, tweet_id, created_at)
    - tweet_likes — связи лайков
    - user_follows — подписки

Тестовые данные:
----------------
    4 пользователя, 4 твита, 5 медиафайлов, лайки и подписки.

Запуск приложения:
------------------
1. Команда для запуска приложения:

    docker compose up --build -d 

2. При запуске докер-контейнера с базой PostgreSQL автоматически 
   происходит инициализация базы данных с занесением туда тестовых
   данных. Эти данные можно восстановить при помощи команды внутри
   докер-контейнера с базой данных:

    docker compose exec -T db psql -U postgres twitterdb < backup.sql

3. Открываем приложение в адресной строке браузера:

    http://localhost/

4. Ключи Api-key для всех пользователей находящихся в базе данных
   (на главной странице приложение есть форма для ввода):
    test, test-1, test-2, test-3 

5. Запуск Swagger:

    http://localhost/api/docs

6. CI/CD:
    Реализовано 15 интеграционных тестов для Microblog API
    с использованием реального uvicorn сервера и requests.Session. 
    Полное покрытие CRUD операций. Все 15 тестов успешно пройдены.

    Команда для проверки качества кода при запущенном Docker:

    docker compose exec api sh -c "
      echo 'Check Ruff ...' && 
      ruff check app/ tests/ &&
      echo 'Ruff: OK' ||
      (echo 'Ruff: warnings' && exit 1) &&
      
      echo 'Check Mypy ...' && 
      mypy app/ tests/ &&
      echo 'Mypy: OK' ||
      (echo 'Mypy: type errors' && exit 1) &&
      
      echo 'Check Tests ...' && 
      pytest tests/ -v &&
      echo 'Tests: PASSED' &&
      
      echo 'All tests and linters PASSED!'
    "
