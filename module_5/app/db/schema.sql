CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    uuid TEXT UNIQUE,
    full_name TEXT,
    created_at TIMESTAMP DEFAULT (now() AT TIME ZONE 'UTC') NOT NULL,
    updated_at TIMESTAMP DEFAULT (now() AT TIME ZONE 'UTC') NOT NULL
);