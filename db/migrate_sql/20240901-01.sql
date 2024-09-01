-- ノートテーブルの処理
DROP TABLE notes;

CREATE TABLE public.notes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying NOT NULL,
    seq integer NOT NULL,
    uid character varying NOT NULL,
    created_at timestamp(6) without time zone NOT NULL,
    updated_at timestamp(6) without time zone NOT NULL
);

ALTER TABLE ONLY public.notes ADD CONSTRAINT notes_pkey PRIMARY KEY (id);
CREATE UNIQUE INDEX index_notes_on_seq_and_uid ON public.notes USING btree (seq, uid);


-- セクションテーブルの処理
DROP TABLE sections;

CREATE TABLE public.sections (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying NOT NULL,
    seq integer NOT NULL,
    note_id uuid NOT NULL,
    created_at timestamp(6) without time zone NOT NULL,
    updated_at timestamp(6) without time zone NOT NULL
);

ALTER TABLE ONLY public.sections ADD CONSTRAINT sections_pkey PRIMARY KEY (id);
CREATE UNIQUE INDEX index_sections_on_seq_and_note_id ON public.sections USING btree (seq, note_id);


-- ページテーブルの処理
DROP TABLE pages;

CREATE TABLE public.pages (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    title character varying NOT NULL,
    content character varying NOT NULL,
    seq integer NOT NULL,
    section_id uuid NOT NULL,
    created_at timestamp(6) without time zone NOT NULL,
    updated_at timestamp(6) without time zone NOT NULL
);

ALTER TABLE ONLY public.pages ADD CONSTRAINT pages_pkey PRIMARY KEY (id);
CREATE UNIQUE INDEX index_pages_on_seq_and_section_id ON public.pages USING btree (seq, section_id);
