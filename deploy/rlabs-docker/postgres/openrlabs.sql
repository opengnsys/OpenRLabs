--
-- PostgreSQL database dump
--

-- Dumped from database version 10.17 (Debian 10.17-1.pgdg90+1)
-- Dumped by pg_dump version 10.17 (Ubuntu 10.17-0ubuntu0.18.04.1)

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

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: active_directory; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.active_directory (
    id integer NOT NULL,
    admin_ad character varying(128),
    password character varying(128),
    server_ad character varying(512),
    base_db character varying(512)
);


ALTER TABLE public.active_directory OWNER TO openrlabs;

--
-- Name: active_directory_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.active_directory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.active_directory_id_seq OWNER TO openrlabs;

--
-- Name: active_directory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.active_directory_id_seq OWNED BY public.active_directory.id;


--
-- Name: reserves; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.reserves (
    id integer NOT NULL,
    user_id integer,
    ou_id character varying(512),
    lab_id character varying(512),
    pc_id character varying(512),
    pc_name character varying(512),
    expiration_time timestamp without time zone,
    ip character varying(512) NOT NULL,
    protocol character varying(512),
    port character varying(512),
    os character varying(512),
    is_assigned boolean DEFAULT false NOT NULL,
    assigned_init_time timestamp without time zone,
    image_id character varying NOT NULL,
    reserved_init_time timestamp without time zone NOT NULL,
    prereserve_id integer,
    mac character varying NOT NULL
);


ALTER TABLE public.reserves OWNER TO openrlabs;

--
-- Name: active_reserves_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.active_reserves_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.active_reserves_id_seq OWNER TO openrlabs;

--
-- Name: active_reserves_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.active_reserves_id_seq OWNED BY public.reserves.id;


--
-- Name: auth_cas; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.auth_cas (
    id integer NOT NULL,
    user_id integer,
    created_on timestamp without time zone,
    service character varying(512),
    ticket character varying(512),
    renew character(1)
);


ALTER TABLE public.auth_cas OWNER TO openrlabs;

--
-- Name: auth_cas_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.auth_cas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_cas_id_seq OWNER TO openrlabs;

--
-- Name: auth_cas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.auth_cas_id_seq OWNED BY public.auth_cas.id;


--
-- Name: auth_event; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.auth_event (
    id integer NOT NULL,
    time_stamp timestamp without time zone,
    client_ip character varying(512),
    user_id integer,
    origin character varying(512),
    description text
);


ALTER TABLE public.auth_event OWNER TO openrlabs;

--
-- Name: auth_event_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.auth_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_event_id_seq OWNER TO openrlabs;

--
-- Name: auth_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.auth_event_id_seq OWNED BY public.auth_event.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    role character varying(512),
    description text
);


ALTER TABLE public.auth_group OWNER TO openrlabs;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO openrlabs;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_membership; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.auth_membership (
    id integer NOT NULL,
    user_id integer,
    group_id integer
);


ALTER TABLE public.auth_membership OWNER TO openrlabs;

--
-- Name: auth_membership_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.auth_membership_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_membership_id_seq OWNER TO openrlabs;

--
-- Name: auth_membership_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.auth_membership_id_seq OWNED BY public.auth_membership.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    group_id integer,
    name character varying(512),
    table_name character varying(512),
    record_id integer
);


ALTER TABLE public.auth_permission OWNER TO openrlabs;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO openrlabs;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    first_name character varying(128),
    last_name character varying(128),
    email character varying(512),
    password character varying(512),
    registration_key character varying(512),
    reset_password_key character varying(512),
    registration_id character varying(512),
    username character varying(128)
);


ALTER TABLE public.auth_user OWNER TO openrlabs;

--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO openrlabs;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: labs_timetable; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.labs_timetable (
    id integer NOT NULL,
    lab_id integer NOT NULL,
    lab_name character varying(512) NOT NULL,
    "Init_Day" integer NOT NULL,
    "End_Day" integer NOT NULL,
    "Init_time" time without time zone NOT NULL,
    "End_time" time without time zone NOT NULL,
    cod_asign character varying
);


ALTER TABLE public.labs_timetable OWNER TO openrlabs;

--
-- Name: labs_timetable_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.labs_timetable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.labs_timetable_id_seq OWNER TO openrlabs;

--
-- Name: labs_timetable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.labs_timetable_id_seq OWNED BY public.labs_timetable.id;


