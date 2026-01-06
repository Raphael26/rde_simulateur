--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8
-- Dumped by pg_dump version 16.8

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: zromain
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO zromain;

--
-- Name: user; Type: TABLE; Schema: public; Owner: zromain
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public."user" OWNER TO zromain;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: zromain
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO zromain;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zromain
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: zromain
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: zromain
--

COPY public.alembic_version (version_num) FROM stdin;
808149692999
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: zromain
--

COPY public."user" (id, username, password) FROM stdin;
1	azert	a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
2	zromain	60937bbb9e45b7e9761b2bf6741f96b9b751c8802b901726a6b1fb5e6f8c8d25
3	romainzhang42@gmail.com	
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zromain
--

SELECT pg_catalog.setval('public.user_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: zromain
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: zromain
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

