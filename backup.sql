--
-- PostgreSQL database dump
--

\restrict zwiuXlwf92FWKhVeiqCffMbmZogd71lYGilBLAtxeO42Ts4MKpgJhJbcv3vs70N

-- Dumped from database version 15.15
-- Dumped by pg_dump version 15.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: medias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medias (
    id integer NOT NULL,
    filename character varying(255) NOT NULL,
    user_id integer,
    tweet_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.medias OWNER TO postgres;

--
-- Name: medias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.medias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.medias_id_seq OWNER TO postgres;

--
-- Name: medias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.medias_id_seq OWNED BY public.medias.id;


--
-- Name: tweet_likes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tweet_likes (
    tweet_id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.tweet_likes OWNER TO postgres;

--
-- Name: tweets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tweets (
    id integer NOT NULL,
    content text NOT NULL,
    author_id integer,
    likes_count integer DEFAULT 0,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.tweets OWNER TO postgres;

--
-- Name: tweets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tweets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tweets_id_seq OWNER TO postgres;

--
-- Name: tweets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tweets_id_seq OWNED BY public.tweets.id;


--
-- Name: user_follows; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_follows (
    follower_id integer NOT NULL,
    following_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.user_follows OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    api_key character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: medias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medias ALTER COLUMN id SET DEFAULT nextval('public.medias_id_seq'::regclass);


--
-- Name: tweets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets ALTER COLUMN id SET DEFAULT nextval('public.tweets_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: medias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medias (id, filename, user_id, tweet_id, created_at) FROM stdin;
1	4b6c6eac2170.jpg	1	1	2026-01-10 09:38:48.157595+00
2	4e2c1dfdd0ae.jpeg	2	2	2026-01-10 09:41:08.189467+00
3	8d98daeaa1e0.jpg	4	4	2026-01-10 09:56:04.496598+00
5	44aca17c3af4.jpg	4	4	2026-01-10 09:56:04.951313+00
4	72391de01b36.jpg	4	4	2026-01-10 09:56:04.773314+00
\.


--
-- Data for Name: tweet_likes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tweet_likes (tweet_id, user_id, created_at) FROM stdin;
1	1	2026-01-10 09:38:52.952628+00
1	2	2026-01-10 09:41:13.948119+00
2	2	2026-01-10 09:41:15.220638+00
2	3	2026-01-10 09:48:56.039925+00
1	3	2026-01-10 09:48:57.48022+00
3	4	2026-01-10 09:51:28.006462+00
2	4	2026-01-10 09:51:30.934009+00
1	4	2026-01-10 09:51:32.717574+00
4	4	2026-01-10 09:56:08.907929+00
\.


--
-- Data for Name: tweets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tweets (id, content, author_id, likes_count, created_at) FROM stdin;
1	Угадаете актера???	1	0	2026-01-10 09:38:48.604124+00
2	Вот это десктоп!!!	2	0	2026-01-10 09:41:08.423615+00
3	«Если кто-нибудь может с очевидностью доказать мне, что я неправильно сужу или действую, то я с радостью изменюсь. Ибо я ищу истины, от которой еще никто никогда не потерпел вреда. Терпит же вред тот, кто упорствует в своем заблуждении и невежестве». — Марк Аврелий.	3	0	2026-01-10 09:48:48.888882+00
4	Какую заставку выбрать, подскажите!?	4	0	2026-01-10 09:56:05.048986+00
\.


--
-- Data for Name: user_follows; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_follows (follower_id, following_id, created_at) FROM stdin;
2	1	2026-01-10 09:42:02.748563+00
3	1	2026-01-10 09:49:01.029983+00
4	1	2026-01-10 09:51:35.59777+00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, api_key, created_at) FROM stdin;
1	Иван Иванов	test	2026-01-10 05:15:51.066318+00
2	Мария Петрова	test-1	2026-01-10 05:15:51.066318+00
3	Петр Сидоров	test-2	2026-01-10 05:15:51.066318+00
4	Игорь Чернов	test-3	2026-01-10 05:15:51.066318+00
\.


--
-- Name: medias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.medias_id_seq', 5, true);


--
-- Name: tweets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tweets_id_seq', 4, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: medias medias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medias
    ADD CONSTRAINT medias_pkey PRIMARY KEY (id);


--
-- Name: tweet_likes tweet_likes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweet_likes
    ADD CONSTRAINT tweet_likes_pkey PRIMARY KEY (tweet_id, user_id);


--
-- Name: tweets tweets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets
    ADD CONSTRAINT tweets_pkey PRIMARY KEY (id);


--
-- Name: user_follows user_follows_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_follows
    ADD CONSTRAINT user_follows_pkey PRIMARY KEY (follower_id, following_id);


--
-- Name: users users_api_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_api_key_key UNIQUE (api_key);


--
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: medias medias_tweet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medias
    ADD CONSTRAINT medias_tweet_id_fkey FOREIGN KEY (tweet_id) REFERENCES public.tweets(id);


--
-- Name: medias medias_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medias
    ADD CONSTRAINT medias_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: tweet_likes tweet_likes_tweet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweet_likes
    ADD CONSTRAINT tweet_likes_tweet_id_fkey FOREIGN KEY (tweet_id) REFERENCES public.tweets(id);


--
-- Name: tweet_likes tweet_likes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweet_likes
    ADD CONSTRAINT tweet_likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: tweets tweets_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets
    ADD CONSTRAINT tweets_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: user_follows user_follows_follower_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_follows
    ADD CONSTRAINT user_follows_follower_id_fkey FOREIGN KEY (follower_id) REFERENCES public.users(id);


--
-- Name: user_follows user_follows_following_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_follows
    ADD CONSTRAINT user_follows_following_id_fkey FOREIGN KEY (following_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict zwiuXlwf92FWKhVeiqCffMbmZogd71lYGilBLAtxeO42Ts4MKpgJhJbcv3vs70N