--
-- Name: nip_groups; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.nip_groups (
    id integer NOT NULL,
    nip character varying(128) NOT NULL,
    groups text NOT NULL
);


ALTER TABLE public.nip_groups OWNER TO openrlabs;

--
-- Name: nip_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.nip_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nip_groups_id_seq OWNER TO openrlabs;

--
-- Name: nip_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.nip_groups_id_seq OWNED BY public.nip_groups.id;


--
-- Name: openRLabs_setup; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public."openRLabs_setup" (
    id integer NOT NULL,
    "URL_Apache_Guacamole_WebSocket" character varying(512),
    "URL_openGnsys_server" character varying(512),
    "URL_openRLabs_server" character varying(512),
    maxtime_reserve character varying(512),
    seconds_to_wait integer DEFAULT 200 NOT NULL,
    auth_mode character varying(512)
);


ALTER TABLE public."openRLabs_setup" OWNER TO openrlabs;

--
-- Name: openRLabs_setup_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public."openRLabs_setup_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."openRLabs_setup_id_seq" OWNER TO openrlabs;

--
-- Name: openRLabs_setup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public."openRLabs_setup_id_seq" OWNED BY public."openRLabs_setup".id;


--
-- Name: ous_setup; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.ous_setup (
    id integer NOT NULL,
    ou_id character varying(512),
    ou_name character varying(512),
    ou_user character varying(512),
    ou_password character varying(512)
);


ALTER TABLE public.ous_setup OWNER TO openrlabs;

--
-- Name: ous_setup_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.ous_setup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ous_setup_id_seq OWNER TO openrlabs;

--
-- Name: ous_setup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.ous_setup_id_seq OWNED BY public.ous_setup.id;


--
-- Name: pop3_servers; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.pop3_servers (
    id integer NOT NULL,
    url character varying(512),
    port integer NOT NULL,
    use_tls boolean DEFAULT true NOT NULL,
    default_server boolean DEFAULT false NOT NULL
);


ALTER TABLE public.pop3_servers OWNER TO openrlabs;

--
-- Name: pop3_servers_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.pop3_servers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pop3_servers_id_seq OWNER TO openrlabs;

--
-- Name: pop3_servers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.pop3_servers_id_seq OWNED BY public.pop3_servers.id;


--
-- Name: pre_reserves; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.pre_reserves (
    id integer NOT NULL,
    lab_id integer NOT NULL,
    lab_name character varying(518) NOT NULL,
    init_time timestamp without time zone NOT NULL,
    finish_time timestamp without time zone NOT NULL,
    num_reserves integer DEFAULT 1 NOT NULL,
    ou_id character varying NOT NULL,
    image_id character varying NOT NULL,
    image_name character varying NOT NULL,
    protocol character varying,
    last_check_time timestamp without time zone
);


ALTER TABLE public.pre_reserves OWNER TO openrlabs;

--
-- Name: pre_reserves_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.pre_reserves_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pre_reserves_id_seq OWNER TO openrlabs;

--
-- Name: pre_reserves_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.pre_reserves_id_seq OWNED BY public.pre_reserves.id;


--
-- Name: services; Type: TABLE; Schema: public; Owner: openrlabs
--

CREATE TABLE public.services (
    id integer NOT NULL,
    name character varying(512),
    port character varying(512)
);


ALTER TABLE public.services OWNER TO openrlabs;

--
-- Name: services_id_seq; Type: SEQUENCE; Schema: public; Owner: openrlabs
--

CREATE SEQUENCE public.services_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.services_id_seq OWNER TO openrlabs;

--
-- Name: services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openrlabs
--

ALTER SEQUENCE public.services_id_seq OWNED BY public.services.id;


--
-- Name: active_directory id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.active_directory ALTER COLUMN id SET DEFAULT nextval('public.active_directory_id_seq'::regclass);


--
-- Name: auth_cas id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_cas ALTER COLUMN id SET DEFAULT nextval('public.auth_cas_id_seq'::regclass);


