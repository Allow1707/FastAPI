CREATE TABLE public.products (
    id SERIAL PRIMARY KEY,
    uuid TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    price FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT (now() AT TIME ZONE 'UTC') NOT NULL
);