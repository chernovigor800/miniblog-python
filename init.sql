-- Создание основных таблиц
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    api_key VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tweets (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id),
    likes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS medias (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    user_id INTEGER REFERENCES users(id),
    tweet_id INTEGER REFERENCES tweets(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tweet_likes (
    tweet_id INTEGER REFERENCES tweets(id),
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tweet_id, user_id)
);

CREATE TABLE IF NOT EXISTS user_follows (
    follower_id INTEGER REFERENCES users(id),
    following_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, following_id)
);

-- Занесение в таблицы тестовых данных
INSERT INTO users (id, name, api_key, created_at) VALUES
(1, 'Иван Иванов', 'test', '2026-01-10 05:15:51.066318+00'),
(2, 'Мария Петрова', 'test-1', '2026-01-10 05:15:51.066318+00'),
(3, 'Петр Сидоров', 'test-2', '2026-01-10 05:15:51.066318+00'),
(4, 'Игорь Чернов', 'test-3', '2026-01-10 05:15:51.066318+00')
ON CONFLICT (id) DO NOTHING;


INSERT INTO tweets (id, content, author_id, likes_count, created_at) VALUES
(1, 'Угадаете актера???', 1, 0, '2026-01-10 09:38:48.604124+00'),
(2, 'Вот это десктоп!!!', 2, 0, '2026-01-10 09:41:08.423615+00'),
(3, '«Если кто-нибудь может с очевидностью доказать мне, что я неправильно сужу или действую, то я с радостью изменюсь. Ибо я ищу истины, от которой еще никто никогда не потерпел вреда. Терпит же вред тот, кто упорствует в своем заблуждении и невежестве». — Марк Аврелий.', 3, 0, '2026-01-10 09:48:48.888882+00'),
(4, 'Какую заставку выбрать, подскажите!?', 4, 0, '2026-01-10 09:56:05.048986+00')
ON CONFLICT (id) DO UPDATE SET content = EXCLUDED.content, likes_count = EXCLUDED.likes_count;


INSERT INTO medias (id, filename, user_id, tweet_id, created_at) VALUES
(1, '4b6c6eac2170.jpg', 1, 1, '2026-01-10 09:38:48.157595+00'),
(2, '4e2c1dfdd0ae.jpeg', 2, 2, '2026-01-10 09:41:08.189467+00'),
(3, '8d98daeaa1e0.jpg', 4, 4, '2026-01-10 09:56:04.496598+00'),
(4, '72391de01b36.jpg', 4, 4, '2026-01-10 09:56:04.773314+00'),
(5, '44aca17c3af4.jpg', 4, 4, '2026-01-10 09:56:04.951313+00')
ON CONFLICT (id) DO NOTHING;


INSERT INTO tweet_likes (tweet_id, user_id, created_at) VALUES
(1, 1, '2026-01-10 09:38:52.952628+00'),
(1, 2, '2026-01-10 09:41:13.948119+00'),
(2, 2, '2026-01-10 09:41:15.220638+00'),
(2, 3, '2026-01-10 09:48:56.039925+00'),
(1, 3, '2026-01-10 09:48:57.48022+00'),
(3, 4, '2026-01-10 09:51:28.006462+00'),
(2, 4, '2026-01-10 09:51:30.934009+00'),
(1, 4, '2026-01-10 09:51:32.717574+00'),
(4, 4, '2026-01-10 09:56:08.907929+00')
ON CONFLICT (tweet_id, user_id) DO NOTHING;


INSERT INTO user_follows (follower_id, following_id, created_at) VALUES
(2, 1, '2026-01-10 09:42:02.748563+00'),
(3, 1, '2026-01-10 09:49:01.029983+00'),
(4, 1, '2026-01-10 09:51:35.59777+00')
ON CONFLICT (follower_id, following_id) DO NOTHING;


SELECT setval('users_id_seq', 4, true);
SELECT setval('tweets_id_seq', 4, true);
SELECT setval('medias_id_seq', 5, true);