--
-- Name: auth_event id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_event ALTER COLUMN id SET DEFAULT nextval('public.auth_event_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_membership id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_membership ALTER COLUMN id SET DEFAULT nextval('public.auth_membership_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: labs_timetable id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.labs_timetable ALTER COLUMN id SET DEFAULT nextval('public.labs_timetable_id_seq'::regclass);


--
-- Name: nip_groups id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.nip_groups ALTER COLUMN id SET DEFAULT nextval('public.nip_groups_id_seq'::regclass);


--
-- Name: openRLabs_setup id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public."openRLabs_setup" ALTER COLUMN id SET DEFAULT nextval('public."openRLabs_setup_id_seq"'::regclass);


--
-- Name: ous_setup id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.ous_setup ALTER COLUMN id SET DEFAULT nextval('public.ous_setup_id_seq'::regclass);


--
-- Name: pop3_servers id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.pop3_servers ALTER COLUMN id SET DEFAULT nextval('public.pop3_servers_id_seq'::regclass);


--
-- Name: pre_reserves id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.pre_reserves ALTER COLUMN id SET DEFAULT nextval('public.pre_reserves_id_seq'::regclass);


--
-- Name: reserves id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.reserves ALTER COLUMN id SET DEFAULT nextval('public.active_reserves_id_seq'::regclass);


--
-- Name: services id; Type: DEFAULT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.services ALTER COLUMN id SET DEFAULT nextval('public.services_id_seq'::regclass);


--
-- Name: active_directory active_directory_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.active_directory
    ADD CONSTRAINT active_directory_pkey PRIMARY KEY (id);


--
-- Name: reserves active_reserves_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT active_reserves_pkey PRIMARY KEY (id);


--
-- Name: auth_cas auth_cas_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_cas
    ADD CONSTRAINT auth_cas_pkey PRIMARY KEY (id);


--
-- Name: auth_event auth_event_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_event
    ADD CONSTRAINT auth_event_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_membership auth_membership_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_membership
    ADD CONSTRAINT auth_membership_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: labs_timetable labs_timetable_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.labs_timetable
    ADD CONSTRAINT labs_timetable_pkey PRIMARY KEY (id);


--
-- Name: nip_groups nip_groups_nip_unique; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.nip_groups
    ADD CONSTRAINT nip_groups_nip_unique UNIQUE (nip);


--
-- Name: nip_groups nip_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.nip_groups
    ADD CONSTRAINT nip_groups_pkey PRIMARY KEY (id);


--
-- Name: openRLabs_setup openRLabs_setup_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public."openRLabs_setup"
    ADD CONSTRAINT "openRLabs_setup_pkey" PRIMARY KEY (id);


--
-- Name: ous_setup ous_setup_ou_id_key; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.ous_setup
    ADD CONSTRAINT ous_setup_ou_id_key UNIQUE (ou_id);


--
-- Name: ous_setup ous_setup_ou_name_key; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.ous_setup
    ADD CONSTRAINT ous_setup_ou_name_key UNIQUE (ou_name);


--
-- Name: ous_setup ous_setup_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.ous_setup
    ADD CONSTRAINT ous_setup_pkey PRIMARY KEY (id);


--
-- Name: pop3_servers pop3_servers_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.pop3_servers
    ADD CONSTRAINT pop3_servers_pkey PRIMARY KEY (id);


--
-- Name: pre_reserves prereserves_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.pre_reserves
    ADD CONSTRAINT prereserves_pkey PRIMARY KEY (id);


--
-- Name: services services_name_key; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_name_key UNIQUE (name);


--
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- Name: services services_port_key; Type: CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_port_key UNIQUE (port);


--
-- Name: reserves active_reserves_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT active_reserves_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.auth_user(id) ON DELETE CASCADE;


--
-- Name: auth_cas auth_cas_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_cas
    ADD CONSTRAINT auth_cas_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.auth_user(id) ON DELETE CASCADE;


--
-- Name: auth_event auth_event_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_event
    ADD CONSTRAINT auth_event_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.auth_user(id) ON DELETE CASCADE;


--
-- Name: auth_membership auth_membership_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_membership
    ADD CONSTRAINT auth_membership_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.auth_group(id) ON DELETE CASCADE;


--
-- Name: auth_membership auth_membership_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_membership
    ADD CONSTRAINT auth_membership_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.auth_user(id) ON DELETE CASCADE;


--
-- Name: auth_permission auth_permission_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.auth_group(id) ON DELETE CASCADE;


--
-- Name: reserves reserves__prereserve_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openrlabs
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT reserves__prereserve_id_fkey FOREIGN KEY (prereserve_id) REFERENCES public.pre_reserves(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

